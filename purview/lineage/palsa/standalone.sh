set -e

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
    az deployment group show --name $deploymentName --resource-group $rg $@
    # if failure, clean up by `az deployment group delete --name newdeploymenttemp --resource-group $rg`
}
deploy-env() {
    deploy-stats --query properties.outputs >stats.value.json
    export FUNNAME=$(jq -r '.functionAppName.value' stats.value.json)
    export KVNAME=$(jq -r '.kvName.value' stats.value.json)
    export ADLSNAME=$(jq -r '.storageAccountName.value' stats.value.json) # storageAccountName

    # You can see there are 2 keys created in same time. We pick the second one here
    adls_key=$(az storage account keys list -g $rg -n $ADLSNAME --query '[1].value' --output tsv)
    echo $adls_key
    export RGLOCATION=$purviewlocation # TODO clean this
    rm stats.value.json
}

# Install necessary types into your Purview instance
config-purview() {
    purview_endpoint="https://$purviewName.purview.azure.com"

    tenantid=$(curl https://raw.githubusercontent.com/davidkhala/azure-utils/refs/heads/main/cli/context.sh | bash -s tenant)

    local login_endpoint="https://login.microsoftonline.com/$tenantid/oauth2/token"
    acc_purview_token=$(curl $login_endpoint --data "resource=https://purview.azure.net&client_id=$clientid&client_secret=$clientsecret&grant_type=client_credentials" -H Metadata:true -s | jq -r '.access_token')

    # learnt from https://github.com/microsoft/Purview-ADB-Lineage-Solution-Accelerator/pull/235
    curl https://raw.githubusercontent.com/davidkhala/Microsoft/refs/heads/main/purview/lineage/palsa/Custom_Types.json -O

    curl -s -X POST $purview_endpoint/catalog/api/atlas/v2/types/typedefs -H "Authorization: Bearer $acc_purview_token" -H "Content-Type: application/json" -d @Custom_Types.json > config-purview-out.json
  
}
show-databricks(){
    # adb_details=$(az databricks workspace list --resource-group $RG_NAME)
}
config-databricks() {
    # TODO databricks part
    if ! unzip -v; then
        echo "unzip is required. Please find and install on your OS"
        exit 1
    fi

    if ! databricks -v; then
        # install DataBricks CLI
        curl -fsSL https://raw.githubusercontent.com/databricks/setup-cli/main/install.sh | sudo sh
    fi
}

TODO-block(){
    ### Download Jar File
curl -O -L https://repo1.maven.org/maven2/io/openlineage/openlineage-spark/0.18.0/openlineage-spark-0.18.0.jar
###
az storage container create -n rawdata --account-name $ADLSNAME --account-key $ADLSKEY
sampleA_resp=$(az storage blob upload --account-name $ADLSNAME --account-key $ADLSKEY -f exampleInputA.csv -c rawdata -n examples/data/csv/exampleInputA/exampleInputA.csv)
sampleB_resp=$(az storage blob upload --account-name $ADLSNAME --account-key $ADLSKEY -f exampleInputB.csv -c rawdata -n examples/data/csv/exampleInputB/exampleInputB.csv)

}

$@
