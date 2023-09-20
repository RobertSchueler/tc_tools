import unittest

from factories import ElementTreeFactory, ElementFactory, SVGElementFactory
from factories.svg_image_factory import SVGImageFactory
from factories.values import lowercase_string
from mapper import merge_svg_root_and_element_tree, SVGRoot, merge_svg_and_element
from mapper.to_svg_mapper import IMAGE_TAG


class TestToElementTreeMapper(unittest.TestCase):
    def setUp(self) -> None:
        self.etree = ElementTreeFactory().build()
        self.element = ElementFactory().build()
        self.href = lowercase_string()()
        self.image_element = ElementFactory().build(tag=IMAGE_TAG, fixed_attributes={"href": self.href})
        self.svg_element = SVGElementFactory().build()
        self.svg_image = SVGImageFactory().build()

    def test_merge_svg_root_and_element_tree_should_throw_no_errors(self) -> None:
        original_svg_root = SVGRoot([])
        merge_svg_root_and_element_tree(original_svg_root, self.etree)

    def test_merge_svg_and_element_should_throw_no_errors(self) -> None:
        merge_svg_and_element(self.svg_element, self.element)

    def test_merge_svg_and_element_should_merge_svg_images_and_images(self) -> None:
        merged_element = merge_svg_and_element(self.svg_image, self.image_element)
        self.assertEqual(merged_element.get("href"), self.svg_image.get_href())