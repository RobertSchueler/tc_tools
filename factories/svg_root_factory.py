from mapper import SVGElement, SVGRoot
from . import SVGElementFactory
from .base_factory import BaseFactory
from .values import list_of


class SVGRootFactory(BaseFactory):
    def build(self, **fixed_parameter):
        return super().build(
            [
                ("children", list_of(SVGElementFactory.build))
            ],
            **fixed_parameter
        )

    def generate(self, children: list[SVGElement]):
        return SVGRoot(children)