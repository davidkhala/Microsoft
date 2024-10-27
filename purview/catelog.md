# Governance Domain

Governance Domain organizes data products into meaningful groups and link them to business concepts
- Data product: only focus on **gold** layer in medallion architecture
- groups and link: no new computation components introduced. It is just an administrative tagging system.

Governance Domain is seperate from Data Map solution
- It has its own Data Quality Scan than Data Source Scan in Data Map. But the former can reuse later's connection information




### Type: an extra descriptor. No impact to choose any
- Functional unit: organizations or business units such as Sales, Marketing, or Finance
- Line of business: products or services being sold such as Xbox, Office, or Azure and different markets or subsidiaries
- Data domain : key organization-wide entities such as customers or employees
- Regulatory: compliance related such as GDPR, SOX, or HIPPA
- Project: **general purpose** collaborative programs across the organization


## Refs
[Tutorial to setup](https://learn.microsoft.com/en-us/purview/section1-setup-your-governance-domain)
- [based on CDC COVID-19 dataset](https://github.com/davidkhala/datasets/tree/main/SQL/covid-19)
