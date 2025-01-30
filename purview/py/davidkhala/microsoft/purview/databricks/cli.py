import argparse

from azure.core.credentials import TokenCredential
from databricks.sdk import WorkspaceClient
from davidkhala.azure.auth import from_service_principal
from davidkhala.databricks.workspace import Workspace
from davidkhala.databricks.workspace.path import SDK
from davidkhala.microsoft.purview.databricks import Databricks
from davidkhala.microsoft.purview.lineage import Lineage


def rename(workspace: Workspace, credential: TokenCredential):
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
    parser.add_argument("--databricks.host", type=str, required=True,
                        help="e.g https://adb-2367537008441771.11.azuredatabricks.net")
    parser.add_argument("--databricks.token", type=str, required=True, help="databricks token (starting with 'dapi')")
    parser.add_argument("--entra.tenant-id", type=str, required=True)
    parser.add_argument("--entra.client-id", type=str, required=True)
    parser.add_argument("--entra.client-secret", type=str, required=True)

    args = parser.parse_args()
    credential = from_service_principal(
        getattr(args, 'entra.tenant-id'),
        getattr(args, 'entra.client-id'),
        getattr(args, 'entra.client-secret'),
    )
    client = WorkspaceClient(host=getattr(args, 'databricks.host'), token=getattr(args, 'databricks.token'))

    rename(Workspace(client), credential)


if __name__ == "__main__":
    main()
