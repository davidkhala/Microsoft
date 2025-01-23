entityType = {
    'powerbi': {
        'dataset': 'powerbi_dataset',
        'report': 'powerbi_report',
        'table': 'powerbi_table',
        'column': 'powerbi_column'
    },
    'mssql': {
        'view': 'azure_sql_view',
        'table': 'azure_sql_table',
        'DB': 'azure_sql_db',
    },
    'databricks': {
        'notebook': 'databricks_notebook',
        'table': 'databricks_table'
    }
}

relationshipType = {
    'mssql': {
        'table2table': 'direct_lineage_dataset_dataset'
    },
    'powerbi': {
        'table_has_columns': 'powerbi_column_table'
    },

}

objectType = {
    'table': 'Tables'
}
