import unittest
from unittest.mock import patch

from factories import PandasDataframeFactory, ElementTreeFactory
from factories.values import lowercase_string
from processor import base_process, base_process_single_item

import persistence
import os


class TestProcessor(unittest.TestCase):
    def setUp(self) -> None:
        self.pandas_dataframe = PandasDataframeFactory().build()
        self.element_tree = ElementTreeFactory().build()

    def test_base_process_should_not_throw_errors(self)->None:
        opt_str = lowercase_string()()
        exc_str = lowercase_string()()
        svg_str = lowercase_string()()
        with patch("pandas.read_excel") as pandas_read_excel_mock:
            pandas_read_excel_mock.return_value = self.pandas_dataframe
            with patch("os.system") as os_system_mock:
                with patch("xml.etree.ElementTree.parse") as etree_parse_mock:
                    etree_parse_mock.return_value = self.element_tree
                    with patch("processor.processor.parse_configuration_file") as parse_configurations_file_mock:
                        base_process(opt_str, exc_str, svg_str, base_process_single_item)

        parse_configurations_file_mock.assert_called_once_with(opt_str)
        pandas_read_excel_mock.assert_called_once_with(exc_str)
        os_system_mock.assert_called()
        etree_parse_mock.assert_called()
