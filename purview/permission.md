[In a sample data lifecycle](https://learn.microsoft.com/en-us/purview/governance-roles-permissions#data-asset-lifecycle-example)


# Scan
> [Before you set up your scan, you must give the managed identity of the Microsoft Purview account permissions to enumerate your Azure subscription.](https://learn.microsoft.com/en-us/purview/manage-credentials?wt.mc_id=mspurview_inproduct_scan_msiauth_csadai)
- As soon as the Microsoft Purview Account is created, a system-assigned managed identity (SAMI) is created automatically in Microsoft Entra tenant. This SAMI is visible under **Enterprise App** in Entra
- It positions like a service account.
- You still need to assign access to Azure resource to this SAMI one by one
  - [configure storage acount](https://learn.microsoft.com/en-us/purview/register-scan-azure-blob-storage-source#authentication-for-a-scan)