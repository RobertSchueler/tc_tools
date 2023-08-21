import os
import unittest
from unittest.mock import patch

from processor import base_process, base_process_single_item

from TestDataFactory import TestDataFactory


class TestProcessor(unittest.TestCase):
    def test_base_process_should_not_throw_errors(self)->None:
        with patch("pandas.read_excel") as pandas_read_excel_mock:
            pandas_read_excel_mock.return_value = TestDataFactory.create_pd_dataframe()
            with patch("os.system") as os_system_mock:
                with patch("xml.etree.ElementTree.parse") as etree_parse_mock:
                    etree_parse_mock.return_value = TestDataFactory.create_element_tree(3)
                    base_process("ink", "exc", "svg", base_process_single_item)

        pandas_read_excel_mock.assert_called_once()
        os_system_mock.assert_called()
        etree_parse_mock.assert_called()
