from .base_factory import BaseFactory
from mapper import SVGElement
from .values import lowercase_string


class SVGElementFactory(BaseFactory):
    def build(self, **fixed_values) -> SVGElement:
        return super().build(
            [
                ("label", lowercase_string())
            ],
            **fixed_values
        )

    def generate(self, label: str) -> SVGElement:
        element: SVGElement = SVGElement()
        element.set_label(label)
        return element
