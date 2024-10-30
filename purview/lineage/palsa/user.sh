subscription=$(curl https://raw.githubusercontent.com/davidkhala/azure-utils/refs/heads/main/cli/context.sh | bash -s subscription)
service_principal=${service_principal:-"Purview-ADB-Lineage-Solution-Accelerator"}

credentialFile=".credential.json"

if ! [ -f $credentialFile ]; then
    # create service principal
    az ad sp create-for-rbac --name $service_principal --role Reader --scopes "/subscriptions/$subscription" --query "{appId:appId, password:password}" > $credentialFile
fi
export clientid=$(jq -r ".appId" $credentialFile) # Azure Service Principal client ID
    
export clientsecret=$(jq -r ".password" $credentialFile) # Azure Service Principal client secret