from xml.etree.ElementTree import Element

from .base_factory import BaseFactory
from .values import lowercase_string


class ElementFactory(BaseFactory):

    def build(self, **fixed_parameter):
        return super().build(
            [
                ("name", lowercase_string)
            ],
            **fixed_parameter
        )

    def generate(self, name):
        return Element(name)