import xml.etree.ElementTree as ElementTree
from .svg_elements import SVGRoot, SVGElement

LABEL_KEY: str = "inkscape:label"


def extract_svg_root_from_element_tree(etree: ElementTree) -> SVGRoot:
    children: list[SVGElement] = [
        extract_svg_element_from_element(element) for element in etree.getroot()
    ]
    return SVGRoot(children)


def extract_svg_element_from_element(element: ElementTree.Element) -> SVGElement:
    svg_element: SVGElement = SVGElement()
    for attrib, value in element.attrib.items():
        if attrib == LABEL_KEY:
            svg_element.set_label(value)
            break

    return svg_element
