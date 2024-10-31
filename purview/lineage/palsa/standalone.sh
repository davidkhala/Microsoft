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
    # if failure, clean up by `az deployment group delete --name newdeploymenttemp --resource-group $rg`
    rm newdeploymenttemp.json
    
}

deploy-stats() {
    az deployment group show --name $deploymentName --resource-group $rg
}

# Install necessary types into your Purview instance
config-purview() {
    purview_endpoint="https://$purviewName.purview.azure.com"

    tenantid=$(curl https://raw.githubusercontent.com/davidkhala/azure-utils/refs/heads/main/cli/context.sh | bash -s tenant)

    local login_endpoint="https://login.microsoftonline.com/$tenantid/oauth2/token"
    acc_purview_token=$(curl $login_endpoint --data "resource=https://purview.azure.net&client_id=$clientid&client_secret=$clientsecret&grant_type=client_credentials" -H Metadata:true -s | jq -r '.access_token')

    curl https://raw.githubusercontent.com/microsoft/Purview-ADB-Lineage-Solution-Accelerator/refs/heads/release/2.3/deployment/infra/Custom_Types.json -O

    curl -s -X POST $purview_endpoint/catalog/api/atlas/v2/types/typedefs -H "Authorization: Bearer $acc_purview_token" -H "Content-Type: application/json" -d @Custom_Types.json
    # TODO troubleshoot error
    # {"requestId":"d1fb3a39-9016-44c0-9a7a-8164419d4188","errorCode":"ATLAS-400-00-01A","errorMessage":"invalid parameters: invalid payload, expect schemaAttributes in purview_custom_connector_generic_column should be list of string, but found: data_type"}
    rm Custom_Types.json
}

# TODO databricks part
if ! unzip -v; then
    echo "unzip is required. Please find and install on your OS"
    exit 1
fi

if ! databricks -v; then
    # install DataBricks CLI
    curl -fsSL https://raw.githubusercontent.com/databricks/setup-cli/main/install.sh | sudo sh
fi
# TODO databricks part
$@
