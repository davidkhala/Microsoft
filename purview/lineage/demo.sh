#!/bin/bash
set -e
rg=${rg:-"Purview-ADB-Lineage-Solution-Accelerator"} # resource_group
region=SoutheastAsia                                 # take care of purview
purviewlocation=$region
prefix=""

release=release/2.3

service_principal=${service_principal:-"Purview-ADB-Lineage-Solution-Accelerator"}
create-service-principal() {
    export subscription=$(curl https://raw.githubusercontent.com/davidkhala/azure-utils/refs/heads/main/cli/context.sh | bash -s subscription)
    
    curl https://raw.githubusercontent.com/davidkhala/azure-utils/refs/heads/main/cli/entra.sh | bash -s create-service-principal $service_principal | > credential.json
    export clientsecret=$(jq -r ".password" credential.json)
    export clientid=$(jq -r ".appId" credential.json)
    rm credential.json

}
clientid="<CLIENT_ID>"         # Azure Service Principal client ID
clientsecret="<CLIENT_SECRET>" # Azure Service Principal client secret
tenantid="<TENANT_ID>"

setup() {
    if ! az group exists --resource-group $rg; then
        az group create --location $region --resource-group $rg
    fi

    git clone https://github.com/microsoft/Purview-ADB-Lineage-Solution-Accelerator.git

    # you need to add the service principal to the data curator role in the Purview resource.
}
$@
