import os
from unittest import TestCase

from davidkhala.azure.ci import credentials

from davidkhala.microsoft.fabric.mgmt import Management


class MgmtTest(TestCase):
    auth = credentials()
    
    subscription_id = os.environ.get('SUBSCRIPTION_ID') or "d02180af-0630-4747-ab1b-0d3b3c12dafb"
    mgmt = Management(auth, subscription_id)

    def test_static(self):
        print(self.mgmt.available_sku())

    def test_list(self):
        for entry in self.mgmt.list():
            print(entry)
