set -e
if ! [ -f ./common.sh ]; then
    curl https://raw.githubusercontent.com/davidkhala/Microsoft/refs/heads/main/purview/lineage/palsa/common.sh -O
    source ./common.sh
    rm ./common.sh
else
    source ./common.sh
fi

if ! unzip -v; then
    echo "unzip is required. Please find and install on your OS"
    exit 1
fi

if ! databricks -v; then
    # install DataBricks CLI
    curl -fsSL https://raw.githubusercontent.com/databricks/setup-cli/main/install.sh | sudo sh
fi

rg=${rg:-"Purview-ADB-Lineage-Solution-Accelerator"}
purviewName=$(curl https://raw.githubusercontent.com/davidkhala/azure-utils/refs/heads/main/cli/purview.sh | bash -s name)

# DEBUG
curl https://raw.githubusercontent.com/microsoft/Purview-ADB-Lineage-Solution-Accelerator/refs/heads/release/2.3/deployment/infra/newdeploymenttemp.json -O

az deployment group create --resource-group $rg --template-file "./newdeploymenttemp.json" --parameters purviewName=$purviewName prefixName= clientid=$clientid clientsecret=$clientsecret resourceTagValues={} --output none
# if failure, clean up by `az deployment group delete --name newdeploymenttemp --resource-group $rg`
rm newdeploymenttemp.json
