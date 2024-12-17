import enum

from davidkhala.purview.databricks import Databricks
from davidkhala.purview.fabric.powerbi import Dataset, Table as PowerBITable
from davidkhala.purview.lineage import Lineage


class Builder:
    def __init__(self, l: Lineage, dataset: Dataset):
        self.dataset = dataset
        self.l = l

    class DatabricksStrategy(enum.Enum):
        Publish = None  # Power BI dataset created `Publish to Power BI workspace`
        Desktop = 1  # Power BI connection file downloaded by `Open in Power BI Desktop`

    def source_databricks(self, adb: Databricks, strategy: DatabricksStrategy):
        self.source = {
            'type': 'databricks',
            "purview": adb,
            "strategy": strategy,
        }

    def build(self):
        tables = self.dataset.tables()
        if self.source['type'] == 'databricks':

            class DatabricksTable(PowerBITable):
                def __init__(self, table: dict, *, catalog: str = None, schema: str = None):
                    super().__init__(table)
                    if not catalog and not schema:
                        # Power BI connection file downloaded by `Open in Power BI Desktop`
                        self.catalog, self.schema, self.table = self.name.replace("`", "").split()
                    else:
                        # other cases
                        self.catalog, self.schema = [catalog, schema]

                @property
                def full_name(self):
                    return f"{self.catalog}.{self.schema}.{self.table}"

            strategy = self.source['strategy']
            for table in tables:  # Assume they are all databricks tables
                if strategy == Builder.DatabricksStrategy.Desktop:
                    bi_table = DatabricksTable(table)
                else:
                    assert strategy == Builder.DatabricksStrategy.Publish
                    _catalog, _schema = self.dataset.name.split('-')
                    bi_table = DatabricksTable(table, catalog=_catalog, schema=_schema)

                databricks_table = self.source['purview'].table(bi_table.full_name)
                databricks_table_entity = self.l.get_entity(guid=databricks_table.id, min_ext_info=True)
                bi_table_entity = self.l.get_entity(guid=bi_table.id, min_ext_info=True)
                if not set(bi_table_entity.column_names) == set(databricks_table_entity.column_names):
                    # column name matching
                    continue
                self.l.table(bi_table, upstreams=[
                    databricks_table.id,
                ])
                self.l.column(
                    bi_table_entity.relation_by_source_id(databricks_table.id),
                    {key: None for key in bi_table_entity.column_names}
                )
