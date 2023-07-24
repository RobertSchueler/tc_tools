import xml.etree.ElementTree as ElementTree
from .svg_elements import SVGRoot, SVGElement


def extract_svg_root_from_element_tree(etree: ElementTree) -> SVGRoot:
    return SVGRoot([SVGElement() for _ in etree.getroot()])
