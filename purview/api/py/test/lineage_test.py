import unittest
import const
from catalog import Catalog

db_endpoint = 'mssql://always-free.database.windows.net/app-kyndryl-hk'

targetViewName = db_endpoint + '/SalesLT/vProductAndDescription'
sourceTable_Product = db_endpoint + '/SalesLT/Product'
sourceTable_ProductModel = db_endpoint + '/SalesLT/ProductModel'
sourceTable_ProductDescription = db_endpoint + '/SalesLT/ProductDescription'
sourceTable_ProductModelProductDescription = db_endpoint + '/SalesLT/ProductModelProductDescription'
sourceTableType = const.type_name['mssql']['table']
targetViewType = const.type_name['mssql']['view']
class LineageTestCase(unittest.TestCase):
    def setUp(self):
        self._catalog = Catalog()
        self.vProductAndDescription = self._catalog.get_entity(targetViewType, targetViewName)
        print(self.vProductAndDescription.guid)
        self.Product = self._catalog.get_entity(sourceTableType, sourceTable_Product)
        self.ProductModel = self._catalog.get_entity(sourceTableType, sourceTable_ProductModel)
        self.ProductDescription = self._catalog.get_entity(sourceTableType, sourceTable_ProductDescription)
        self.ProductModelProductDescription = self._catalog.get_entity(sourceTableType, sourceTable_ProductModelProductDescription)
    def test_table2view_lineage(self):
        print()

if __name__ == '__main__':
    unittest.main()