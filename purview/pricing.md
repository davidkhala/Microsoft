# Account type: Enterprise

Platform size is measured by capacity unit (min: 1)
- $0.411 per capacity unit per hour
- 1 capacity unit includes 10 GB metadata storage and 25 operations per sec.

# Account Type: Free
[Tier compare](https://learn.microsoft.com/en-us/purview/free-version)


# Terminate
- Delete Microsoft Purview account in Azure portal

# New model than Azure Purview
- > [there's no cost for scanning data assets into the data map, but there are charges for 'governed assets' and 'data management.'](https://learn.microsoft.com/en-us/purview/ms-purview-new-dg-pricing-faq)
- > The new pricing model for Microsoft Purview Data Governance goes into effect on **January 6, 2025**.

## Governed assets
the active management and curation of assets turns assets into 'governed assets.'
- a technical asset is associated to **a data product or a critical data element** is a governed asset
- a governed asset is still a single governed asset regardless of how many concepts are attached to the asset.

> Assets are counted on a daily basis

activities that aren't data governance specific
- registering and scanning of data sources
- storing technical data assets in a common platform in the form of tables, files, datasets, semantic models, AI models, reports, dashboards, etc.

