from tc_tools.mapper import SVGImage
from .base_factory import BaseFactory
from .values import lowercase_string


class SVGImageFactory(BaseFactory):
    def build(self, **fixed_values) -> SVGImage:
        return super().build(
            [
                ("label", lowercase_string()),
                ("href", lowercase_string())
            ],
            **fixed_values
        )

    def generate(self, label: str, href: str) -> SVGImage:
        element: SVGImage = SVGImage()
        element.set_label(label)
        element.href = href
        return element