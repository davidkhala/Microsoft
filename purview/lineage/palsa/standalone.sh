rg=${rg:-"Purview-ADB-Lineage-Solution-Accelerator"}
purviewName=# TODO get
az deployment group create --resource-group $rg --template-file "./Purview-ADB-Lineage-Solution-Accelerator/deployment/infra/newdeploymenttemp.json" --parameters purviewName=<ExistingPurviewServiceName>
