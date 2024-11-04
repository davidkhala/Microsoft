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
2. Adding Purview's SAMI into this group `Fabric Connect`
3. Go to [tenant settings page of Fabric portal](https://app.fabric.microsoft.com/admin-portal/tenantSettings)
4. Select **Admin API settings** > **Service principals can access read-only admin APIs**, type in `Fabric Connect` and click [Apply]
5. Similarly, Enable **Admin API settings** > **Enhance admin APIs responses with detailed metadata** for the entire organization
6. Similarly, Enable **Admin API settings** > **Enhance admin APIs responses with DAX and mashup expressions** for the entire organization
7. Wait around 15 minutes before registering a scan and test connection (after you update above settings)


## Azure SQL DB
[additional SQL steps](https://learn.microsoft.com/en-us/purview/register-scan-azure-sql-database?tabs=managed-identity)
- option 1: In Azure SQL DB server level, Go to **Settings/Microsoft Entra ID** and switch current **Microsoft Entra admin** to the SAMI.
  - This is **not recommend**, but a quick workaround
- option 2: Create SAMI as DB user in Azure SQL DB by running below as **Microsoft Entra User**
  > The Microsoft Entra admin is the only user who can initially create other Microsoft Entra users in SQL Database
  
  ```
  -- A good SQL runtime is **Query Editor** in Azure SQL DB db level
  CREATE USER "[SAMI name]" FROM EXTERNAL PROVIDER
  GO

  EXEC sp_addrolemember 'db_owner', "[SAMI name]"
  GO

  CREATE MASTER KEY
  GO
  ```
## Azure Databricks
Beyond IAM, You need to further grant **Access policies** (in the same left panel) of Key Vault to Purview's SAMI

# Internal
## Data Catelog: Roles and permissions
- Data Governance Administrators
- Governance Domain Creator
  - It includes view access to Governance domains: `Microsoft.Purview/datagovernance/businessdomain/read`
- Data Health Owners
- Data Health Readers


