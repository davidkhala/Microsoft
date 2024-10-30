#!/bin/bash
set -e
export rg=${rg:-"Purview-ADB-Lineage-Solution-Accelerator"} # resource_group
if ! az group exists --resource-group $rg; then
        az group create --location $purviewlocation --resource-group $rg
fi

export purviewlocation=SoutheastAsia
export prefix=""

export tenantid=$(curl https://raw.githubusercontent.com/davidkhala/azure-utils/refs/heads/main/cli/context.sh | bash -s tenant)


service_principal=${service_principal:-"Purview-ADB-Lineage-Solution-Accelerator"}
subscription=$(curl https://raw.githubusercontent.com/davidkhala/azure-utils/refs/heads/main/cli/context.sh | bash -s subscription)
credentialFile=".credential.json"

if ! [ -f $credentialFile ]; then
    # create service principal
    az ad sp create-for-rbac --name $service_principal --role Reader --scopes "/subscriptions/$subscription" --query "{appId:appId, password:password}" > $credentialFile
fi
export clientid=$(jq -r ".appId" $credentialFile) # Azure Service Principal client ID
    
export clientsecret=$(jq -r ".password" $credentialFile) # Azure Service Principal client secret
