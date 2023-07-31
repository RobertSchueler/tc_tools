from xml.etree.ElementTree import ElementTree, Element

import pandas as pd

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

    @staticmethod
    def create_pd_dataframe():
        return pd.DataFrame({"a": [1,2,3,4], "b": ["a", "b", "c", "d"]})
