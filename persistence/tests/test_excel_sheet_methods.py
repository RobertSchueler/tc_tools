import unittest
from unittest.mock import patch

from TestDataFactory import TestDataFactory
from persistence import create_simple_data_source_from_excel


class TestExcelSheetMethods(unittest.TestCase):
    def test_create_simple_data_source_from_excel_should_return_simple_data_source(self):
        with patch("pandas.read_excel") as pandas_read_excel_mock:
            pandas_read_excel_mock.return_value = TestDataFactory.create_pd_dataframe()
            data_source = create_simple_data_source_from_excel("excel.xmhl")

        pandas_read_excel_mock.assert_called_once_with("excel.xmhl")
        expected_data = [{"a": 1, "b": "a"}, {"a": 2, "b": "b"}, {"a": 3, "b": "c"}, {"a": 4, "b": "d"}]

        for entry, expected_entry in zip(data_source, expected_data):
            self.assertEqual(entry, expected_entry)