from tc_tools.mapper import SVGImage
from .base_factory import BaseFactory
from .values import lowercase_string, floating


class SVGImageFactory(BaseFactory):
    def build(self, **fixed_values) -> SVGImage:
        return super().build(
            [
                ("label", lowercase_string()),
                ("href", lowercase_string()),
                ("outer_x", floating()),
                ("outer_y", floating()),
                ("outer_width", floating()),
                ("outer_height", floating())
            ],
            **fixed_values
        )

    def generate(self, label: str, href: str, outer_x: float, outer_y: float, outer_width: float, outer_height: float) -> SVGImage:
        element: SVGImage = SVGImage()
        element.set_label(label)
        element.href = href
        element.outer_x = outer_x
        element.outer_y = outer_y
        element.outer_width = outer_width
        element.outer_height = outer_height
        return element