import os
import unittest

from databricks.sdk import WorkspaceClient
from davidkhala.azure.ci import credentials

from davidkhala.microsoft.purview import const
from davidkhala.microsoft.purview.databricks.cli import powerbi_dataset_lineage
from davidkhala.microsoft.purview.lineage import Lineage

auth = credentials()


class AzureSQLDBSampleDatasetTestCase(unittest.TestCase):

    def setUp(self):
        self.l = Lineage(auth)
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


from davidkhala.microsoft.purview.lineage.weaver.powerbi import Builder


class DatabricksTestcase(unittest.TestCase):

    def test_rename(self):
        from davidkhala.microsoft.purview.databricks.cli import rename
        from davidkhala.databricks.workspace import Workspace
        token = os.environ.get('DATABRICKS_TOKEN')
        if token:
            w = Workspace(WorkspaceClient(token=token, host=os.environ.get('DATABRICKS_HOST')))
        else:
            w = Workspace.from_local()
        rename(w, auth)

    def test_powerbi_dataset_lineage_desktop(self):
        target_dataset = 'nyctlc'
        powerbi_dataset_lineage(auth, target_dataset, Builder.DatabricksStrategy.Desktop)

    def test_powerbi_dataset_lineage_publish(self):
        # by `Publish to Power BI workspace`
        target_dataset = 'az_databricks-default'
        powerbi_dataset_lineage(auth, target_dataset, Builder.DatabricksStrategy.Publish)


if __name__ == '__main__':
    unittest.main()
