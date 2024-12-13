import unittest

from davidkhala.syntax.fs import write_json

from davidkhala.purview.scan import Scan, Source, Run


class SourceTestCase(unittest.TestCase):
    def setUp(self):
        self.source = Source()

    def test_get_source(self):
        name = 'Fabric-AppTeam'
        _source = self.source.get(name)
        self.assertEqual(_source.get('name'), name)
        scan = Scan(name)
        _scans = scan.ls()
        print(_scans)

    def test_list_sources(self):
        sources = self.source.ls()
        print(sources)


class ScanTestCase(unittest.TestCase):
    def setUp(self):
        name = 'AzureDatabricks'
        self.scan = Scan(name)

    def test_list_scans(self):
        for scan in self.scan.ls():
            print(scan.get('name'))

    def test_filter(self):
        r = self.scan.scope('Scan')
        write_json(r, 'filters')


from time import sleep


class RunTestCase(unittest.TestCase):
    def setUp(self):
        data_source_name = 'AzureDatabricks'
        scan_name = 'Scan'
        self.run = Run(data_source_name, scan_name)

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
        :return:
        """
        self.run.start(wait_until_success=True)


if __name__ == '__main__':
    unittest.main()
