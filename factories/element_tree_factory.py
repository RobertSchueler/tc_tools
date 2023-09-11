from xml.etree.ElementTree import Element, ElementTree

from .base_factory import BaseFactory
from .element_factory import ElementFactory
from .values import lowercase_string, list_of


class ElementTreeFactory(BaseFactory):
    def build(self, **kwargs) -> ElementTree:
        return super().build(
            [
                ("rootname", lowercase_string()),
                ("children", list_of(ElementFactory().build))
            ],
            **kwargs
        )

    def generate(self, rootname: str, children: list[Element]) -> ElementTree:
        parent = Element(rootname)
        for child in children:
            parent.append(child)
        return ElementTree(parent)
