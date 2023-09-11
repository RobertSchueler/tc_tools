import unittest
from xml.etree.ElementTree import Element, ElementTree

from factories import ElementTreeFactory, ElementFactory
from factories.values import lowercase_string, full_string
from mapper import extract_svg_root_from_element_tree, SVGRoot, SVGElement, SVGImage
from mapper.to_svg_mapper import LABEL_KEY, extract_svg_element_from_element, IMAGE_TAG, \
    HREF_KEY, extract_svg_image_from_element


class TestToSVGMapper(unittest.TestCase):
    def setUp(self) -> None:
        self.etree: ElementTree = ElementTreeFactory().build()
        self.inkscape_label = lowercase_string()()
        self.element_with_inkscape_label = ElementFactory().build(
            fixed_attributes={LABEL_KEY: self.inkscape_label}
        )

        self.href_value = full_string()()
        self.element_with_image_tag = ElementFactory().build(
            tag=IMAGE_TAG, fixed_attributes={HREF_KEY: self.href_value}
        )

    def test_extract_svg_root_from_element_tree_should_have_as_much_children_as_etree(self) -> None:
        svg_root: SVGRoot = extract_svg_root_from_element_tree(self.etree)
        expected_len: int = len([_ for _ in self.etree.getroot()])
        actual_len: int = len([_ for _ in svg_root])
        self.assertEqual(expected_len, actual_len)

    def test_extract_svg_element_from_element_should_extract_inkscape_labels(self) -> None:
        generated_svg_element: SVGElement = extract_svg_element_from_element(
            self.element_with_inkscape_label
        )
        self.assertEqual(
            generated_svg_element.get_label(),
            self.inkscape_label
        )

    def test_extract_extract_svg_element_from_element_should_extract_href_from_images(self) -> None:
        generated_svg_image: SVGImage = extract_svg_image_from_element(
            self.element_with_image_tag
        )
        self.assertEqual(
            self.href_value,
            generated_svg_image.get_href()
        )
