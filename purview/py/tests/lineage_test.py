import unittest

from davidkhala.microsoft.purview import const
from davidkhala.microsoft.purview.lineage import Lineage


class AzureSQLDBSampleDatasetTestCase(unittest.TestCase):

    def setUp(self):
        self.l = Lineage()
        db_endpoint = 'mssql://always-free.database.windows.net/app-kyndryl-hk'

        targetViewName = db_endpoint + '/SalesLT/vProductAndDescription'
        sourceTable_Product = db_endpoint + '/SalesLT/Product'
        sourceTable_ProductModel = db_endpoint + '/SalesLT/ProductModel'
        sourceTable_ProductDescription = db_endpoint + '/SalesLT/ProductDescription'
        sourceTable_ProductModelProductDescription = db_endpoint + '/SalesLT/ProductModelProductDescription'

        sourceTableType = const.entityType['mssql']['table']
        targetViewType = const.entityType['mssql']['view']
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
        self.l.table(self.vProductAndDescription,
                     upstreams=[
                         self.Product.guid,
                         self.ProductDescription.guid,
                         self.ProductModel.guid,
                         self.ProductModelProductDescription.guid,
                     ])

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


from davidkhala.microsoft.purview.fabric.powerbi import PowerBI
from davidkhala.microsoft.purview.lineage.weaver.powerbi import Builder


class DatabricksTestcase(unittest.TestCase):

    def setUp(self):
        from davidkhala.databricks.workspace import Workspace
        from davidkhala.databricks.workspace.path import SDK
        # databricks objects
        self.w = Workspace.from_local()
        self.s = SDK.from_workspace(self.w)
        # purview objects
        from davidkhala.microsoft.purview.databricks import Databricks
        self.l = Lineage()
        self.adb = Databricks(self.l)

    def test_rename(self):
        for notebook in self.adb.notebooks():
            new_name = self.s.get_by(notebook_id=notebook.notebook_id)
            if new_name:  # if found
                self.adb.notebook_rename(notebook, new_name)

    def test_powerbi_dataset_lineage_desktop(self):

        target_dataset = 'nyctlc'
        dataset = PowerBI(self.l).dataset(name=target_dataset)
        if not dataset:
            raise Exception(f"dataset({target_dataset}) not found")
        builder = Builder()
        builder.lineage = self.l
        builder.dataset = dataset
        builder.source_databricks(self.adb, Builder.DatabricksStrategy.Desktop)
        builder.build()

    def test_powerbi_dataset_lineage_publish(self):
        # by `Publish to Power BI workspace`
        target_dataset = 'az_databricks-sample'
        dataset = PowerBI(self.l).dataset(name=target_dataset)
        if not dataset:
            raise Exception(f"dataset({target_dataset}) not found")

        builder = Builder()
        builder.lineage = self.l
        builder.dataset = dataset
        builder.source_databricks(self.adb, Builder.DatabricksStrategy.Publish)
        builder.build()


if __name__ == '__main__':
    unittest.main()
