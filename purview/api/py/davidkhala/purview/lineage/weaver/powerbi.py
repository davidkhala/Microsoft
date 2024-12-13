import enum

from davidkhala.databricks.workspace.table import Table

from davidkhala.purview.databricks import Databricks
from davidkhala.purview.fabric.powerbi import Dataset, Table as PowerBITable
from davidkhala.purview.lineage import Lineage


class Builder:
    def __init__(self, l: Lineage, dataset: Dataset):
        self.dataset = dataset
        self.l = l

    def source_databricks(self, t: Table, adb: Databricks):
        self.source = {
            'type': 'databricks',
            "table": t,
            "purview": adb
        }

    def build(self):
        tables = self.dataset.tables()
        if self.source['type'] == 'databricks':
            for table in tables:  # Assume they are all databricks tables
                bi_table = DatabricksTable(table)
                if not self.source['table'].exists(bi_table.full_name):
                    continue
                databricks_table = self.source['purview'].table(bi_table.full_name)

                self.l.table(bi_table, upstreams=[
                    databricks_table.id,
                ])
                bi_table_entity = self.l.get_entity(guid=bi_table.id, min_ext_info=True)
                self.l.column(
                    bi_table_entity.relation_by_source_id(databricks_table.id),
                    {key: None for key in bi_table_entity.column_names}
                )


class Strategy(enum.Enum):
    Desktop = 1
    Fabric = 2


class DatabricksTable(PowerBITable):
    def __init__(self, table: dict, strategy=Strategy.Desktop):
        super().__init__(table)
        if strategy == Strategy.Desktop:
            self.catalog, self.schema, self.table = self.name.replace("`", "").split()

    @property
    def full_name(self):
        return f"{self.catalog}.{self.schema}.{self.table}"
