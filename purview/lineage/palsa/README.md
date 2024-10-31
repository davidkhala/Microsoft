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

## Deploy option 2: Connect with existing
0. Provision MS Purview and Azure Databricks
1. Run `./standalone.sh deploy-connector`
2. Add the service principal `Purview-ADB-Lineage-Solution-Accelerator` to the `Data Curator` role in your Purview resource.
    - `Data Map` > `Domains` > select the Purview instance > `Role assignments`
3. Install necessary types into your Purview instance 
    ```
    `./standalone.sh config-purview`
    ```
4. TODO 
https://github.com/microsoft/Purview-ADB-Lineage-Solution-Accelerator/blob/release/2.3/deploy-base.md#download-the-openlineage-spark-agent-and-configure-with-your-azure-databricks-clusters