from davidkhala.microsoft.purview import Catalog
from davidkhala.microsoft.purview.const import entityType
from davidkhala.microsoft.purview.entity import Asset


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

    def table(self, full_name) -> Table | None:

        catalog, schema, table = full_name.split('.')

        qualifiedName_filters = list(map(lambda token: {
            "attributeName": "qualifiedName",
            "operator": "contains",
            "attributeValue": token
        }, [catalog, schema, table]))

        found = self.c.assets({
            "filter": {
                "and": [
                    {
                        "attributeName": "name",
                        "operator": "eq",
                        "attributeValue": table
                    },
                    {"entityType": entityType['databricks']['table']},
                    *qualifiedName_filters,
                ]
            }
        })

        if len(found) == 0:
            return None
        elif len(found) > 1:
            for matched in found:
                import warnings
                warnings.warn(matched.__str__())
            raise RuntimeWarning(f"Multiple Databricks tables found with name '{full_name}'")
        else:
            assert found[0]['qualifiedName'].endswith(f"/catalogs/{catalog}/schemas/{schema}/tables/{table}")
            return Table(found[0])

    def notebook_rename(self, notebook: Notebook, new_name: str):
        notebook.name = new_name
        return self.c.update_entity(notebook)
