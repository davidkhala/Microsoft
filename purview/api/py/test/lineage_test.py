import unittest

import const
from davidkhala.purview.lineage import Lineage
from davidkhala.purview.lineage.databricks import Databricks

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
        self.l = Lineage()
        self.vProductAndDescription = self.l.get_entity(type_name=targetViewType, qualified_name=targetViewName)
        self.Product = self.l.get_entity(type_name=sourceTableType, qualified_name=sourceTable_Product)
        self.ProductModel = self.l.get_entity(type_name=sourceTableType, qualified_name=sourceTable_ProductModel)
        self.ProductDescription = self.l.get_entity(
            type_name=sourceTableType,
            qualified_name=sourceTable_ProductDescription
        )
        self.ProductModelProductDescription = self.l.get_entity(
            type_name=sourceTableType,
            qualified_name=sourceTable_ProductModelProductDescription
        )

    def test_table2view_lineage(self):
        self.l.table(self.vProductAndDescription, [
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
        self.l.column(r_Product, {
            'ProductID': None,
            'Name': None,
        })
        self.l.column(r_ProductModel, {
            'Name': 'ProductModel'
        })
        self.l.column(r_ProductDescription, {
            'Culture': None
        })
        self.l.column(r_ProductModelProductDescription, {
            'Description': None
        })


class DatabricksTestcase(unittest.TestCase):

    def setUp(self):
        from davidkhala.databricks.workspace.path import SDK
        from davidkhala.databricks.workspace import Workspace
        w = Workspace.from_local()
        self.s = SDK.from_workspace(w)
        self.l = Databricks(Lineage())

    def test_rename(self):
        notebooks = self.l.notebooks()
        for notebook in notebooks:
            new_name = self.s.get_by(notebook_id=notebook.notebook_id)
            if new_name:  # if found
                self.l.notebook_rename(notebook, new_name)


if __name__ == '__main__':
    unittest.main()
