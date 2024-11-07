# Lineage

## [mannual lineage](https://learn.microsoft.com/en-us/purview/catalog-lineage-user-guide#manual-lineage)
- > When you add lineage between two data assets, you can additionally configure the column level lineage.
  - prerequisite: Both current or upstream/downstream data asset should have a schema 
  - > These asset types don't currently allow manual lineage because they support automated lineage:
    - Azure Data Factory
    - Synapse pipelines
    - Power BI datasets
    - Teradata stored procedure
    - Azure SQL stored procedure
    ![image](https://github.com/user-attachments/assets/43e74e6d-cfbd-486b-976f-ce3fa5641900)


## Azure Databricks
- 我在Purview目前只支持Table/View的lineage。Volume类型是不支持的。
  - There will not be lineage data if a notebook load CSV from Volume data

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
- [Supported source for table level lineage](https://learn.microsoft.com/en-us/purview/how-to-lineage-powerbi#lineage-of-power-bi-artifacts-in-microsoft-purview)
  - Azure SQL Database
  - Azure Blob Storage
  - Azure Data Lake Store (Gen1 & Gen2)
- Supported source for column level lineage and transformations (except for Dataflows)
  - Azure SQL Database
