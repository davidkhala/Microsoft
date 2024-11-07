# enable system.access table
METASTORE_ID=$(curl -s https://raw.githubusercontent.com/davidkhala/spark/refs/heads/main/databricks/cli/context.sh | bash -s metastore)
databricks system-schemas enable $METASTORE_ID access

