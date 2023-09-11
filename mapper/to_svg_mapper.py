import xml.etree.ElementTree as ElementTree

from . import SVGImage
from .svg_elements import SVGRoot, SVGElement

LABEL_KEY: str = "inkscape:label"
HREF_KEY: str = "xlink:href"

IMAGE_TAG: str = "image"


def extract_svg_root_from_element_tree(etree: ElementTree) -> SVGRoot:
    children: list[SVGElement] = [
        extract_svg_element_from_element(element) for element in etree.getroot()
    ]
    return SVGRoot(children)


def extract_svg_element_from_element(element: ElementTree.Element) -> SVGElement:
    if element_is_image(element):
        return extract_svg_image_from_element(element)

    return extract_base_svg_element_from_element(element)


# private
def extract_svg_image_from_element(element: ElementTree.Element) -> SVGImage:
    svg_image: SVGImage = SVGImage()
    set_base_values_to_svg_element(element, svg_image)
    for attrib, value in element.attrib.items():
        if attrib == HREF_KEY:
            svg_image.set_href(value)
            break
    return svg_image


# private
def extract_base_svg_element_from_element(
        element: ElementTree.Element
) -> SVGElement:
    svg_element: SVGElement = SVGElement()
    set_base_values_to_svg_element(element, svg_element)
    return svg_element


# private
def set_base_values_to_svg_element(
        element: ElementTree.Element,
        svg_element: SVGElement
) -> None:
    for attrib, value in element.attrib.items():
        if attrib == LABEL_KEY:
            svg_element.set_label(value)
            break


# private
def element_is_image(element: ElementTree.Element) -> bool:
    return element.tag == IMAGE_TAG
