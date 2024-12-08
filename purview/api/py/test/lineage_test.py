import unittest
import const
from davidkhala.purview import Catalog

db_endpoint = 'mssql://always-free.database.windows.net/app-kyndryl-hk'

targetViewName = db_endpoint + '/SalesLT/vProductAndDescription'
sourceTable_Product = db_endpoint + '/SalesLT/Product'
sourceTable_ProductModel = db_endpoint + '/SalesLT/ProductModel'
sourceTable_ProductDescription = db_endpoint + '/SalesLT/ProductDescription'
sourceTable_ProductModelProductDescription = db_endpoint + '/SalesLT/ProductModelProductDescription'
sourceTableType = const.type_name['mssql']['table']
targetViewType = const.type_name['mssql']['view']


class AzureSQLDBSampleDatasetTestCase(unittest.TestCase):
    def setUp(self):
        self._catalog = Catalog()
        self.vProductAndDescription = self._catalog.get_entity(targetViewType, targetViewName)
        self.Product = self._catalog.get_entity(sourceTableType, sourceTable_Product)
        self.ProductModel = self._catalog.get_entity(sourceTableType, sourceTable_ProductModel)
        self.ProductDescription = self._catalog.get_entity(sourceTableType, sourceTable_ProductDescription)
        self.ProductModelProductDescription = self._catalog.get_entity(sourceTableType,
                                                                       sourceTable_ProductModelProductDescription)

    def test_table2view_lineage(self):
        self._catalog.lineage_table(self.vProductAndDescription, [
            self.Product.guid,
            self.ProductDescription.guid,
            self.ProductModel.guid,
            self.ProductModelProductDescription.guid,
        ], None)

    def test_column2view_lineage(self):
        r_Product = self.vProductAndDescription.relation_by_source_id(self.Product.guid)

        r_ProductModel = self.vProductAndDescription.relation_by_source_id(self.ProductModel.guid)

        r_ProductDescription = self.vProductAndDescription.relation_by_source_id(self.ProductDescription.guid)

        r_ProductModelProductDescription = self.vProductAndDescription.relation_by_source_id(
            self.ProductModelProductDescription.guid)
        self._catalog.lineage_column(r_Product, {
            'ProductID': None,
            'Name': None,
        })
        self._catalog.lineage_column(r_ProductModel, {
            'Name': 'ProductModel'
        })
        self._catalog.lineage_column(r_ProductDescription, {
            'Culture': None
        })
        self._catalog.lineage_column(r_ProductModelProductDescription, {
            'Description': None
        })



class RenameNotebookTestcase(unittest.TestCase):

    def setUp(self):
        from davidkhala.databricks.workspace.path import SDK
        from davidkhala.databricks.workspace import Workspace
        w = Workspace.from_local()
        self.s = SDK.from_workspace(w)
    def test(self):
        # TODO get all notebook items

        pass
    def test_rename(self):
        self.s.get_by(notebook_id=918032188629039)

if __name__ == '__main__':
    unittest.main()
