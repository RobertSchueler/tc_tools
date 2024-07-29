import unittest
from unittest.mock import patch

from tc_tools.factories import PandasDataframeFactory
from tc_tools.persistence import create_simple_data_source_from_excel


class TestExcelSheetMethods(unittest.TestCase):
    def setUp(self) -> None:
        self.pandas_dataframe_content_dict = PandasDataframeFactory().build_pandas_conform_dict()
        self.pandas_dataframe = PandasDataframeFactory().build(
            row_data=self.pandas_dataframe_content_dict
        )

    def test_create_simple_data_source_from_excel_should_return_simple_data_source(self):
        with patch("pandas.read_excel") as pandas_read_excel_mock:
            pandas_read_excel_mock.return_value = self.pandas_dataframe
            data_source = create_simple_data_source_from_excel("excel.xmhl")

        pandas_read_excel_mock.assert_called_once_with("excel.xmhl")

        for entry_idx, entry in enumerate(data_source):
            for key, value in self.pandas_dataframe_content_dict.items():
                self.assertEqual(entry[key], value[entry_idx])
