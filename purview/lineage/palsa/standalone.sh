set -e

if ! [ -f ./common.sh ]; then
    curl -s https://raw.githubusercontent.com/davidkhala/Microsoft/refs/heads/main/purview/lineage/palsa/common.sh -O
    source ./common.sh
    rm ./common.sh
else
    source ./common.sh
fi

purviewName=$(curl -s https://raw.githubusercontent.com/davidkhala/azure-utils/refs/heads/main/cli/purview.sh | bash -s name)

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
login() {
    local adb_rg=${1:-$rg} # The Resource Group of Azure Databricks
    export workspace_name=${2:-"az-databricks"}
    local global_adb_token=$(curl -s https://raw.githubusercontent.com/davidkhala/azure-utils/refs/heads/main/cli/databricks.sh | bash -s get-access-token)

    adb_ws_url=$(az databricks workspace show --resource-group $adb_rg --name $workspace_name --query workspaceUrl -o tsv)
    databricks configure --token --host https://$adb_ws_url <<<$global_adb_token
    echo $adb_ws_url
}
config-databricks() {
    # software prequisite block

    if ! databricks -v; then
        if ! unzip -v >/dev/null; then
            echo "unzip is required. Please find and install on your OS"
            exit 1
        fi
        # install DataBricks CLI
        curl -fsSL https://raw.githubusercontent.com/databricks/setup-cli/main/install.sh | sudo sh
    fi
    echo y | az databricks -h >/dev/null

    export workspace_name=${2:-"az-databricks"}

    adb_ws_url=$(login $@)

    local adb_ws_url_id=$(sed 's/.azuredatabricks.net//g' <<<$adb_ws_url) # ADB-WORKSPACE-ID e.g. `adb-2525538437753513.13`

    # manipulate Unity Catalog volumes

    # create volume
    volume=openlineage-volume
    export schema=${schema:-default}
    export catalog=${catalog:-$(sed 's/-/_/' <<<$workspace_name)}
    curl https://raw.githubusercontent.com/davidkhala/spark/refs/heads/main/databricks/cli/ucv.sh | bash -s create-managed $volume

    STAGE_DIR=/Volumes/$catalog/$schema/$volume

    # dbfs cp ./openlineage-spark-*.jar

    curl -O -L https://repo1.maven.org/maven2/io/openlineage/openlineage-spark/0.18.0/openlineage-spark-0.18.0.jar
    databricks fs cp --overwrite ./openlineage-spark-0.18.0.jar dbfs:$STAGE_DIR/
    rm ./openlineage-spark-0.18.0.jar

    # dbfs cp --overwrite ./open-lineage-init-script.sh

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
    databricks fs cp --overwrite ./open-lineage-init-script.sh dbfs:$STAGE_DIR/open-lineage-init-script.sh
    rm ./open-lineage-init-script.sh
    allow $STAGE_DIR

    cluster_name="openlineage" # name of compute cluster within Databricks
    if [[ -f stats.value.json ]]; then
        FUNNAME=$(jq -r '.functionAppName.value' stats.value.json)
    else
        FUNNAME=functionappqwvw
    fi
    az functionapp show --name $FUNNAME --resource-group $rg >/dev/null # existence check
    local FUNCTION_APP_DEFAULT_HOST_KEY=$(az functionapp keys list --resource-group $rg --name $FUNNAME --query functionKeys.default -o tsv)

    # json for cluster configuration
    cat <<EOF >create-cluster.json
{
    "cluster_name": "$cluster_name",
    "spark_version": "15.4.x-scala2.12",
    "node_type_id": "Standard_DS3_v2",
    "num_workers": 1,
    "spark_conf": {
        "spark.openlineage.version": "v1",
        "spark.openlineage.host": "https://$FUNNAME.azurewebsites.net",
        "spark.openlineage.url.param.code": "$FUNCTION_APP_DEFAULT_HOST_KEY"
    },
    "spark_env_vars": {
        "PYSPARK_PYTHON" : "/databricks/python3/bin/python3"
    },
    "data_security_mode":"USER_ISOLATION",
    "autotermination_minutes": 10,
    "enable_elastic_disk": true,
    "init_scripts": [
        {
            "volumes":{
                "destination": "$STAGE_DIR/open-lineage-init-script.sh"
            }
        }
    ]
}
EOF
    databricks clusters create --json @create-cluster.json >cluster_info.json
    rm create-cluster.json
    cluster_id=$(jq -r .cluster_id cluster_info.json)
    rm cluster_info.json
    # editing cluster
    databricks libraries install --json "{\"cluster_id\":\"$cluster_id\", \"libraries\":[{\"maven\": {\"coordinates\": \"com.microsoft.azure:spark-mssql-connector_2.12:1.2.0\"}}]}"

    databricks clusters update --json "{\"cluster_id\":\"$cluster_id\",\"cluster\":{\"spark_conf\":{\"spark.openlineage.namespace\":\"$adb_ws_url_id#$cluster_id\" }},\"update_mask\":\"spark_conf\" }"

}
allow() {
    local STAGE_DIR=${1:-"/Volumes/az_databricks/default/openlineage-volume"}
    curl -s https://raw.githubusercontent.com/davidkhala/spark/refs/heads/main/databricks/cli/uc.sh -O
    chmod +x uc.sh
    ./uc.sh allow-script $STAGE_DIR/open-lineage-init-script.sh >/dev/null
    ./uc.sh allow-jar $STAGE_DIR/openlineage-spark-0.18.0.jar >/dev/null
    ./uc.sh allow-maven com.microsoft.azure:spark-mssql-connector_2.12:1.2.0 >/dev/null
    rm uc.sh
}
config-job-compute() {
    if [[ -f .credential.json ]]; then
        appId=$(jq -r .appId .credential.json)
    fi
    if [[ -z $appId ]]; then
        echo "missing appId of service_principal (Azure)"
        exit 1
    fi

    service_principal=${service_principal:-"Purview-ADB-Lineage-Solution-Accelerator"}
    # curl -s https://raw.githubusercontent.com/davidkhala/spark/refs/heads/main/databricks/cli/user.sh -O
    chmod +x user.sh
    local adminsGroupId=$(./user.sh admins)
    ./user.sh create-service-principal $service_principal --application-id $appId --json "{\"groups\":[{\"value\":\"$adminsGroupId\"}],\"entitlements\":[{\"value\":\"allow-cluster-create\"}]}"

    rm user.sh

}
$@
