# [Microsoft Fabric](https://learn.microsoft.com/en-us/fabric/get-started/microsoft-fabric-overview)
> Fabric offers **persona-optimized** experiences and tools in an integrated user interface, without the need for access to Azure resources.
 
[portal](https://app.fabric.microsoft.com/)
- > Fabric administration is centralized in the [Admin portal](https://app.fabric.microsoft.com/admin-portal/tenantSettings).
- [portal: Help + Support](https://app.powerbi.com/admin-portal/supportCenter) is dedicated for Fabric.
  - You cannot use Azure portal to create/view service request

Fabric is a combination of workloads
- [PowerBI](https://github.com/davidkhala/power/tree/main/bi)
- Data factory: combining Power Query with the scale of Azure Data Factory
  - [Data pipelines](factory/pipeline/README.md)
- Industry Solutions: ?
- Real-Time Intelligence
  - new UI for classic Azure Stream Analytics 
- Synapse
  - Data Engineering: a Spark platform
  - Data Warehouse
  - Data Science: Azure Machine Learning + Spark
  - Real-Time Intelligence
     - https://blog.fabric.microsoft.com/en-in/blog/sense-analyze-and-generate-insights-with-synapse-real-time-analytics-in-microsoft-fabric?ft=05-2023:date

> Fabric is built on Power BI and Azure Data Lake Storage, with other capabilities included. 

Integrate with Purview by
- sensitivity labels
