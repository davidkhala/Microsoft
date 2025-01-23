from enum import Enum

from azure.identity import DefaultAzureCredential
from azure.purview.scanning import PurviewScanningClient


def get_client(**kwargs):
    credentials = DefaultAzureCredential()
    endpoint = "https://api.purview-service.microsoft.com/scan"
    return PurviewScanningClient(endpoint, credentials, **kwargs)


class Scan:
    def __init__(self, data_source_name, **kwargs):
        self.client = get_client(**kwargs)
        self.data_source_name = data_source_name

    def ls(self):
        return list(self.client.scans.list_by_data_source(self.data_source_name))

    def scope(self, scan_name):
        return self.client.filters.get(self.data_source_name, scan_name)


class Run:
    def __init__(self, data_source_name, scan_name, **kwargs):
        self.client = get_client(**kwargs)
        self.data_source_name = data_source_name
        self.scan_name = scan_name

    class ScanLevel(Enum):
        Full = 'Full'
        Incremental = 'Incremental'

    @staticmethod
    def get_id(receipt: dict):
        err = receipt['error']
        if err:
            raise err

        assert receipt['status'] == 'Accepted'
        return receipt['scanResultId']

    def wait_until_success(self, run_id: str):
        found = self.get(run_id)
        if not found:
            raise RuntimeError(f"Run({run_id}) not found")
        if found['status'] in ['Queued', 'Running']:
            from time import sleep
            sleep(1)
            return self.wait_until_success(run_id)
        elif found['status'] == 'Succeeded':
            return found
        else:
            raise RuntimeError(f"Run({run_id}) ends with status '{found['status']}'")

    def start(self, *, scan_level: ScanLevel = ScanLevel.Full, wait_until_success):
        import uuid
        run_id = str(uuid.uuid4())
        receipt = self.client.scan_result.run_scan(self.data_source_name, self.scan_name, run_id, scan_level=scan_level)

        if wait_until_success:
            self.wait_until_success(run_id)
        return Run.get_id(receipt)

    def get(self, run_id: str):
        for run in self.client.scan_result.list_scan_history(self.data_source_name, self.scan_name):
            if run['id'] == run_id:
                return run

    def ls(self):
        return list(self.client.scan_result.list_scan_history(self.data_source_name, self.scan_name))

    def wait_until_running(self, run_id: str):
        while True:
            found = self.get(run_id)
            if found['status'] == 'Running':
                break
            else:
                assert found['status'] == 'Queued'

    def cancel(self, run_id):
        self.wait_until_running(run_id)
        receipt = self.client.scan_result.cancel_scan(self.data_source_name, self.scan_name, run_id)
        return Run.get_id(receipt)


class Source:
    def __init__(self, **kwargs):
        self.client = get_client(**kwargs)

    def get(self, data_source_name):
        return self.client.data_sources.get(data_source_name)

    def ls(self):
        return list(self.client.data_sources.list_all())

    def rm(self, data_source_name):
        return self.client.data_sources.delete(data_source_name)
