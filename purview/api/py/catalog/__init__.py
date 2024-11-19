from azure.identity import DefaultAzureCredential
from azure.purview.catalog import PurviewCatalogClient


class Catalog:
    def __init__(self, **kwargs):
        credentials = DefaultAzureCredential()
        self.client = PurviewCatalogClient("https://api.purview-service.microsoft.com", credentials, **kwargs)

    def assets(self, search_request=None):
        if search_request is None:
            search_request = {"keywords": "*"}
        self.client.discovery.query(search_request)
