
rg=${rg:-"Purview-ADB-Lineage-Solution-Accelerator"} # resource_group
purviewlocation=SoutheastAsia
if ! az group exists --resource-group $rg; then
        az group create --location $purviewlocation --resource-group $rg
fi


