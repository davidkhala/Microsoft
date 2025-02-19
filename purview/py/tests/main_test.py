import unittest

from davidkhala.azure import default_scopes
from davidkhala.azure.ci import credentials
from davidkhala.syntax.fs import write_json
from davidkhala.microsoft.purview import Catalog

auth = credentials()


class AuthTestCase(unittest.TestCase):
    def test_auth(self):
        auth.get_token(*default_scopes)


class CatalogTestCase(unittest.TestCase):

    def setUp(self):
        self._catalog = Catalog(auth)

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
