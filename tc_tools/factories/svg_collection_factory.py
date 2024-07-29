from . import SVGElementFactory
from .base_factory import BaseFactory
from .values import lowercase_string, list_of
from tc_tools.mapper import SVGCollection, SVGElement


class SVGCollectionFactory(BaseFactory):
    def build(self, **fixed_values) -> SVGCollection:
        return super().build(
            [
                ("label", lowercase_string()),
                ("children", list_of(SVGElementFactory().build))
            ],
            **fixed_values
        )

    def generate(self, label: str, children: list[SVGElement]) -> SVGCollection:
        collection: SVGCollection = SVGCollection()
        collection.set_label(label)
        collection.add_children(children)
        return collection
