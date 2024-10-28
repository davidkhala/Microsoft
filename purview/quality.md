# Controls
Not ready to calculate score?
![image](https://github.com/user-attachments/assets/70d4133f-ce72-4dff-8782-f11c6db20916)


# Data Quality

## Role 
Data Quality Steward role
- To create and manage data quality rules

Data Quality Reader role
- To view existing quality rules


## Rule
[view rules](https://learn.microsoft.com/en-us/purview/concepts-data-quality-rules#view-existing-data-quality-rules)



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

