# (Data) Pipelines
Similar to Databricks DLT and Azure Data Factory

> To create a pipeline based on a template, select the **Choose a task to start** tile  

## Activity
Pipelines encapsulate a sequence of *activities*
> Activities are the executable tasks

## Data transformation activities
It includes 
- simple **Copy Data** activities for data ingestion
- **Data Flow** activities that encapsulate [dataflows (Gen2)](https://github.com/davidkhala/azure-utils/tree/main/data/factory#dataflows-gen2) for data transformations.
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
 