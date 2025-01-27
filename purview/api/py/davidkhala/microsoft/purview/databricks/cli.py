import argparse

from azure.core.credentials import TokenCredential
from databricks.sdk import WorkspaceClient
from davidkhala.databricks.workspace import Workspace
from davidkhala.databricks.workspace.path import SDK
from davidkhala.microsoft.purview.databricks import Databricks
from davidkhala.microsoft.purview.lineage import Lineage


def rename(workspace:Workspace, credential: TokenCredential):
    # databricks objects
    sdk = SDK.from_workspace(workspace)
    # purview objects
    lineage = Lineage(credential)
    adb = Databricks(lineage)

    # body
    for notebook in adb.notebooks():
        new_name = sdk.get_by(notebook_id=notebook.notebook_id)
        if new_name:  # if found
            adb.notebook_rename(notebook, new_name)

def main():
    parser = argparse.ArgumentParser(description="Purview notebook rename tool")
    parser.add_argument("--databricks.host", type=str, required=True, help="e.g https://adb-2367537008441771.11.azuredatabricks.net")
    parser.add_argument( "--databricks.token", type=str,required=True, help="databricks token (starting with 'dapi')")

    args = parser.parse_args()
    host = getattr(args, 'databricks.host')
    token = getattr(args, 'databricks.token')

    client = WorkspaceClient(host=host, token=token)


    rename(Workspace(client))





if __name__ == "__main__":
    main()