import unittest
from unittest.mock import patch
from xml.etree.ElementTree import Element

from tc_tools.factories import ElementTreeFactory, ElementFactory, SVGElementFactory
from tc_tools.factories.svg_collection_factory import SVGCollectionFactory
from tc_tools.factories.svg_image_factory import SVGImageFactory
from tc_tools.factories.svg_text_factory import SVGTextFactory
from tc_tools.factories.values import lowercase_string, list_of, integer, \
    positive_integer, floating
from tc_tools.mapper import merge_svg_root_and_element_tree, SVGRoot, \
    merge_svg_and_element, SVGImage
from tc_tools.mapper.to_svg_mapper import IMAGE_TAG

class TestToElementTreeMapper(unittest.TestCase):
    def setUp(self) -> None:
        self.etree = ElementTreeFactory().build()
        self.element = ElementFactory().build()
        self.href = lowercase_string()()
        self.image_tag = lowercase_string(ending_with=IMAGE_TAG)()
        self.image_element = ElementFactory().build(
            tag=self.image_tag, fixed_attributes={
                "href": self.href,
                "x": str(floating()()),
                "y": str(floating()()),
                "width": str(floating()()),
                "height": str(floating()())
            }
        )
        self.svg_element = SVGElementFactory().build()
        self.svg_image = SVGImageFactory().build()

        self.grandchildren = list_of(SVGElementFactory().build)()
        self.children = [
            SVGCollectionFactory().build(children=self.grandchildren),
            SVGElementFactory().build()
        ]
        self.recursive_collection = SVGCollectionFactory().build(
            children=self.children
        )

        self.element_grandchildren = [
            ElementFactory().build() for _ in range(len(self.grandchildren))
        ]
        self.element_children = [
            ElementFactory().build_with_children(
                children=self.element_grandchildren
            ),
            ElementFactory().build()
        ]
        self.recursive_element = ElementFactory().build_with_children(
            children=self.element_children
        )

    def test_merge_svg_root_and_element_tree_should_throw_no_errors(self) -> None:
        original_svg_root = SVGRoot([])
        merge_svg_root_and_element_tree(original_svg_root, self.etree)

    def test_merge_svg_and_element_should_throw_no_errors(self) -> None:
        merge_svg_and_element(self.svg_element, self.element)

    def test_merge_svg_and_element_should_merge_svg_images_and_images(self) -> None:
        image_width = positive_integer()()
        image_height = positive_integer()()
        with patch("imagesize.get") as imagesize_patch:
            imagesize_patch.return_value = (image_width, image_height)
            merged_element = merge_svg_and_element(self.svg_image, self.image_element)
        href = get_attribute_from_element(merged_element, "href")
        self.assertEqual(href, self.svg_image.href)

        new_x = float(get_attribute_from_element(merged_element, "x"))
        new_y = float(get_attribute_from_element(merged_element, "y"))
        new_width = float(get_attribute_from_element(merged_element, "width"))
        new_height = float(get_attribute_from_element(merged_element, "height"))

        old_x = float(get_attribute_from_element(self.image_element, "x"))
        old_y = float(get_attribute_from_element(self.image_element, "y"))
        old_width = float(get_attribute_from_element(self.image_element, "width"))
        old_height = float(get_attribute_from_element(self.image_element, "height"))

        # check that new image in in the center
        self.assertEqual(new_x - old_x, new_width - old_width)
        self.assertEqual(new_y - old_y, new_height - old_height)
        # check that new image is inside old image
        self.assertGreaterEqual(new_x, old_x)
        self.assertGreaterEqual(new_y, old_y)
        self.assertLessEqual(new_width, old_width)
        self.assertLessEqual(new_height, old_height)

        # check that new image is maximally scaled
        self.assertTrue(old_width - new_width < 0.01 or old_height - new_height < 0.01)

    def test_merge_svg_and_element_should_ignore_non_existent_images(self) -> None:
        with patch("imagesize.get") as imagesize_patch:
            imagesize_patch.side_effect = FileNotFoundError("Failed to get image size")
            merged_element = merge_svg_and_element(self.svg_image, self.image_element)
        href = get_attribute_from_element(merged_element, "href")
        self.assertEqual(href, self.svg_image.href)

        new_x = float(get_attribute_from_element(merged_element, "x"))
        new_y = float(get_attribute_from_element(merged_element, "y"))
        new_width = float(get_attribute_from_element(merged_element, "width"))
        new_height = float(get_attribute_from_element(merged_element, "height"))

        old_x = float(get_attribute_from_element(self.image_element, "x"))
        old_y = float(get_attribute_from_element(self.image_element, "y"))
        old_width = float(get_attribute_from_element(self.image_element, "width"))
        old_height = float(get_attribute_from_element(self.image_element, "height"))

        self.assertEqual(old_x, new_x)
        self.assertEqual(old_y, new_y)
        self.assertEqual(old_height, new_height)
        self.assertEqual(old_width, new_width)

    def test_merge_svg_and_element_should_recursively_merge(self) -> None:
        merged_element = merge_svg_and_element(
            self.recursive_collection, self.recursive_element
        )
        merged_element_children = [child for child in merged_element]
        merged_element_grandchildren = [
            grandchild for child in merged_element_children for grandchild in child
        ]

        self.assertEqual(len(merged_element_grandchildren), len(self.grandchildren))

    def test_merge_svg_and_element_should_merge_svg_text_and_texts(self) -> None:
        element_to_merge = ElementFactory().build()
        svg_text_to_merge = SVGTextFactory().build()

        merged_element = merge_svg_and_element(svg_text_to_merge, element_to_merge)

        self.assertEqual(merged_element.text, "")
        self.assertEqual(merged_element[0].text, svg_text_to_merge.get_text_content())

    def test_merge_svg_and_element_should_merge_svg_text_and_multiline_texts(self) -> None:
        element_to_merge = ElementFactory().build()
        svg_text_to_merge = SVGTextFactory().build(text_content = "First line\nSecond line\nThird line")

        merged_element = merge_svg_and_element(svg_text_to_merge, element_to_merge)

        self.assertEqual(merged_element.text, "")
        self.assertEqual(3, len(merged_element))
        self.assertEqual(merged_element[0].text, "First line")
        self.assertEqual(merged_element[1].text, "Second line")
        self.assertEqual(merged_element[2].text, "Third line")


def get_attribute_from_element(element: Element, param) -> str:
    attrib_key = [key for key in element.attrib.keys() if key.endswith(param)][0]
    return element.attrib.get(attrib_key)
