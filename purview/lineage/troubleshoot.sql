select

 t.workspace_id,

 t.entity_type,

 t.entity_id,

 t.entity_run_id,

 t.source_table_full_name,

 t.source_type,

 t.target_table_full_name,

 t.target_type,

 t.event_time,

 c.source_column_name,

 c.target_column_name

from

 (

   select

     workspace_id,

     entity_type,

     entity_id,

     entity_run_id,

     source_table_full_name,

     source_type,

     target_table_full_name,

     target_type,

     event_time

   from

     system.access.table_lineage

   where

     workspace_id=3410668323225095

     and entity_type in('NOTEBOOK')

     and source_table_catalog != 'system'

     and source_table_catalog in ('azure-open-datasets') and target_table_catalog in ('azure-open-datasets')

     and source_table_full_name is not null

     and target_table_full_name is not null

     limit 100000 

 ) t

 left join (

   select

     entity_type,

     entity_id,

     entity_run_id,

     source_table_full_name,

     source_column_name,

     target_table_full_name,

     target_column_name

   from

     system.access.column_lineage

 ) c on t.entity_id = c.entity_id

 and t.entity_run_id = c.entity_run_id and t.source_table_full_name = c.source_table_full_name and t.target_table_full_name = c.target_table_full_name
