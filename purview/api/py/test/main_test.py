import unittest

from davidkhala.syntax.fs import write_json

from davidkhala.purview import Catalog


class CatalogTestCase(unittest.TestCase):

    def setUp(self):
        self._catalog = Catalog()

    def test_list(self):
        l = self._catalog.assets()
        write_json(l, 'assets')
    def test_find(self):
        l=self._catalog.assets({"keywords": "1274571724986851"})
        write_json(l, 'assets_one')
        # TODO https://learn.microsoft.com/en-us/rest/api/purview/datamapdataplane/discovery/query?view=rest-purview-datamapdataplane-2023-09-01&tabs=HTTP#discovery_query_type

if __name__ == '__main__':
    unittest.main()
