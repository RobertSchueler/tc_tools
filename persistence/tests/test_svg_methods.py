import unittest
from unittest.mock import patch, Mock
import xml.etree.ElementTree as ElementTree

from ..svg_methods import parse_svg_to_element_tree, write_element_tree_to_svg


class TestSVGMethods(unittest.TestCase):
    def test_parse_svg_to_element_tree_should_call_parse_from_elemente_tree_lib(self):
        mock_return_value = ElementTree.ElementTree()
        with patch("xml.etree.ElementTree.parse") as etree_parse_mock:
            etree_parse_mock.return_value = mock_return_value
            result = parse_svg_to_element_tree("path")

        etree_parse_mock.assert_called_once_with("path")
        self.assertEqual(result, mock_return_value)

    def test_write_element_tree_to_svg_should_call_write_from_elemente_tree_lib(self):
        etree = ElementTree.ElementTree()
        etree.write = Mock()
        write_element_tree_to_svg(etree, "path")
        etree.write.assert_called_once_with("path")
