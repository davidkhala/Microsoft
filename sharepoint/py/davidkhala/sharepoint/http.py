from davidkhala.utils.http_request import Request
from davidkhala.utils.http_request.stream import Request as StreamRequest
from urllib3 import HTTPResponse


class Graph(Request):
    def __init__(self, tenant: str):
        super().__init__()
        self.tenant = tenant

    def with_client_secret(self, client_id: str, client_secret: str):
        url = f"https://login.microsoftonline.com/{self.tenant}/oauth2/v2.0/token"
        r = self.request(url, method="POST", data={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
            "scope": "https://graph.microsoft.com/.default"
        })

        self.options["headers"]["Authorization"] = f"Bearer {r['access_token']}"

    def get_item(self, site: str, drive: str, path: str):
        url = f"https://graph.microsoft.com/v1.0/sites/{site}/drives/{drive}/root:/{path}"
        return self.request(url, method="GET")

    def get_item_id(self, site: str, drive: str, path: str) -> str:
        return self.get_item(site, drive, path)['id']

    def stream(self, site: str, drive: str, path: str) -> HTTPResponse:
        """
        Expect session open before stream
        Expect session close after stream
        """
        _id = self.get_item_id(site, drive, path)
        req = StreamRequest(self)
        url = f"https://graph.microsoft.com/v1.0/sites/{site}/drives/{drive}/items/{_id}/content"
        resp = req.request(url, "GET")
        return resp.raw
