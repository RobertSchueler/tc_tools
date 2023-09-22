import unittest
from unittest.mock import patch

from factories import PandasDataframeFactory, ElementTreeFactory, values
from factories.svg_image_factory import SVGImageFactory
from factories.svg_root_factory import SVGRootFactory
from factories.values import lowercase_string, dict_with_fixed_keys
from processor import base_process, base_process_single_item

import persistence
import os


class TestProcessor(unittest.TestCase):
    def setUp(self) -> None:
        self.pandas_dataframe = PandasDataframeFactory().build()
        self.element_tree = ElementTreeFactory().build()

        self.label = lowercase_string()()
        self.svg_image = SVGImageFactory().build(label=self.label)
        self.svg_root_with_image = SVGRootFactory().build(children=[self.svg_image])
        self.href = lowercase_string()()
        self.data_for_image_with_href = {f"{self.label}.href": self.href}
        self.data_for_image_without_href = {self.label: self.href}

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

    def test_base_process_single_item_should_process_images_correctly(self):

        base_process_single_item(self.svg_root_with_image, self.data_for_image_with_href)

        self.assertEqual(self.href, self.svg_image.get_href())

    def test_base_process_single_item_should_process_href_when_no_attribute_is_given(self):

        base_process_single_item(self.svg_root_with_image, self.data_for_image_without_href)

        self.assertEqual(self.href, self.svg_image.get_href())
