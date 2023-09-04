import unittest
from xml.etree.ElementTree import Element, ElementTree

from factories import ElementTreeFactory
from mapper import extract_svg_root_from_element_tree, SVGRoot


class TestToSVGMapper(unittest.TestCase):
    def setUp(self) -> None:
        self.etree: ElementTree = ElementTreeFactory().build()

    def test_extract_svg_root_from_element_tree_should_have_as_much_children_as_etree(self) -> None:
        svg_root: SVGRoot = extract_svg_root_from_element_tree(self.etree)
        expected_len: int = len([_ for _ in self.etree.getroot()])
        actual_len: int = len([_ for _ in svg_root])
        self.assertEqual(expected_len, actual_len)
