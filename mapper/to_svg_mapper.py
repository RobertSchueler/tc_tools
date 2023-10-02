import xml.etree.ElementTree as ElementTree

from . import SVGImage, SVGCollection
from .svg_elements import SVGRoot, SVGElement, SVGText

LABEL_KEY: str = "label"
HREF_KEY: str = "href"

IMAGE_TAG: str = "image"
TEXT_TAG: str = "text"


# public
def extract_svg_root_from_element_tree(etree: ElementTree) -> SVGRoot:
    children: list[SVGElement] = [
        extract_svg_element_from_element(element) for element in etree.getroot()
    ]
    return SVGRoot(children)


# public
def extract_svg_element_from_element(element: ElementTree.Element) -> SVGElement:
    children = get_children_of_element(element)

    if element_is_text(element):
        return extract_svg_text_from_element(element, children)

    if element_is_collection(children):
        return extract_svg_collection_from_element(element, children)

    if element_is_image(element):
        return extract_svg_image_from_element(element)

    return extract_base_svg_element_from_element(element)


def get_children_of_element(element: ElementTree.Element) -> list[ElementTree.Element]:
    return [child for child in element]


def extract_svg_text_from_element(element: ElementTree.Element, children: list[ElementTree.Element]) -> SVGText:
    svg_text = SVGText()
    set_base_values_to_svg_element(element, svg_text)
    text_content = extract_text_from_element(element) + "".join(
        [extract_text_from_element(child) for child in children]
    )
    svg_text.set_text_content(text_content)

    return svg_text


def extract_text_from_element(element: ElementTree.Element) -> str:
    if element.text is None:
        return ""
    return element.text


def extract_svg_collection_from_element(element: ElementTree.Element, children: list[ElementTree.Element]) -> SVGCollection:
    svg_collection = SVGCollection()
    set_base_values_to_svg_element(element, svg_collection)

    svg_children = [extract_svg_element_from_element(child) for child in children]
    svg_collection.add_children(svg_children)

    return svg_collection


def extract_svg_image_from_element(element: ElementTree.Element) -> SVGImage:
    svg_image: SVGImage = SVGImage()
    set_base_values_to_svg_element(element, svg_image)
    for attrib, value in element.attrib.items():
        if attrib.endswith(HREF_KEY):
            svg_image.set_href(value)
            break
    return svg_image


def extract_base_svg_element_from_element(
        element: ElementTree.Element
) -> SVGElement:
    svg_element: SVGElement = SVGElement()
    set_base_values_to_svg_element(element, svg_element)
    return svg_element


def set_base_values_to_svg_element(
        element: ElementTree.Element,
        svg_element: SVGElement
) -> None:
    for attrib, value in element.attrib.items():
        if attrib.endswith(LABEL_KEY):
            svg_element.set_label(value)
            break


def element_is_image(element: ElementTree.Element) -> bool:
    return element.tag.endswith(IMAGE_TAG)


def element_is_text(element):
    return element.tag.endswith(TEXT_TAG)


def element_is_collection(children: list[ElementTree.Element]) -> bool:
    return len(children) > 0
