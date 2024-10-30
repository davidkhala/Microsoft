#!/bin/bash
set -e
export rg=${rg:-"Purview-ADB-Lineage-Solution-Accelerator"} # resource_group
if ! az group exists --resource-group $rg; then
        az group create --location $purviewlocation --resource-group $rg
fi

export purviewlocation=SoutheastAsia
export prefix=""

export tenantid=$(curl https://raw.githubusercontent.com/davidkhala/azure-utils/refs/heads/main/cli/context.sh | bash -s tenant)

