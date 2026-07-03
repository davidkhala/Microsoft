from office365.graph_client import GraphClient
from office365.onedrive.sites.sites_with_root import SitesWithRoot
from office365.sharepoint.client_context import ClientContext


class Context:
    def __init__(self, site_url: str):
        self.client = ClientContext(site_url)


class Graph:
    def __init__(self, tenant: str):
        self.client = GraphClient(tenant=tenant)

    def with_client_secret(self, client_id: str, client_secret: str):
        self.client = self.client.with_client_secret(client_id, client_secret)

    @property
    def sites(self) -> SitesWithRoot:
        return self.client.sites.get().execute_query()


