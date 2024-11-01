set -e -x

if ! [ -f ./common.sh ]; then
    curl https://raw.githubusercontent.com/davidkhala/Microsoft/refs/heads/main/purview/lineage/palsa/common.sh -O
    source ./common.sh
    rm ./common.sh
else
    source ./common.sh
fi

purviewName=$(curl https://raw.githubusercontent.com/davidkhala/azure-utils/refs/heads/main/cli/purview.sh | bash -s name)

deploymentName=newdeploymenttemp

deploy-connector() {
    curl https://raw.githubusercontent.com/microsoft/Purview-ADB-Lineage-Solution-Accelerator/refs/heads/release/2.3/deployment/infra/newdeploymenttemp.json -O

    az deployment group create --resource-group $rg --name $deploymentName --template-file "./newdeploymenttemp.json" --parameters purviewName=$purviewName prefixName= clientid=$clientid clientsecret=$clientsecret resourceTagValues={} --output none

    rm newdeploymenttemp.json

}

deploy-stats() {
    az deployment group show --name $deploymentName --resource-group $rg --query properties.outputs >stats.value.json # cache the result
    # if failure, clean up by `az deployment group delete --name newdeploymenttemp --resource-group $rg`
}
deploy-env() {

    export KVNAME=$(jq -r '.kvName.value' stats.value.json)
    export ADLSNAME=$(jq -r '.storageAccountName.value' stats.value.json) # storageAccountName
}

# Install necessary types into your Purview instance
config-purview() {
    purview_endpoint="https://$purviewName.purview.azure.com"

    tenantid=$(curl https://raw.githubusercontent.com/davidkhala/azure-utils/refs/heads/main/cli/context.sh | bash -s tenant)

    local login_endpoint="https://login.microsoftonline.com/$tenantid/oauth2/token"
    acc_purview_token=$(curl $login_endpoint --data "resource=https://purview.azure.net&client_id=$clientid&client_secret=$clientsecret&grant_type=client_credentials" -H Metadata:true -s | jq -r '.access_token')

    # learnt from https://github.com/microsoft/Purview-ADB-Lineage-Solution-Accelerator/pull/235
    curl https://raw.githubusercontent.com/davidkhala/Microsoft/refs/heads/main/purview/lineage/palsa/Custom_Types.json -O

    curl -s -X POST $purview_endpoint/catalog/api/atlas/v2/types/typedefs -H "Authorization: Bearer $acc_purview_token" -H "Content-Type: application/json" -d @Custom_Types.json >config-purview-out.json

}
config-databricks() {
    # software prequisite block
    {
        if ! unzip -v >/dev/null; then
            echo "unzip is required. Please find and install on your OS"
            exit 1
        fi

        if ! databricks -v; then
            # install DataBricks CLI
            curl -fsSL https://raw.githubusercontent.com/databricks/setup-cli/main/install.sh | sudo sh
            alias dbfs='databricks fs'
        fi
        echo y | az databricks -h >/dev/null
    }

    local adb_rg=${1:-$rg} # The Resource Group of Azure Databricks
    local ADB_WS_NAME=${2:-"az-databricks"}

    adb_detail=$(az databricks workspace show --resource-group $adb_rg --name $ADB_WS_NAME)

    export adb_ws_url=$(jq -r '.workspaceUrl' <<<$adb_detail)

    global_adb_token=$(curl https://raw.githubusercontent.com/davidkhala/azure-utils/refs/heads/main/cli/databricks.sh | bash -s get-access-token)
    echo $global_adb_token | databricks configure --token --host https://$adb_ws_url

    az_token=$(curl https://raw.githubusercontent.com/davidkhala/azure-utils/refs/heads/main/cli/context.sh | bash -s get-access-token)
    adb_ws_id=$(jq -r '.id' <<<$adb_detail)

    adb_api_headers=(
        '-H' "Authorization: Bearer $global_adb_token"
        '-H' "X-Databricks-Azure-SP-Management-Token: $az_token"
        '-H' "X-Databricks-Azure-Workspace-Resource-Id: $adb_ws_id"
        '-H' 'Content-Type: application/json'
    )

    # json for cluster configuration
    # It should include adb_ws_url in namespace to ensure support for managed hive tables out of the box
    cluster_name="openlineage"                                                # name of compute cluster within Databricks
    local adb_ws_url_id=$(echo $adb_ws_url | sed 's/.azuredatabricks.net//g') # ADB-WORKSPACE-ID e.g. `adb-2525538437753513.13`

    # manipulate DBFS
    {
        # Validate connection
        dbfs ls dbfs:/ >/dev/null

        # mkdirs
        dbfs mkdirs dbfs:/databricks/openlineage

        # dbfs cp --overwrite ./openlineage-spark-*.jar               dbfs:/databricks/openlineage/
        {
            # Download Jar File
            curl -O -L https://repo1.maven.org/maven2/io/openlineage/openlineage-spark/0.18.0/openlineage-spark-0.18.0.jar
            dbfs cp --overwrite ./openlineage-spark-*.jar dbfs:/databricks/openlineage/

        }

        # dbfs cp --overwrite ./open-lineage-init-script.sh           dbfs:/databricks/openlineage/open-lineage-init-script.sh
        {

            STAGE_DIR="/dbfs/databricks/openlineage"
            cat <<OUTEREND >open-lineage-init-script.sh
#!/bin/bash

STAGE_DIR="$STAGE_DIR"

echo "BEGIN: Upload Spark Listener JARs"
cp -f $STAGE_DIR/openlineage-spark-*.jar /mnt/driver-daemon/jars || { echo "Error copying Spark Listener library file"; exit 1;}
echo "END: Upload Spark Listener JARs"

echo "BEGIN: Modify Spark config settings"
cat << 'EOF' > /databricks/driver/conf/openlineage-spark-driver-defaults.conf
[driver] {
  "spark.extraListeners" = "io.openlineage.spark.agent.OpenLineageSparkListener"
}
EOF
echo "END: Modify Spark config settings"
OUTEREND
            dbfs cp --overwrite ./open-lineage-init-script.sh dbfs:/databricks/openlineage/open-lineage-init-script.sh
        }
    }

    # TODO create cluster
    {
        local FUNNAME=$(jq -r '.functionAppName.value' stats.value.json)
        local FUNCTION_APP_DEFAULT_HOST_KEY=$(az functionapp keys list --resource-group $rg --name $FUNNAME --query functionKeys.default -o tsv)
        
        cat <<EOF >create-cluster.json
{
    "cluster_name": "$cluster_name",
    "spark_version": "9.1.x-scala2.12",
    "node_type_id": "Standard_DS3_v2",
    "num_workers": 1,
    "spark_conf": {
        "spark.openlineage.version" : "v1",
        "spark.openlineage.host" : "https://$FUNNAME.azurewebsites.net",
        "spark.openlineage.url.param.code": "$FUNCTION_APP_DEFAULT_HOST_KEY"
    },
    "spark_env_vars": {
        "PYSPARK_PYTHON" : "/databricks/python3/bin/python3"
    },
    "autotermination_minutes": 15,
    "enable_elastic_disk": true,
    "cluster_source": "UI",
    "init_scripts": [
        {
            "dbfs":{
                "destination": "dbfs:/databricks/openlineage/open-lineage-init-script.sh"
            }
        }
    ],
    "libraries": [
        {
            "maven": {
                "coordinates": "com.microsoft.azure:spark-mssql-connector_2.12:1.2.0"
            }
        }
    ]
}
EOF
        curl -X POST https://$adb_ws_url/api/2.0/clusters/create "${adb_api_headers[@]}" -d @create-cluster.json

        # TODO post install config
        #  spark.openlineage.namespace <ADB-WORKSPACE-ID>#<DB_CLUSTER_ID>
    }

}

TODO-block() {

    ### TODO why we need below block?
    FUNCTION_APP_NAME=functionappqwvw.azurewebsites.net

    # You can see there are 2 keys created in same time. We pick the second one here
    ADLSKEY=$(az storage account keys list -g $rg -n $ADLSNAME --query '[1].value' --output tsv)
    samplestoragecontainer=rawdata
    az storage container create -n $samplestoragecontainer --account-name $ADLSNAME --account-key $ADLSKEY
    sampleA_resp=$(az storage blob upload --account-name $ADLSNAME --account-key $ADLSKEY -f exampleInputA.csv -c $samplestoragecontainer -n examples/data/csv/exampleInputA/exampleInputA.csv)
    sampleB_resp=$(az storage blob upload --account-name $ADLSNAME --account-key $ADLSKEY -f exampleInputB.csv -c $samplestoragecontainer -n examples/data/csv/exampleInputB/exampleInputB.csv)

}

$@
