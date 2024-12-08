import unittest

from davidkhala.syntax.format import JSONReadable
from davidkhala.syntax.fs import write

from davidkhala.purview import Catalog

class CatalogTestCase(unittest.TestCase):

    def setUp(self):
        self._catalog = Catalog()

    def test_list(self):
        l = self._catalog.assets()
        write('assets.json', JSONReadable(l))

if __name__ == '__main__':
    unittest.main()
