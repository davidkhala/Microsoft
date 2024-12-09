/**
 *
 * @enum {string} entityType
 */
export const typeName = {
    powerbi: {
        dataset: "powerbi_dataset",
        report: 'powerbi_report'
    },
    relationship: {
        table2table: 'direct_lineage_dataset_dataset'
    },
    mssql: {
        view: 'azure_sql_view',
        table: 'azure_sql_table',
        DB: 'azure_sql_db',
    },
    databricks: {
        notebook: 'databricks_notebook',
        table: 'databricks_table'
    }
}
export const objectType = {
    table: "Tables"
}