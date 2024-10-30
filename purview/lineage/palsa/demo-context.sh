#!/bin/bash
set -e
rg=${rg:-"Purview-ADB-Lineage-Solution-Accelerator"} # resource_group
purviewlocation=SoutheastAsia
if ! az group exists --resource-group $rg; then
        az group create --location $purviewlocation --resource-group $rg
fi

service_principal=${service_principal:-"Purview-ADB-Lineage-Solution-Accelerator"}
subscription=$(curl https://raw.githubusercontent.com/davidkhala/azure-utils/refs/heads/main/cli/context.sh | bash -s subscription)
credentialFile=".credential.json"

if ! [ -f $credentialFile ]; then
    # create service principal
    az ad sp create-for-rbac --name $service_principal --role Reader --scopes "/subscriptions/$subscription" --query "{appId:appId, password:password}" > $credentialFile
fi

echo "export rg=$rg" > settings.sh
echo "export purviewlocation=$purviewlocation" > settings.sh
echo "export prefix=\"\"" > settings.sh

echo "export tenantid=$(curl https://raw.githubusercontent.com/davidkhala/azure-utils/refs/heads/main/cli/context.sh | bash -s tenant)" > settings.sh

echo "export clientid=$(jq -r ".appId" $credentialFile)" > settings.sh # Azure Service Principal secret ID

echo "export clientsecret=$(jq -r ".password" $credentialFile)" > settings.sh # Azure Service Principal secret value