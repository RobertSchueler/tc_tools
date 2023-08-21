import unittest
from unittest.mock import patch

from TestDataFactory import TestDataFactory
from processor import base_process, base_process_single_item

import persistence
import os


class TestProcessor(unittest.TestCase):
    def test_base_process_should_not_throw_errors(self)->None:
        with patch("pandas.read_excel") as pandas_read_excel_mock:
            pandas_read_excel_mock.return_value = TestDataFactory.create_pd_dataframe()
            with patch("os.system") as os_system_mock:
                with patch("xml.etree.ElementTree.parse") as etree_parse_mock:
                    etree_parse_mock.return_value = TestDataFactory.create_element_tree(3)
                    with patch("processor.processor.parse_configuration_file") as parse_configurations_file_mock:
                        base_process("opt", "exc", "svg", base_process_single_item)

        parse_configurations_file_mock.assert_called_once_with("opt")
        pandas_read_excel_mock.assert_called_once_with("exc")
        os_system_mock.assert_called()
        etree_parse_mock.assert_called()
