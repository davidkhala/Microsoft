import unittest

from davidkhala.purview.scan import Scan


class ScanTestCase(unittest.TestCase):
    def setUp(self):
        self.s = Scan()
    def test_something(self):
        pass


if __name__ == '__main__':
    unittest.main()
