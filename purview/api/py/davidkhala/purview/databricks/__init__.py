from davidkhala.purview import Catalog
from davidkhala.purview.const import entityType
from davidkhala.purview.entity import Asset


class Notebook(Asset):

    @property
    def notebook_id(self):
        """
        object_id in Databricks API
        :return:
        """
        return self.qualifiedName.split('/')[-1]


class Table(Asset):
    @property
    def table(self):
        return self.qualifiedName.split('/')[-1]

    @property
    def schema(self):
        return self.qualifiedName.split('/')[-3]

    @property
    def catalog(self):
        return self.qualifiedName.split('/')[-5]


class Databricks:
    def __init__(self, c: Catalog):
        self.c = c

    def notebooks(self) -> list[Notebook]:
        values = self.c.assets({
            "filter": {
                "or": [{"entityType": entityType['databricks']['notebook']}]
            }
        })
        return list(map(lambda value: Notebook(value), values))

    def tables(self) -> list[Table]:
        values = self.c.assets({
            "filter": {
                "or": [{"entityType": entityType['databricks']['table']}]
            }
        })
        return list(map(lambda value: Table(value), values))

    def notebook_rename(self, notebook: Notebook, new_name: str):
        notebook.name = new_name
        return self.c.update_entity(notebook)
