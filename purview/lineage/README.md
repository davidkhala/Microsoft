# Lineage


## Azure Databricks
- Purview目前只支持Table/View的lineage。Volume类型是不支持的。
  - There will not be lineage data if a notebook load CSV from Volume data
- enable system schema `system.access` by [run script](https://github.com/davidkhala/databricks-common/blob/main/cli/lineage.sh)
  - > Error: Only account admins can enable system schemas
    - You need to assign `Account admin` role to user in Databricks **Account Console** > **User management**
  

## Azure SQL DB
> Failed to AddOrUpdate lineage scan for <scan-name>: The current database for lineage scan is read-only. Please update with a writeable database.
- You cannot scan on a standby database in Geo Replica

## [Microsoft Fabric](https://learn.microsoft.com/en-us/purview/how-to-lineage-fabric)
1. Select `Data Catelog` > `Discovery` > `Data assets`
2. Choose tile 'Microsoft Fabric', then tile `Fabric workspaces`
3. Select the **item name** of workspace
4. Switch to cases

### Case: PowerBI

Report
- When editing lineage (mannual lineage) for PowerBI Report, it is limited to table level.
  > Unable to map columns for this asset. The asset doesn't have a schema.

Dataset
> Manual lineage reporting is not supported for this asset type.
- automated lineage 
  - [Supported source for table level lineage](https://learn.microsoft.com/en-us/purview/how-to-lineage-powerbi#lineage-of-power-bi-artifacts-in-microsoft-purview)
    - Azure SQL Database
    - Azure Blob Storage
    - Azure Data Lake Store (Gen1 & Gen2)
  - Supported source for column level lineage and transformations (except for Dataflows)
    - Azure SQL Database
