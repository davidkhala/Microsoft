import enum
import warnings

from davidkhala.syntax.js import Array

from davidkhala.purview import Catalog, AbstractEntity
from davidkhala.purview.const import entityType
from davidkhala.purview.entity import Asset, Entity


class Strategy(enum.Enum):
    Desktop = 1
    Fabric = 2


class Table(AbstractEntity):
    """
    Table as a value of `referredEntities`
    """

    def __init__(self, table: dict, strategy: Strategy = Strategy.Desktop):
        super().__init__(table)
        self.strategy = strategy

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


class DatabricksTable(Table):
    def __init__(self, *args):
        super().__init__(*args)
        if self.strategy == Strategy.Desktop:
            self.catalog, self.schema, self.table = self.name.replace("`", "").split()

    @property
    def full_name(self):
        return f"{self.catalog}.{self.schema}.{self.table}"


class Dataset(Entity):

    def __init__(self, body: dict, min_ext_info):
        super().__init__(body)
        self.min_ext_info = min_ext_info

    def tables(self) -> Array[dict]:
        return Array(self.referredEntities.values()).filter(lambda e: e['typeName'] == entityType['powerbi']['table'])

    def columns(self) -> Array[dict]:
        r = Array(self.referredEntities.values()).filter(lambda e: e['typeName'] == entityType['powerbi']['column'])
        if self.min_ext_info:
            warnings.warn("with min_ext_info=True, columns data will not be included")
            assert r.__len__() == 0
        return r


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

    def dataset(self, *, name=None, qualified_name=None) -> Dataset | None:
        if not qualified_name:
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
                qualified_name = found[0]['qualifiedName']

        return self.datasetWithReferredEntities(qualified_name)

    def datasetWithReferredEntities(self, qualified_name, min_ext_info=True) -> Dataset:
        entity = self.c.get_entity(
            type_name=entityType['powerbi']['dataset'], qualified_name=qualified_name,
            min_ext_info=min_ext_info,  # with min_ext_info, columns data will not be included
        )
        return Dataset(entity, min_ext_info)
