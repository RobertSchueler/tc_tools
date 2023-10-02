import unittest
from xml.etree.ElementTree import Element, ElementTree

from factories import ElementTreeFactory, ElementFactory
from factories.values import lowercase_string, full_string, list_of
from mapper import extract_svg_root_from_element_tree, SVGRoot, SVGElement, SVGImage, \
    SVGCollection, SVGText
from mapper.to_svg_mapper import LABEL_KEY, extract_svg_element_from_element, IMAGE_TAG, \
    HREF_KEY, TEXT_TAG


class TestToSVGMapper(unittest.TestCase):
    def test_extract_svg_root_from_element_tree_should_have_as_much_children_as_etree(self) -> None:
        etree: ElementTree = ElementTreeFactory().build()

        svg_root: SVGRoot = extract_svg_root_from_element_tree(etree)
        expected_len: int = len([_ for _ in etree.getroot()])
        actual_len: int = len([_ for _ in svg_root])
        self.assertEqual(expected_len, actual_len)

    def test_extract_svg_element_from_element_should_extract_inkscape_labels(self) -> None:
        inkscape_label = lowercase_string()()
        element_with_inkscape_label = ElementFactory().build(
            fixed_attributes={LABEL_KEY: inkscape_label}
        )

        generated_svg_element: SVGElement = extract_svg_element_from_element(
            element_with_inkscape_label
        )
        self.assertEqual(
            generated_svg_element.get_label(),
            inkscape_label
        )

    def test_extract_svg_element_from_element_should_extract_attributes_from_images(self) -> None:
        href_value = full_string()()
        image_tag = lowercase_string(ending_with=IMAGE_TAG)()
        label = lowercase_string()()
        element_with_image_tag = ElementFactory().build(
            tag=image_tag, fixed_attributes={
                LABEL_KEY: label,
                HREF_KEY: href_value
            }
        )

        generated_svg_image = extract_svg_element_from_element(
            element_with_image_tag
        )

        self.assertEqual(generated_svg_image.__class__, SVGImage)
        if not isinstance(generated_svg_image, SVGImage):
            # to make type safety happy
            return

        self.assertEqual(
            label,
            generated_svg_image.get_label()
        )

        self.assertEqual(
            href_value,
            generated_svg_image.get_href()
        )

    def test_extract_svg_element_from_element_tree_should_work_recursively(self) -> None:
        label = lowercase_string()()
        grandchildren = list_of(ElementFactory().build)()
        child_element_with_children = ElementFactory().build_with_children(
            fixed_attributes={
                LABEL_KEY: label
            },
            children=grandchildren
        )
        child_element_without_children = ElementFactory().build()
        recursive_etree = ElementTreeFactory().build(
            children=[
                child_element_with_children,
                child_element_without_children
            ]
        )

        generated_svg_root = extract_svg_root_from_element_tree(recursive_etree)
        children = [child for child in generated_svg_root]
        grandchildren = [grandchild for grandchild in children[0]]

        self.assertEqual(children[0].__class__, SVGCollection)
        self.assertEqual(children[0].get_label(), label)
        self.assertEqual(children[1].__class__, SVGElement)
        self.assertEqual(len(grandchildren), len(grandchildren))

    def test_extract_svg_element_from_element_should_extract_text_content_from_text(self) -> None:
        tag = lowercase_string(ending_with="text")()
        label = lowercase_string()()
        root_content = full_string()()
        text_contents = list_of(full_string())()
        children = [
            ElementFactory().build(text_content=text_content)
            for text_content in text_contents
        ]
        text_element = ElementFactory().build(
            tag=tag,
            fixed_attributes={
                LABEL_KEY: label
            },
            children=children,
            text_content=root_content
        )

        generated_svg_text = extract_svg_element_from_element(text_element)

        self.assertEqual(generated_svg_text.__class__, SVGText)
        if not isinstance(generated_svg_text, SVGText):
            # to make type safety happy
            return

        self.assertEqual(generated_svg_text.get_label(), label)

        expected_text_content = root_content
        for child_content in text_contents:
            expected_text_content += child_content

        self.assertEqual(generated_svg_text.get_text_content(), expected_text_content)

    def test_extract_svg_element_from_element_should_extract_empty_strings_from_non_set_text(
            self) -> None:
        tag = lowercase_string(ending_with=TEXT_TAG)()
        label = lowercase_string()()
        text_contents = list_of(lambda: None)()
        children = [
            ElementFactory().build(text_content=text_content)
            for text_content in text_contents
        ]
        text_element = ElementFactory().build(
            tag=tag,
            fixed_attributes={
                LABEL_KEY: label
            },
            children=children,
            text_content=None
        )

        generated_svg_text = extract_svg_element_from_element(text_element)

        self.assertEqual(generated_svg_text.__class__, SVGText)
        if not isinstance(generated_svg_text, SVGText):
            # to make type safety happy
            return

        expected_text_content = ""

        self.assertEqual(generated_svg_text.get_text_content(),
                         expected_text_content)

