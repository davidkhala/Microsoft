import uuid

from azure.identity import DefaultAzureCredential
from azure.purview.scanning import PurviewScanningClient


class Scan:
    def __init__(self, **kwargs):
        credentials = DefaultAzureCredential()
        self.client = PurviewScanningClient("https://api.purview-service.microsoft.com", credentials, **kwargs)

    def run(self, data_source_name, scan_name):
        run_id = uuid.uuid4()
        self.client.scan_result.run_scan(data_source_name, scan_name, run_id)

    def ls(self, data_source_name):
        self.client.scans.list_by_data_source(data_source_name)

    # TODO
    def sources(self):
        self.client.data_sources.list_all()
