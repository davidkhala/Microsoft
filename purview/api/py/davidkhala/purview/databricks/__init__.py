from davidkhala.syntax.js import Array

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

    def table(self, full_name) -> Table | None:

        """
        TODO It does not work with filter
        {
            "attributeName": "qualifiedName",
            "operator": "contains",
            "attributeValue": f"/catalogs/{catalog}/schemas/{schema}/tables/{table}"
        },
        # databricks://6874eaf2-721e-4c52-a79f-8d3c0ded5e1d/catalogs/azureopendatastorage/schemas/nyctlc/tables/fhvhv
        :param full_name:
        :return:
        """
        catalog, schema, table = full_name.split('.')

        pattern = f"/catalogs/{catalog}/schemas/{schema}/tables/{table}"
        raw_found = self.c.assets({
            "filter": {
                "and": [

                    {
                        "attributeName": "name",
                        "operator": "eq",
                        "attributeValue": table
                    },

                    {"entityType": entityType['databricks']['table']},
                ]
            }
        })
        found = Array(raw_found).filter(lambda asset: asset['qualifiedName'].endswith(pattern))

        if len(found) == 0:
            return None
        elif len(found) > 1:
            for matched in found:
                import warnings
                warnings.warn(matched.__str__())
            raise RuntimeWarning(f"Multiple Databricks tables found with name '{full_name}'")
        else:
            return Table(found[0])

    def notebook_rename(self, notebook: Notebook, new_name: str):
        notebook.name = new_name
        return self.c.update_entity(notebook)
