from azure.core.credentials import TokenCredential
from azure.mgmt.fabric import FabricMgmtClient


class Management:
    def __init__(self, credential: TokenCredential, subscription_id):
        self.client = FabricMgmtClient(credential, subscription_id)

    def pause(self, resource_group_name: str, capacity_name: str):
        self.client.fabric_capacities.begin_suspend(resource_group_name, capacity_name).result()

    def available_sku(self, location='East Asia'):
        r = []
        for entry in self.sku():
            if entry['location'] == location: r.append(entry["name"])
        return r

    def list(self):
        return ({
            "properties": entry.properties,
            "id": entry.id,
            "name": entry.name,
            "location": entry.location,
            "sku": entry.sku.name
        } for entry in self.client.fabric_capacities.list_by_subscription())

    def sku(self):
        return ({
            "name": entry.name,
            "location": entry.locations[0]
        } for entry in self.client.fabric_capacities.list_skus())
