from davidkhala.microsoft.purview import Catalog, AbstractEntity
from davidkhala.microsoft.purview.const import entityType
from davidkhala.microsoft.purview.entity import Asset, Entity


class Table(AbstractEntity):
    """
    Table as a value of `referredEntities`
    """

    def __init__(self, table: dict):
        super().__init__(table)

    @property
    def name(self):
        return self["attributes"]['name']

    @property
    def qualifiedName(self):
        return self["attributes"]['qualifiedName']

    @property
    def entityType(self):
        return self['typeName']

    @property
    def id(self):
        return self['guid']


class Dataset(Entity):

    def __init__(self, body: dict):
        super().__init__(body)

    def tables(self) -> list[dict]:
        return list(filter(lambda e: e['typeName'] == entityType['powerbi']['table'], self.referredEntities.values()))


class PowerBI:

    def __init__(self, c: Catalog):
        self.c = c

    def datasets(self):
        values = self.c.assets({
            "filter": {
                "or": [{"entityType": entityType['powerbi']['dataset']}]
            }
        })
        return list(map(lambda value: Asset(value), values))

    def find_dataset(self, name) -> dict | None:
        found = self.c.assets({
            "filter": {
                "and": [
                    {"entityType": entityType['powerbi']['dataset']},
                    {
                        "attributeName": "name",
                        "operator": "eq",
                        "attributeValue": name
                    }
                ]
            }
        })
        if len(found) == 0:
            return None
        elif len(found) > 1:
            raise RuntimeWarning(f"Multiple powerbi datasets found with name '{name}'")
        else:
            return found[0]

    def dataset(self, *, name=None, qualified_name=None) -> Dataset | None:
        if not qualified_name:
            found = self.find_dataset(name)
            if not found:
                return None
            qualified_name = self.find_dataset(name)['qualifiedName']
        return self.get_dataset(qualified_name)

    def get_dataset(self, qualified_name, min_ext_info=True) -> Dataset:
        entity = self.c.get_entity(
            type_name=entityType['powerbi']['dataset'], qualified_name=qualified_name,
            min_ext_info=min_ext_info,  # with min_ext_info, columns data will not be directly included
        )
        return Dataset(entity)
