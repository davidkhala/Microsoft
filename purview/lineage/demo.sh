#!/bin/bash
set -e
rg=${rg:-"Purview-ADB-Lineage-Solution-Accelerator"} # resource_group

purviewlocation=SoutheastAsia
prefix=""

release=release/2.3

export subscription=$(curl https://raw.githubusercontent.com/davidkhala/azure-utils/refs/heads/main/cli/context.sh | bash -s subscription)
service_principal=${service_principal:-"Purview-ADB-Lineage-Solution-Accelerator"}
export tenantid=$(curl https://raw.githubusercontent.com/davidkhala/azure-utils/refs/heads/main/cli/context.sh | bash -s tenant)

credentialFile=".credential.json"

if ! [ -f $credentialFile ]; then
    # create service principal
    az ad sp create-for-rbac --name $1 --role Reader --scopes "/subscriptions/$subscription" --query "{appId:appId, password:password}" > $credentialFile
fi
export clientid=$(jq -r ".appId" $credentialFile) # Azure Service Principal client ID
    
export clientsecret=$(jq -r ".password" $credentialFile) # Azure Service Principal client secret


setup() {
    if ! az group exists --resource-group $rg; then
        az group create --location $purviewlocation --resource-group $rg
    fi

    if ! [ -d Purview-ADB-Lineage-Solution-Accelerator ]; then
        git clone https://github.com/microsoft/Purview-ADB-Lineage-Solution-Accelerator.git
    fi
    

    # you need to add the service principal to the data curator role in the Purview resource.
}
$@
