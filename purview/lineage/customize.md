![](https://learn.microsoft.com/en-us/purview/media/how-to-custom-lineage-api/lineage-larger.png)
# [Mannual lineage](https://learn.microsoft.com/en-us/purview/catalog-lineage-user-guide#manual-lineage)
- > When you add lineage between two data assets, you can additionally configure the column level lineage.
  - prerequisite: Both current or upstream/downstream data asset should have a schema 
- > These asset types don't currently allow manual lineage because they support automated lineage:
  - Azure Data Factory
  - Synapse pipelines
  - Power BI datasets
  - Teradata stored procedure
  - Azure SQL stored procedure
  ![image](https://github.com/user-attachments/assets/43e74e6d-cfbd-486b-976f-ce3fa5641900)
  - Solution: when manual lineage is not supported, customizing lineage via Purview API is still allowed  

# [Customized lineage](https://learn.microsoft.com/en-us/purview/legacy/how-to-purview-custom-lineage-api-user-guide)
![image](https://github.com/user-attachments/assets/3af22fea-feaa-4dbd-ae23-4abc06305318)


![Databricks publish to PowerBI](https://github.com/user-attachments/assets/5c6d5486-57d5-4f74-a354-c5e8a445529b)