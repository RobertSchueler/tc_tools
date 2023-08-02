import unittest
from xml.etree.ElementTree import Element, ElementTree

from mapper import extract_svg_root_from_element_tree
from TestDataFactory import TestDataFactory


class TestToSVGMapper(unittest.TestCase):
    def setUp(self) -> None:
        self.etree = TestDataFactory.create_element_tree(3)

    def test_extract_svg_root_from_element_tree_should_have_as_much_children_as_etree(self) -> None:
        svg_root = extract_svg_root_from_element_tree(self.etree)
        self.assertEqual(len([_ for _ in svg_root]), 3)
