import unittest

from mapper import merge_svg_root_and_element_tree, SVGRoot, merge_svg_and_element
from TestDataFactory import TestDataFactory


class TestToElementTreeMapper(unittest.TestCase):
    def setUp(self) -> None:
        self.etree = TestDataFactory.create_element_tree(3)
        self.element = TestDataFactory.create_element()
        self.svg_element = TestDataFactory.create_svg_element()

    def test_merge_svg_root_and_element_tree_should_throw_no_errors(self) -> None:
        original_svg_root = SVGRoot([])
        merge_svg_root_and_element_tree(original_svg_root, self.etree)

    def test_merge_svg_and_element_should_throw_no_errors(self) -> None:
        merge_svg_and_element(self.element, self.svg_element)
