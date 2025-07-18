import unittest
from unittest.mock import patch

from tc_tools.factories import PandasDataframeFactory, ElementTreeFactory
from tc_tools.factories.svg_image_factory import SVGImageFactory
from tc_tools.factories.svg_root_factory import SVGRootFactory
from tc_tools.factories.svg_text_factory import SVGTextFactory
from tc_tools.factories.values import lowercase_string, full_string, integer
from tc_tools.processor import base_process, base_process_single_item


class TestProcessor(unittest.TestCase):
    def test_base_process_should_not_throw_errors(self) -> None:
        pandas_dataframe = PandasDataframeFactory().build()
        element_tree = ElementTreeFactory().build()

        opt_str = lowercase_string()()
        exc_str = lowercase_string()()
        svg_str = lowercase_string()()
        with patch("pandas.read_excel") as pandas_read_excel_mock:
            pandas_read_excel_mock.return_value = pandas_dataframe
            with patch("os.system") as os_system_mock:
                with patch("xml.etree.ElementTree.parse") as etree_parse_mock:
                    etree_parse_mock.return_value = element_tree
                    with patch("tc_tools.processor.processor.parse_configuration_file") as parse_configurations_file_mock:
                        base_process(opt_str, exc_str, svg_str, base_process_single_item)

        parse_configurations_file_mock.assert_called_once_with(opt_str)
        pandas_read_excel_mock.assert_called_once_with(exc_str)
        os_system_mock.assert_called()
        etree_parse_mock.assert_called()

    def test_base_process_single_item_should_process_images_correctly(self):
        label = lowercase_string()()
        href = full_string()()

        svg_image = SVGImageFactory().build(label=label)
        svg_root_with_image = SVGRootFactory().build(children=[svg_image])

        data_for_image_with_href = {f"{label}.href": href}

        base_process_single_item(svg_root_with_image, data_for_image_with_href)

        self.assertEqual(href, svg_image.get_href())

    def test_base_process_single_item_should_process_href_when_no_attribute_is_given(self):

        label = lowercase_string()()
        href = full_string()()

        svg_image = SVGImageFactory().build(label=label)
        svg_root_with_image = SVGRootFactory().build(children=[svg_image])

        data_for_image_without_href = {f"{label}": href}

        base_process_single_item(svg_root_with_image, data_for_image_without_href)

        self.assertEqual(href, svg_image.get_href())

    def test_base_process_single_item_should_process_texts_correctly(self):
        label = lowercase_string()()
        svg_text = SVGTextFactory().build(label=label)
        svg_root_with_text = SVGRootFactory().build(children=[svg_text])

        text_content = full_string()()

        data_for_text_with_text_content = {f"{label}.text": text_content}

        base_process_single_item(svg_root_with_text, data_for_text_with_text_content)

        self.assertEqual(text_content, svg_text.get_text_content())

    def test_base_process_single_item_should_process_texts_correctly_when_no_attribute_is_given(self):
        label = lowercase_string()()
        svg_text = SVGTextFactory().build(label=label)
        svg_root_with_text = SVGRootFactory().build(children=[svg_text])

        text_content = full_string()()

        data_for_text_with_text_content = {f"{label}": text_content}

        base_process_single_item(svg_root_with_text, data_for_text_with_text_content)

        self.assertEqual(text_content, svg_text.get_text_content())

    def test_base_process_single_item_should_process_numeric_values_correctly(self):
        label = lowercase_string()()
        svg_text = SVGTextFactory().build(label=label)
        svg_root_with_text = SVGRootFactory().build(children=[svg_text])

        numeric_value = integer()()

        data_for_text_with_numeric_content = {f"{label}": numeric_value}

        base_process_single_item(svg_root_with_text, data_for_text_with_numeric_content)

        self.assertEqual(str(numeric_value), svg_text.get_text_content())