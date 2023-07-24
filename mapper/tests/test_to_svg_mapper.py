import unittest
from xml.etree.ElementTree import Element, ElementTree

from mapper import extract_svg_root_from_element_tree


class TestToSVGMapper(unittest.TestCase):
    def setUp(self) -> None:
        children = [Element("child"), Element("child"), Element("child")]
        parent = Element("parent")
        for child in children:
            parent.append(child)
        self.etree = ElementTree(parent)

    def test_extract_svg_root_from_element_tree_should_have_as_much_children_as_etree(self) -> None:
        svg_root = extract_svg_root_from_element_tree(self.etree)
        self.assertEqual(len([_ for _ in svg_root]), 3)
