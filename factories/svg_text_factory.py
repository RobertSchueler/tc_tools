from mapper import SVGText
from .base_factory import BaseFactory
from .values import full_string


class SVGTextFactory(BaseFactory):
    def build(self, **fixed_parameters):
        return super().build(
            [
                ("text_content", full_string())
            ],
            **fixed_parameters
        )

    def generate(self, text_content: str) -> SVGText:
        svg_text = SVGText()
        svg_text.set_text_content(text_content)
        return svg_text
