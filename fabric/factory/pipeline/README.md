# Data Pipelines
low-code experience
- Similar to Databricks DLT and Azure Data Factory
- Alternative to Dataflow Gen2
- > Most of the functionality of data pipelines comes from Azure Data Factory

# Provision
1. Entrances
    - From the workspace: Select **+ New**, then select **Data pipeline**.
    - From the warehouse asset: Select **Get Data**, and then **New data pipeline**.
2. [Start building your data pipeline]
    - from scratch: Select the **Add pipeline activity** tile
    - [Copy data](./activity/CopyData.md)
    - based on a template: Select the **Choose a task to start** tile


## Activity
Pipelines encapsulate a sequence of *activities*
> Activities are the executable tasks

## Data transformation activities
It includes 
- simple **Copy Data** activities for data ingestion
- **Data Flow** activities that encapsulate [dataflows (Gen2)](../../flow/README.md) for data transformations.
- **Notebook** activities to run a Spark notebook
- **Stored procedure** activities to run SQL code
- **Delete data** activities to delete existing data


## Control flow activities
> use to implement loops, conditional branching, or manage variable and parameter values


## Canvas
> The graphical pipeline *canvas* in Fabric user interface

## Run
> Each time a pipeline is executed, a *data pipeline run* is initiated.

view run history from canvas or from pipeline item list
 