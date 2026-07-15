import unittest

from davidkhala.azure.ci import credentials
from davidkhala.utils.syntax.fs import write_json

from davidkhala.microsoft.purview.scan import Scan, Source, Run

auth = credentials()


class SourceTestCase(unittest.TestCase):
    def setUp(self):
        self.source = Source(auth)

    def test_get_source(self):
        name = 'Fabric'
        _source = self.source.get(name)
        self.assertEqual(_source.get('name'), name)

    def test_list_sources(self):
        sources = self.source.ls()
        print(sources)
        print(self.source.names)


class ScanTestCase(unittest.TestCase):
    def setUp(self):
        name = 'Fabric'
        self.scan = Scan(auth, name)

    def test_list_scans(self):
        for scan in self.scan.ls():
            name = scan.get('name')
            r = self.scan.scope(name)
            write_json(r, 'filters')


class RunTestCase(unittest.TestCase):
    def setUp(self):
        data_source_name = 'Fabric'
        scan_name = 'Scan-shared-only'
        self.run = Run(auth, data_source_name, scan_name)

    def test_dry_run(self):
        run_id = self.run.start(wait_until_success=False)
        self.run.cancel(run_id)
        print(run_id)

    def test_list_runs(self):
        runs = self.run.ls()
        write_json(runs, 'runs')

    def test_run(self):
        """
        This will last for > 3 minutes
        """
        self.run.start(wait_until_success=True)


if __name__ == '__main__':
    unittest.main()
