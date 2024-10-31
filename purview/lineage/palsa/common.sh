
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
    az ad sp create-for-rbac --name $service_principal --role Reader --scopes "/subscriptions/$subscription" --query "{appId:appId, password:password}" > $credentialFile
fi

