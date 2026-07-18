import os
import unittest
from unittest import skip

from databricks.sdk import WorkspaceClient
from davidkhala.azure.ci import credentials

from davidkhala.microsoft.purview.databricks.cli import powerbi_dataset_lineage
from davidkhala.microsoft.purview.lineage.weaver.powerbi import Builder

auth = credentials()


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
    @skip
    def test_powerbi_dataset_lineage_desktop(self):
        target_dataset = 'nyctlc'
        powerbi_dataset_lineage(auth, target_dataset, Builder.DatabricksStrategy.Desktop)
    @skip
    def test_powerbi_dataset_lineage_publish(self):
        # by `Publish to Power BI workspace`
        target_dataset = 'az_databricks-default'
        powerbi_dataset_lineage(auth, target_dataset, Builder.DatabricksStrategy.Publish)


if __name__ == '__main__':
    unittest.main()
