from .base_factory import BaseFactory
from mapper import SVGElement


class SVGElementFactory(BaseFactory):
    def build(self):
        return super().build(
            []
        )

    def generate(self):
        return SVGElement()
