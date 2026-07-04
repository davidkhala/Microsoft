import os
import unittest

from davidkhala.sharepoint import Graph
from davidkhala.sharepoint.drive import Drive

tenant_id = os.environ.get('TENANT_ID') or 'c2a38aca-e9c7-4647-8dcd-9185476159ae'
client_id = os.environ.get('CLIENT_ID') or '0676462e-da60-48f3-9625-de82783ca64a'
client_secret = os.environ.get('CLIENT_SECRET')


class GraphClientTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Graph(tenant_id)
        self.client.with_client_secret(client_id, client_secret)

    def test_auth(self):
        print(self.client.sites)

    def test_list(self):
        for site in self.client.sites:
            drives = site.drives.get().execute_query()
            print(site, site.id)
            for drive in drives:
                print(site, "--", drive.id)
                d = Drive(drive)
                d.tree(f"{site.name}/")


class DriveTestCase(GraphClientTestCase):
    def setUp(self):
        super().setUp()
        self.drive = Drive(
            self.client.client.sites[
                'davidkhalahotmail.sharepoint.com,3f75f1a6-1239-4862-b14d-367c1c865604,d786840e-231b-4b8a-b38a-19e174ebb25d'
            ].drive
        )

    def test_default_drive(self):
        self.assertEqual('b!pvF1PzkSYkixTTZ8HIZWBA6EhtcbI4pLs4oZ4XTrsl1HYF74jUSjSr-0WF8hBZy5', self.drive.id)
        self.assertEqual("Documents", self.drive.name)

    def test_download(self):
        self.drive.download("temp/dummy.txt")

    def test_files(self):
        self.drive.tree()


from davidkhala.sharepoint.http import Graph as GraphHTTP


class HTTPTestCase(unittest.TestCase):
    def setUp(self):
        self.client = GraphHTTP(tenant_id)
        self.client.with_client_secret(client_id, client_secret)

    def test_get_item(self):
        site = 'davidkhalahotmail.sharepoint.com,3f75f1a6-1239-4862-b14d-367c1c865604,d786840e-231b-4b8a-b38a-19e174ebb25d'
        drive = 'b!pvF1PzkSYkixTTZ8HIZWBA6EhtcbI4pLs4oZ4XTrsl1HYF74jUSjSr-0WF8hBZy5'

        r = self.client.get_item_id(site, drive, 'temp/dummy.txt')
        self.assertEqual('01GJ54VSTFVTWRRKW4LBCZQO76GZJXPFAW', r)
    def test_stream_item(self):
        site = 'davidkhalahotmail.sharepoint.com,3f75f1a6-1239-4862-b14d-367c1c865604,d786840e-231b-4b8a-b38a-19e174ebb25d'
        drive = 'b!pvF1PzkSYkixTTZ8HIZWBA6EhtcbI4pLs4oZ4XTrsl1HYF74jUSjSr-0WF8hBZy5'
        self.client.open()
        self.client.stream(site, drive, 'temp/dummy.txt')
        self.client.close()

if __name__ == '__main__':
    unittest.main()
