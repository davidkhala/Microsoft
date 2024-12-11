import unittest

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


from time import sleep
class RunTestCase(unittest.TestCase):
    def setUp(self):
        data_source_name = 'AzureDatabricks'
        scan_name = 'Scan'
        self.run = Run(data_source_name, scan_name)

    def test_dry_run(self):

        run_id = self.run.start(wait_until_success=False)
        sleep(1)
        r = self.run.cancel(run_id)
        print(r)

    def test_list_runs(self):
        runs = self.run.ls()
        for run in runs:
            print(run)
            print("\n")

    def test_run(self):
        """
        This will last for > 3 minutes
        :return:
        """
        self.run.start(wait_until_success=True)




if __name__ == '__main__':
    unittest.main()
