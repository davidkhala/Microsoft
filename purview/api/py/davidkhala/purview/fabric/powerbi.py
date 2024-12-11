from davidkhala.purview import Catalog, AbstractEntity
from davidkhala.purview.const import entityType
from davidkhala.purview.entity import Asset, Entity
from davidkhala.syntax.js import Array


class Dataset(Entity):
    @staticmethod
    def from_entity(entity):
        return Dataset({
            'entity': entity.entity,
            "referredEntities": entity.referredEntities
        })

    def tables(self):
        return Array(self.referredEntities.values()).filter(lambda e: e['typeName'] == entityType['powerbi']['table'])

    def columns(self):
        return Array(self.referredEntities.values()).filter(lambda e: e['typeName'] == entityType['powerbi']['column'])


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

        return self.dataset_by(qualified_name)

    def dataset_by(self, qualified_name) -> Dataset:
        entity = self.c.get_entity(type_name=entityType['powerbi']['dataset'], qualified_name=qualified_name,
                                   min_ext_info=True,  # with min_ext_info, columns data will not be included
                                   )
        return Dataset(entity)
