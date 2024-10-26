# Data Quality
https://learn.microsoft.com/en-us/purview/section4-run-dq#prerequisites
> Data quality rules can only be run on delta format tables in ADLS Gen2 and Microsoft Fabric.

This is not right now (Oct 2024)  
![image](https://github.com/user-attachments/assets/8c65b923-8edc-48f4-adce-b5a2d08abd37)

> Only using SAMI from Purview to read data source is supported credential method 

Data quality will use seperate `Connection` in a governance domain than reuse connection in data scan
> [Building this connection to run data quality scans on your data source in that governance domain](https://learn.microsoft.com/en-us/purview/section4-run-dq#create-and-run-data-quality-rules)
