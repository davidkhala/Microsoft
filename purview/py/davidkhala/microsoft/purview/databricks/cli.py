import argparse

from azure.core.credentials import TokenCredential
from databricks.sdk import WorkspaceClient
from davidkhala.azure.auth import from_service_principal
from davidkhala.databricks.workspace import Workspace
from davidkhala.databricks.workspace.path import SDK

from davidkhala.microsoft.purview.databricks import Databricks
from davidkhala.microsoft.purview.fabric.powerbi import PowerBI
from davidkhala.microsoft.purview.lineage import Lineage
from davidkhala.microsoft.purview.lineage.weaver.powerbi import Builder


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


def powerbi_dataset_lineage(credential: TokenCredential, target_dataset: str, strategy: Builder.DatabricksStrategy):
    lineage = Lineage(credential)
    adb = Databricks(lineage)
    dataset = PowerBI(lineage).dataset(name=target_dataset)
    if not dataset:
        raise Exception(f"dataset({target_dataset}) not found")
    builder = Builder()
    builder.lineage = lineage
    builder.dataset = dataset
    builder.source_databricks(adb, strategy)
    builder.build()


def main():
    parser = argparse.ArgumentParser(description="Microsoft Purview tool for Databricks")

    parser.add_argument("--entra.tenant-id", required=True, help="Tenant ID of the Entra Domain")
    parser.add_argument("--entra.client-id", required=True, help="Application (client) ID of the Service Principal")
    parser.add_argument("--entra.client-secret", required=True,
                        help="Value of a Client secret, belonging to the Service Principal")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subparser for the 'rename' action
    rename_parser = subparsers.add_parser("rename", help="Rename Databricks Notebook asset")
    rename_parser.add_argument("--databricks.host", help="e.g https://adb-2367537008441771.11.azuredatabricks.net")
    rename_parser.add_argument("--databricks.token", help="Databricks token (starting with 'dapi')")

    # Subparser for the 'lineage' action
    lineage_parser = subparsers.add_parser("lineage", help="Weave data assets")
    lineage_parser.add_argument("strategy", choices=['desktop', 'publish'], help="Publish strategy from Databricks")
    lineage_parser.add_argument("--dataset", required=True, help="Targeted PowerBI dataset name")

    args = parser.parse_args()
    credential = from_service_principal(
        getattr(args, 'entra.tenant_id'),
        getattr(args, 'entra.client_id'),
        getattr(args, 'entra.client_secret'),
    )
    match args.command:
        case 'rename':
            client = WorkspaceClient(host=getattr(args, 'databricks.host'), token=getattr(args, 'databricks.token'))
            client.current_user.me() # validate
            rename(Workspace(client), credential)
        case 'lineage':
            strategy = Builder.DatabricksStrategy.Publish
            if getattr(args, 'strategy') == 'desktop':
                strategy = Builder.DatabricksStrategy.Desktop

            powerbi_dataset_lineage(credential, getattr(args, 'dataset'), strategy)


if __name__ == "__main__":
    main()
