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

    def wait_until_success(self, run_id):
        found = self.get(run_id)
        if not found:
            raise RuntimeError(f"Run({run_id}) not found")
        if found['status'] == 'Queued':
            from time import sleep
            sleep(1)
            return self.wait_until_success(run_id)
        elif found['status'] == 'Succeeded':
            return found
        else:
            raise RuntimeError(f"Run({run_id}) ends with status '{found['status']}'")

    def start(self, *, scan_level: ScanLevel = ScanLevel.Full, wait_until_success):
        import uuid
        run_id = uuid.uuid4()
        receipt = self.client.scan_result.run_scan(self.data_source_name, self.scan_name, run_id, scan_level=scan_level)

        if wait_until_success:
            self.wait_until_success(run_id)
        return Run.get_id(receipt)

    def get(self, run_id):
        for run in self.client.scan_result.list_scan_history(self.data_source_name, self.scan_name):
            if run['id'] == run_id:
                return run

    def ls(self):
        return list(self.client.scan_result.list_scan_history(self.data_source_name, self.scan_name))

    # TODO After cancel, status is still Queued
    def cancel(self, run_id):
        receipt = self.client.scan_result.cancel_scan(self.data_source_name, self.scan_name, run_id)
        return Run.get_id(receipt)


class Source:
    def __init__(self, **kwargs):
        self.client = get_client(**kwargs)

    def get(self, data_source_name):
        return self.client.data_sources.get(data_source_name)

    def ls(self):
        return list(self.client.data_sources.list_all())
