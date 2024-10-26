# Data Quality
https://learn.microsoft.com/en-us/purview/section4-run-dq#prerequisites
> Data quality rules can only be run on delta format tables in ADLS Gen2 and Microsoft Fabric.  
> Only using SAMI from Purview to read data source is supported credential method 

Data quality will use seperate `Connection` in a governance domain than reuse connection in data scan
> [Building this connection to run data quality scans on your data source in that governance domain](https://learn.microsoft.com/en-us/purview/section4-run-dq#create-and-run-data-quality-rules)
