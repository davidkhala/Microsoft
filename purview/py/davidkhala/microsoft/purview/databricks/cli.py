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
    parser = argparse.ArgumentParser(description="Purview tool for Databricks")

    parser.add_argument("--entra.tenant-id", required=True)
    parser.add_argument("--entra.client-id", required=True)
    parser.add_argument("--entra.client-secret", required=True)

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subparser for the 'rename' action
    rename_parser = subparsers.add_parser("rename", help="Rename Databricks Notebook asset in Purview")
    rename_parser.add_argument("--databricks.host", help="e.g https://adb-2367537008441771.11.azuredatabricks.net")
    rename_parser.add_argument("--databricks.token", help="Databricks token (starting with 'dapi')")

    # Subparser for the 'lineage' action
    lineage_parser = subparsers.add_parser("lineage", help="weave assets in Purview")
    lineage_parser.add_argument("strategy",choices=['desktop', 'publish'], required=True, help="Publish strategy from Databricks")
    lineage_parser.add_argument("--dataset", required=True, help="Targeted PowerBI dataset name")

    args = parser.parse_args()
    credential = from_service_principal(
        getattr(args, 'entra.tenant-id'),
        getattr(args, 'entra.client-id'),
        getattr(args, 'entra.client-secret'),
    )
    match args.command:
        case 'rename':
            client = WorkspaceClient(host=getattr(args, 'databricks.host'), token=getattr(args, 'databricks.token'))
            rename(Workspace(client), credential)
        case 'lineage':
            strategy = Builder.DatabricksStrategy.Publish
            match getattr(args, 'strategy'):
                case 'desktop':
                    strategy = Builder.DatabricksStrategy.Desktop

            powerbi_dataset_lineage(credential, getattr(args,'dataset'), strategy)


if __name__ == "__main__":
    main()
