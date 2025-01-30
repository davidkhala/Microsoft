import os

from davidkhala.azure.auth import from_service_principal, default


def credentials():
    client_secret = os.environ.get('CLIENT_SECRET'),
    if client_secret:
        return from_service_principal(
            tenant_id=os.environ.get('TENANT_ID'),
            client_id=os.environ.get('CLIENT_ID'),
            client_secret=client_secret,
        )
    return default()
