import unittest

from davidkhala.syntax.fs import write_json

from davidkhala.purview import const, Catalog
from davidkhala.purview.fabric.powerbi import DatabricksTable
from davidkhala.purview.lineage import Lineage


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
        from davidkhala.databricks.workspace import Workspace
        from davidkhala.databricks.workspace.path import SDK
        from davidkhala.databricks.workspace.table import Table
        # databricks objects
        self.w = Workspace.from_local()
        self.s = SDK.from_workspace(self.w)
        self.t = Table(self.w.client)
        # purview objects
        from davidkhala.purview.databricks import Databricks
        self.l = Lineage()
        self.adb = Databricks(self.l)

    def test_rename(self):
        for notebook in self.adb.notebooks():
            new_name = self.s.get_by(notebook_id=notebook.notebook_id)
            if new_name:  # if found
                self.adb.notebook_rename(notebook, new_name)

    def test_powerbi_dataset_inspect(self):
        from davidkhala.purview.fabric.powerbi import PowerBI
        bi = PowerBI(self.l)
        target_dataset = 'nyctlc'
        dataset = bi.dataset(name=target_dataset)
        write_json(dataset, target_dataset)
        tables = dataset.tables()
        columns = dataset.columns()
        write_json(tables, target_dataset + '.tables')
        write_json(columns, target_dataset + '.columns')

    def test_table_link(self):
        from davidkhala.purview.fabric.powerbi import PowerBI
        bi = PowerBI(self.l)
        target_dataset = 'nyctlc'
        dataset = bi.dataset(name=target_dataset)
        tables = dataset.tables()
        for table in tables:  # Assume they are all databricks tables
            bi_table = DatabricksTable(table)
            if self.t.exists(bi_table.full_name):
                databricks_table = self.adb.table(bi_table.full_name)

                self.l.table(bi_table, upstreams=[
                    databricks_table.id,
                ])
                bi_table_entity = self.l.get_entity(guid=bi_table.id, min_ext_info=True)
                self.l.column(
                    bi_table_entity.relation_by_source_id(databricks_table.id),
                    {key: None for key in bi_table_entity.column_names}
                )


if __name__ == '__main__':
    unittest.main()
