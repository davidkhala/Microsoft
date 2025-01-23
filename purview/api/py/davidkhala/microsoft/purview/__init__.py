from azure.core.credentials import TokenCredential
from azure.identity import DefaultAzureCredential
from azure.purview.catalog import PurviewCatalogClient

from davidkhala.microsoft.purview.entity import Entity, AbstractEntity


class Catalog:
    def __init__(self, credentials: TokenCredential = DefaultAzureCredential(), **kwargs):
        self.client = PurviewCatalogClient("https://api.purview-service.microsoft.com", credentials, **kwargs)

    def assets(self, options: dict = None) -> list[dict]:
        """
        for filter syntax, see in https://learn.microsoft.com/en-us/rest/api/purview/datamapdataplane/discovery/query?view=rest-purview-datamapdataplane-2023-09-01&tabs=HTTP#examples
        :param options:
        :return:
        """
        if options is None:
            options = {"keywords": "*"}
        r = self.client.discovery.query(search_request=options)

        return r['value']

    def get_entity(self, *, guid=None, type_name=None, qualified_name=None, **kwargs) -> Entity:
        if guid:
            r = self.client.entity.get_by_guid(guid, **kwargs)
        else:
            r = self.client.entity.get_by_unique_attributes(type_name, attr_qualified_name=qualified_name, **kwargs)
        return Entity(r)

    def update_entity(self, _entity: AbstractEntity, **kwargs):
        options = {
            'entity': {
                'attributes': {
                    'qualifiedName': _entity.qualifiedName,
                    'name': _entity.name
                },
                'typeName': _entity.entityType,
                **kwargs,
            }
        }
        return self.client.entity.create_or_update(entity=options)
