# Controls
Controls evaluate health of their data estate from the lens of industry recognized standards.
- Target user: Data Stewards and CDO 


# Data Quality

## Role 
Data Quality Steward role
- To create and manage data quality rules

Data Quality Reader role
- To view existing quality rules


## Rule
[view rules](https://learn.microsoft.com/en-us/purview/concepts-data-quality-rules#view-existing-data-quality-rules)



## Scan
[View data quality scan status](https://learn.microsoft.com/en-us/purview/how-to-data-quality-job-monitoring#browse-data-quality-job-status)

> [Data Quality scan会检查Purview以及Data source的区域，目前只有Southeast Asia 是支持的，East Asia还不支持。](https://learn.microsoft.com/en-us/purview/data-catalog-regions)

### Rule type
- Accuracy - Data should accurately represent real-world entities. Context matters! For example, if you’re storing customer addresses, ensure they match the actual locations. ??
- Completeness
  - Should have no empty, null, or missing data. 
- Conformity
  - Data should align to data format, such as representation of dates, addresses, and allowed values.
- Consistency
  - Same information should be the same across different records
- Timeliness
  - Data is up to date.
- Uniqueness
  - No duplicated value. 


### DSL: Microsoft Purview Data Quality expression language.
Not found in internet




## Outdated docs
https://learn.microsoft.com/en-us/purview/section4-run-dq#prerequisites
> Data quality rules can only be run on delta format tables in ADLS Gen2 and Microsoft Fabric.

This is not right now (Oct 2024)  
![image](https://github.com/user-attachments/assets/8c65b923-8edc-48f4-adce-b5a2d08abd37)

> Only using SAMI from Purview to read data source is supported credential method 

Data quality can reuse `Connection` in Data Map

