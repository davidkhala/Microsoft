[In a sample data lifecycle](https://learn.microsoft.com/en-us/purview/governance-roles-permissions#data-asset-lifecycle-example)

[In a sample data project planning](https://learn.microsoft.com/en-us/purview/data-catalog-get-started#reference-model-for-planning)

# [External](https://learn.microsoft.com/en-us/purview/manage-credentials)
As soon as the Microsoft Purview Account is created, a system-assigned managed identity (SAMI) is created automatically in Microsoft Entra tenant.

## Azure Subscription

You can assign Purview's SAMI to Azure Subscription level `Access Control (IAM)`

## [Microsoft Fabric](https://learn.microsoft.com/en-us/purview/register-scan-fabric-tenant)
1. Create/Identify a group in Entra with 
    - **Group type**: `Security`
    - **Group name**: `Fabric Connect` or another arbitrary name
2. Adding Purview's SAMI into this group `Fabric Connect` as **Member**
    - Adding it as **Owner** is not allowed. It will introduce error in *Test connection*： `Exception when processing request: ErrorCode:(3871) UserErrorDataScanPowerBIBasicMetadataFailure.`
3. Go to [tenant settings page of Fabric portal](https://app.fabric.microsoft.com/admin-portal/tenantSettings)
4. Select **Admin API settings** > **Service principals can access read-only admin APIs**, type in `Fabric Connect` and click [Apply]
5. Similarly, Enable **Admin API settings** > **Enhance admin APIs responses with detailed metadata** for the entire organization
6. Similarly, Enable **Admin API settings** > **Enhance admin APIs responses with DAX and mashup expressions** for the entire organization
7. Wait around 15 minutes before registering a scan and test connection (after you update above settings)


## Azure SQL DB
[additional SQL steps](https://learn.microsoft.com/en-us/purview/register-scan-azure-sql-database?tabs=managed-identity)
- option 1: In Azure SQL DB server level, Go to **Settings/Microsoft Entra ID** and switch current **Microsoft Entra admin** to the SAMI.
  - This is **not recommend**, but a quick workaround
- option 2: Create SAMI as DB user in Azure SQL
  > The Microsoft Entra admin is the only user who can initially create other Microsoft Entra users in SQL Database
  - Run [setup.sql](./mssql/setup.sql) 
  - To clean up
    1. In SSMS, go to `Databases` > [database] > `Extended Events` > `Sessions`, stop and delete Purview session first
    2. Run [clean.sql](./mssql/clean.sql) 
  - Microsoft Entra admin of this Azure SQL Server is required as executor for running these 2 above 
    
## Azure Databricks
It requires
- **Credential**, supported by Purview Vault 
  - Purview's SAMI should have access to write secret in Azure KeyVault.
  - https://github.com/davidkhala/azure-utils/tree/main/vault#permission
- **HTTP Path** of SQL warehouse

### Azure Databricks Unity Catalog
It requires
- **Workspace URL** (e.g. `adb-2367537008441771.11.azuredatabricks.net` )
- **HTTP Path** of SQL warehouse



# Internal
## Data Catelog: Roles and permissions
- Data Governance Administrators
- Governance Domain Creator
  - It includes view access to Governance domains: `Microsoft.Purview/datagovernance/businessdomain/read`
- Data Health Owners
- Data Health Readers


