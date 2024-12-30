# Data warehouse
> Data warehouse is powered up with Synapse Analytics
> Microsoft Fabric's data warehouse is a modern version of the traditional data warehouse.
- it is stored in Delta format and can be queried using T-SQL

Provion in either

- **create hub**
- **workspace**


## Clone tables

- **head-only**: zero-copy cloning to minimize storage costs
  - copying the metadata
  - still referencing the same data files in OneLake

## cross-database querying
Usecase when
- Tables existing in lakehouse
- read-only requirement: not intent to make changes
- avoid copying data from lakehouse to warehouse

## **Query** view
Visual query editor
- Similar to [**Power Query online diagram view**](https://learn.microsoft.com/en-us/power-query/diagram-view)


## **Model** view

Relationships
- *Relationships* allow you to connect tables in the semantic model
- Can be created between tables in **Model** view by click-and-drag
