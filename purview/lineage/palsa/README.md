# [Purview-ADB-Lineage-Solution-Accelerator (PALSA)](https://github.com/microsoft/Purview-ADB-Lineage-Solution-Accelerator)

Author: wijohns@microsoft.com
- https://github.com/wjohnson

## Deploy option 1: Build from scratch
```
git clone https://github.com/microsoft/Purview-ADB-Lineage-Solution-Accelerator.git
cd ./Purview-ADB-Lineage-Solution-Accelerator/deployment/infra/
rm ./settings.sh
curl https://raw.githubusercontent.com/davidkhala/Microsoft/refs/heads/main/purview/lineage/palsa/demo-context.sh | bash
chmod +x openlineage-deployment.sh
./openlineage-deployment.sh
cd -
```

## Deploy option 2: Connect with existing (all-purpose cluster)
0. Prequisite
    - Provision MS Purview and Azure Databricks (Premium tier is required for Unity Catalog)
    - Prepare Azure Databricks workspace name in terminal context, such as `export workspace_name=<e.g. az-databricks>`
    - Prepare `az` authentication. such as `az login --use-device-code` with Entra identity having `Global Administrator` role
    - Go to Databricks Account Console and set **Metastore Admin** with same Entra identity or group including it. e.g. `All account users`
1. Run `./standalone.sh deploy-connector`
2. Add the service principal `Purview-ADB-Lineage-Solution-Accelerator` to the `Data Curator` role in your Purview resource.
    - `Data Map` > `Domains` > select the Purview instance > `Role assignments`
3. Install necessary types into your Purview instance 
    ```
    `./standalone.sh config-purview`
    ```
4. Config your Azure Databricks WorkSpace
    - It validate installation of cli tools
        - Install `unzip`
        - Install `databricks` cli, and then authenticate the cli by Databricks personal access token (setup local connection profile)
        - Install databricks extension for `az` (Azure CLI)
    - It ship below materials into Databricks FS.
        - openlineage plugin (openlineage-spark-0.18.0.jar) once it's downloaded
        - `open-lineage-init-script.sh`
    - create new Databricks cluster        
    ```
    ./standalone.sh config-databricks <resource group of Azure Databricks workspace>
    ```
### Extend support extracting Lineage from Databricks 'Job cluster'
0. Prepare `.credential.json` locally or `export appId=<of service principal>`. (e.g. find appId in MS Entra admin center service principal `Purview-ADB-Lineage-Solution-Accelerator`)
1. Run `./standalone.sh config-job-compute`
2. Assign the service principal as a `Contributor` to the Databricks Workspace