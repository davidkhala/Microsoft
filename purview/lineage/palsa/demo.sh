#!/bin/bash
set -e
export rg=${rg:-"Purview-ADB-Lineage-Solution-Accelerator"} # resource_group

export purviewlocation=SoutheastAsia
export prefix=""

release=release/2.3

export tenantid=$(curl https://raw.githubusercontent.com/davidkhala/azure-utils/refs/heads/main/cli/context.sh | bash -s tenant)

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
