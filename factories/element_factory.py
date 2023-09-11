from xml.etree.ElementTree import Element

from mapper.to_svg_mapper import LABEL_KEY
from .base_factory import BaseFactory
from .values import lowercase_string, dict_with_fixed_not_mandatory_keys


class ElementFactory(BaseFactory):

    def build(self, fixed_attributes=None, **fixed_parameter) -> Element:
        if fixed_attributes is None:
            fixed_attributes = {}
        return super().build(
            [
                ("tag", lowercase_string()),
                ("attrib", self.build_attrib(**fixed_attributes))
            ],
            **fixed_parameter
        )

    def generate(self, tag: str, attrib: dict[str, str]):
        return Element(tag, attrib)

    @staticmethod
    def build_attrib(**fixed_attributes):
        def inner():
            candidate = dict_with_fixed_not_mandatory_keys(
                [LABEL_KEY], lowercase_string()
            )()
            candidate.update(fixed_attributes)
            return candidate
        return inner