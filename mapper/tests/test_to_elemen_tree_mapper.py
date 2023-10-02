import unittest

from factories import ElementTreeFactory, ElementFactory, SVGElementFactory
from factories.svg_collection_factory import SVGCollectionFactory
from factories.svg_image_factory import SVGImageFactory
from factories.svg_text_factory import SVGTextFactory
from factories.values import lowercase_string, list_of
from mapper import merge_svg_root_and_element_tree, SVGRoot, merge_svg_and_element
from mapper.to_svg_mapper import IMAGE_TAG, TEXT_TAG


class TestToElementTreeMapper(unittest.TestCase):
    def setUp(self) -> None:
        self.etree = ElementTreeFactory().build()
        self.element = ElementFactory().build()
        self.href = lowercase_string()()
        self.image_tag = lowercase_string(ending_with=IMAGE_TAG)()
        self.image_element = ElementFactory().build(
            tag=self.image_tag, fixed_attributes={"href": self.href}
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
        merged_element = merge_svg_and_element(self.svg_image, self.image_element)
        self.assertEqual(merged_element.get("href"), self.svg_image.get_href())

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

        self.assertEqual(merged_element.text, svg_text_to_merge.get_text_content())


