from xml.etree.ElementTree import ElementTree, Element

from mapper import SVGElement


class TestDataFactory():
    @staticmethod
    def create_element_tree(n_children: int) -> ElementTree:
        children = [Element("child") for _ in range(n_children)]
        parent = Element("parent")
        for child in children:
            parent.append(child)

        return ElementTree(parent)

    @staticmethod
    def create_element():
        return Element("child")

    @staticmethod
    def create_svg_element():
        return SVGElement()
