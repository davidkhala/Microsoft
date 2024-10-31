
export rg=${rg:-"Purview-ADB-Lineage-Solution-Accelerator"} # resource_group
export purviewlocation=SoutheastAsia
if ! az group exists --resource-group $rg; then
        az group create --location $purviewlocation --resource-group $rg
fi

service_principal=${service_principal:-"Purview-ADB-Lineage-Solution-Accelerator"}
subscription=$(curl https://raw.githubusercontent.com/davidkhala/azure-utils/refs/heads/main/cli/context.sh | bash -s subscription)
credentialFile=".credential.json"

if ! [ -f $credentialFile ]; then
    # create service principal
    curl https://raw.githubusercontent.com/davidkhala/azure-utils/refs/heads/main/cli/entra.sh | bash -s create-service-principal $service_principal > $credentialFile 
    
fi

