/**
 *
 * @enum {string} entityType
 */
export const entityType = {
    powerbi: {
        dataset: "powerbi_dataset", report: 'powerbi_report'
    },
    mssql: {
        view: 'azure_sql_view', table: 'azure_sql_table', DB: 'azure_sql_db',
    },
    databricks: {
        notebook: 'databricks_notebook', table: 'databricks_table'
    }
}
export const relationshipType = {
    table2table: 'direct_lineage_dataset_dataset'
}
export const objectType = {
    table: "Tables"
}