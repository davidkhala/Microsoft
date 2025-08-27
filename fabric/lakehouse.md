# Lakehouse

> The foundation of Microsoft Fabric
- built on top of **OneLake**
- >a collection of files, folders, tables, and shortcuts that act like a database over a data lake. 


# View of lakehouse

## *lake* view
supports data engineering and Apache Spark
- aka. **Lakehouse explorer** pane, **Lakehouse** experience
- View **Files**
## *SQL* view 
allows you to create views, functions, stored procedures and to apply SQL security and object level permissions.
- aka. **SQL analytics endpoint** experience, **Data explorer** pane
- similar to Databricks Warehouse `http_path`
- View **Tables**: enable Row-level security, column-level security, and dynamic data masking
  - similar to [granular warehouse permissions](./warehouse/security.md#data-protection-security-fine-grained-grant-access)


### Table
> Tables in Microsoft Fabric lakehouses are Delta tables

> New tables in the Lakehouse are automatically added to the **default semantic model**
