rg=${rg:-"Purview-ADB-Lineage-Solution-Accelerator"} # resource_group
export purviewlocation=SoutheastAsia
if ! az group exists --resource-group $rg; then
    az group create --location $purviewlocation --resource-group $rg
fi

credentialFile=".credential.json"

if ! [ -f $credentialFile ]; then
    # create service principal
    service_principal=${service_principal:-"Purview-ADB-Lineage-Solution-Accelerator"}
    export subscription=$(curl https://raw.githubusercontent.com/davidkhala/azure-utils/refs/heads/main/cli/context.sh | bash -s subscription)
    curl https://raw.githubusercontent.com/davidkhala/azure-utils/refs/heads/main/cli/entra.sh | bash -s create-service-principal $service_principal >$credentialFile

fi

export clientid=$(jq -r ".appId" $credentialFile)
export clientsecret=$(jq -r ".password" $credentialFile)
export rg=$rg
