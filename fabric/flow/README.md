# Dataflows Gen2
A low-to-no-code ETL solution
- Power Bi dev friendly
  - based on Power Query Online
- Provision in either 
  - Data Factory workload
  - PowerBI workspace
  - lakehouse


# migration 
[Getting from Dataflow Generation 1](https://learn.microsoft.com/en-us/fabric/data-factory/dataflows-gen2-overview#licensing-dataflow-gen1-vs-gen2)
- You can now separate your ETL logic and destination storage by [Data destinations]
- dataflow autosave to cloud or save as draft


# Design notes
- > Dataflows aren't a replacement for a data warehouse.
- > Row-level security isn't supported.

License requirement: **Fabric capacity** or **Trial**