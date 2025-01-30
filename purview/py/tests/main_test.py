import unittest

from davidkhala.syntax.fs import write_json
from davidkhala.microsoft.purview import Catalog
from tests.ci import credentials


class CatalogTestCase(unittest.TestCase):

    def setUp(self):
        self._catalog = Catalog(credentials())

    def test_list(self):
        l = self._catalog.assets()
        write_json(l, 'assets')

    def test_update(self):
        l = self._catalog.assets()
        guid = l[0]['id']
        e = self._catalog.get_entity(guid=guid)
        self._catalog.update_entity(e, guid=e.guid)


if __name__ == '__main__':
    unittest.main()
