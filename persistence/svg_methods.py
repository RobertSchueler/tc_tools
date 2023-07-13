import xml.etree.ElementTree as ElementTree


def parse_svg_to_element_tree(path: str) -> ElementTree:
    return ElementTree.parse(path)


def write_element_tree_to_svg(etree: ElementTree, path: str) -> None:
    etree.write(path)
