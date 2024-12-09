import unittest

from davidkhala.syntax.fs import write_json

from davidkhala.purview import Catalog


class CatalogTestCase(unittest.TestCase):

    def setUp(self):
        self._catalog = Catalog()

    def test_list(self):
        l = self._catalog.assets()
        write_json(l, 'assets')

    def test_update(self):
        guid = "bbc03f8d-4a4e-4413-9bf7-33016c7aa695"
        e = self._catalog.get_entity(guid=guid)

        self._catalog.update_entity(e, guid=e.guid)


if __name__ == '__main__':
    unittest.main()
