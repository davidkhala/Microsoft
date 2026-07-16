import unittest
from pathlib import Path

from davidkhala.microsoft.excel.raw import to_csv


class ToCSVTest(unittest.TestCase):
    def test_maxims(self):
        source = Path(__file__).parent / 'fixtures' / 'SS_item_hierarchy.xlsx'
        sink = Path(__file__).parent / 'artifacts' / 'SS_item_hierarchy.csv'
        to_csv(source, sink)
