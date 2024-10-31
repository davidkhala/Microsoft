rg=${rg:-"Purview-ADB-Lineage-Solution-Accelerator"}
purviewName=$(curl https://raw.githubusercontent.com/davidkhala/azure-utils/refs/heads/main/cli/purview.sh | bash -s name)
az deployment group create --resource-group $rg --template-file "./Purview-ADB-Lineage-Solution-Accelerator/deployment/infra/newdeploymenttemp.json" --parameters purviewName=$purviewName
