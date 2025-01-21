# Real-Time Intelligence

[What's Real-Time data analytics](https://github.com/davidkhala/BI-collection/wiki/Real%E2%80%90time-analytics)

![fabric](https://learn.microsoft.com/en-us/training/wwl/get-started-kusto-fabric/media/real-time-intelligence-core.png)


## *eventstream*

streaming ETL

Data destinations

- *eventhouse*
- Lakehouse
- Derived stream: cascading
  - redirect the output of your eventstream to another eventstream
- Activator
- Custom endpoint
  - route your events to custom endpoint

## *eventhouse*
streaming data storage

### KQL databases
a collection of tables, stored functions, materialized views, and shortcuts.
### KQL queryset
work with KQL database tables

### [OneLake Availability](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/event-house-onelake-availability#how-it-works)
- Create a logical(soft) copy of KQL database in OneLake
  - There's no additional storage cost

## *real-time dashboard*

## (Fabric Data) Activator
a technology that enables automated processing of events that trigger actions.

Concepts
- Events: record in a stream of data at a specific point in time.
- Objects: The data in an event record
- Properties: The fields in the event data can be mapped to properties of the business object
- Rules: set conditions based on the property values of objects referenced in events
