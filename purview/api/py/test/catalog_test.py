import unittest
from catalog import Catalog


class CatalogTestCase(unittest.TestCase):

    def setUp(self):
        self._catalog = Catalog()

    def test_list(self):
        self._catalog.assets()


if __name__ == '__main__':
    unittest.main()
