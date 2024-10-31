#!/bin/bash
set -e
az config set extension.dynamic_install_allow_preview=true

curl https://raw.githubusercontent.com/davidkhala/Microsoft/refs/heads/main/purview/lineage/palsa/common.sh -O
source ./common.sh
rm ./common.sh

echo "export rg=$rg" > settings.sh
echo "export purviewlocation=$purviewlocation" > settings.sh
echo "export prefix=\"\"" > settings.sh

echo "export tenantid=$(curl https://raw.githubusercontent.com/davidkhala/azure-utils/refs/heads/main/cli/context.sh | bash -s tenant)" > settings.sh

echo "export clientid=$clientid" > settings.sh # Azure Service Principal secret ID

echo "export clientsecret=$clientsecret" > settings.sh # Azure Service Principal secret value
