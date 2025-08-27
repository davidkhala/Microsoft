OneLake is the OneDrive for data
- > Similar to how Office applications are prewired to use your organizational OneDrive

> all your data stored in a single open format in **OneLake**
- built on top of Azure Data Lake Storage (ADLS)
- all of the compute engines in Fabric automatically store their data in OneLake
- Default storage format: `Delta Parquet`
# OneCopy
> OneCopy allows you to read data from a single copy, without moving or duplicating data.

**Shortcuts** allow you to quickly source your existing cloud data without having to copy it
- target: ADLS Gen2, OneLake
# Permission

## OneLake data access roles
- aka. OneLake RBAC