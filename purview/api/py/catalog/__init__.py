from azure.identity import DefaultAzureCredential
from azure.purview.catalog import PurviewCatalogClient

from catalog.entity import Entity


class Catalog:
    def __init__(self, **kwargs):
        credentials = DefaultAzureCredential()
        self.client = PurviewCatalogClient("https://api.purview-service.microsoft.com", credentials, **kwargs)

    def assets(self, search_request=None):
        if search_request is None:
            search_request = {"keywords": "*"}
        r = self.client.discovery.query(search_request)
        return r['value']

    def get_entity(self, type_name, qualified_name):

        r = self.client.entity.get_by_unique_attributes(type_name, attr_qualified_name=qualified_name)
        return Entity(r)
