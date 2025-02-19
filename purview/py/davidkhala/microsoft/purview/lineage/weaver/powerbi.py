import enum

from davidkhala.microsoft.purview import TableWare
from davidkhala.microsoft.purview.fabric.powerbi import Dataset, Table as PowerBITable
from davidkhala.microsoft.purview.lineage import Lineage
from davidkhala.microsoft.purview.relationship import Relationship


class DatabricksTable(PowerBITable):
    def __init__(self, table: dict, *, catalog: str = None, schema: str = None):
        super().__init__(table)
        if not catalog and not schema:
            # Power BI connection file downloaded by `Open in Power BI Desktop`
            self.catalog, self.schema, self.table = self.name.replace("`", "").split()
        else:
            # other cases
            self.catalog = catalog
            self.schema = schema
            self.table = self.name

    @property
    def full_name(self):
        return f"{self.catalog}.{self.schema}.{self.table}"


class Builder:
    source: dict
    lineage: Lineage
    dataset: Dataset

    class DatabricksStrategy(enum.Enum):
        Publish = None  # Power BI dataset created `Publish to Power BI workspace`
        Desktop = 1  # Power BI connection file downloaded by `Open in Power BI Desktop`

    def source_databricks(self, adb: TableWare, strategy: DatabricksStrategy):
        self.source = {
            'type': 'databricks',
            "purview": adb,
            "strategy": strategy,
        }

    def build(self):
        tables = self.dataset.tables()
        match self.source['type']:
            case 'databricks':

                strategy = self.source['strategy']
                print(self.source['type'], 'table.count()', tables.__len__())
                for table in tables:  # Assume they are all databricks tables
                    match strategy:
                        case Builder.DatabricksStrategy.Desktop:
                            bi_table = DatabricksTable(table)
                        case Builder.DatabricksStrategy.Publish:
                            _catalog, _schema = self.dataset.displayName.split('-')
                            bi_table = DatabricksTable(table, catalog=_catalog, schema=_schema)

                    databricks_table = self.source['purview'].table(bi_table.full_name)
                    databricks_table_entity = self.lineage.get_entity(guid=databricks_table.id, min_ext_info=True)
                    bi_table_entity = self.lineage.get_entity(guid=bi_table.id, min_ext_info=True)
                    if set(bi_table_entity.column_names) != set(databricks_table_entity.column_names):
                        # column name matching
                        continue
                    self.lineage.table(bi_table, upstreams=[
                        databricks_table.id,
                    ])
                    relationship: Relationship | None = bi_table_entity.relation_by_source_id(databricks_table.id)
                    count = 0
                    while not relationship:
                        from time import sleep
                        sleep(1)
                        relationship = bi_table_entity.relation_by_source_id(databricks_table.id)
                        count += 1
                        print('wait until relationship ready...' + str(count))
                    self.lineage.column(
                        relationship,
                        {key: None for key in bi_table_entity.column_names}
                    )
