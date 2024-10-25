[In a sample data lifecycle](https://learn.microsoft.com/en-us/purview/governance-roles-permissions#data-asset-lifecycle-example)




# External
## Scan
> [Before you set up your scan, you must give the managed identity of the Microsoft Purview account permissions to enumerate your Azure subscription.](https://learn.microsoft.com/en-us/purview/manage-credentials)
- As soon as the Microsoft Purview Account is created, a system-assigned managed identity (SAMI) is created automatically in Microsoft Entra tenant.
- You can assign Purview's SAMI to Azure Subscription level `Access Control (IAM)`

### Exception: Azure SQL DB
[additional SQL steps](https://learn.microsoft.com/en-us/purview/register-scan-azure-sql-database?tabs=managed-identity)
- option 1: In Azure SQL DB server level, Go to **Settings/Microsoft Entra ID** and switch current **Microsoft Entra admin** to the SAMI.
  - This is **not recommend**, but a quick workaround
- option 2: Create SAMI as DB user in Azure SQL DB by running below as **Microsoft Entra User**
  > The Microsoft Entra admin is the only user who can initially create other Microsoft Entra users in SQL Database
  
  ```
  # A good SQL runtime is **Query Editor** in Azure SQL DB db level
  CREATE USER "[SAMI name]" FROM EXTERNAL PROVIDER
  GO

  EXEC sp_addrolemember 'db_datareader', "[SAMI name]"
  GO
  ```

# Internal
## Data Catelog: Roles and permissions
- Data Governance Administrators
- Governance Domain Creator
  - It includes view access to Governance domains: `Microsoft.Purview/datagovernance/businessdomain/read`
- Data Health Owners
- Data Health Readers


