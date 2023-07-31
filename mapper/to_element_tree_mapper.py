import copy
from xml.etree.ElementTree import ElementTree, Element
from mapper import SVGRoot, SVGElement


def merge_svg_root_and_element_tree(root: SVGRoot, etree: ElementTree) -> ElementTree:
    copied_etree = copy.deepcopy(etree)
    for svg_child, etree_child in zip(root, copied_etree.getroot()):
        merge_svg_and_element(svg_child, etree_child)
    return copied_etree


def merge_svg_and_element(svg_element: SVGElement, element: Element) -> Element:
    return element
