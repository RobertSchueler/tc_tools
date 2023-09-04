import unittest

from factories import ElementTreeFactory, ElementFactory, SVGElementFactory
from mapper import merge_svg_root_and_element_tree, SVGRoot, merge_svg_and_element


class TestToElementTreeMapper(unittest.TestCase):
    def setUp(self) -> None:
        self.etree = ElementTreeFactory().build()
        self.element = ElementFactory().build()
        self.svg_element = SVGElementFactory().build()

    def test_merge_svg_root_and_element_tree_should_throw_no_errors(self) -> None:
        original_svg_root = SVGRoot([])
        merge_svg_root_and_element_tree(original_svg_root, self.etree)

    def test_merge_svg_and_element_should_throw_no_errors(self) -> None:
        merge_svg_and_element(self.element, self.svg_element)
