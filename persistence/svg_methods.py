import xml.etree.ElementTree as ElementTree


def parse_svg_to_element_tree(path: str) -> ElementTree:
    return ElementTree.parse(path)
