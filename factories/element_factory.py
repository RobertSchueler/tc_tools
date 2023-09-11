from xml.etree.ElementTree import Element

from mapper.to_svg_mapper import LABEL_KEY
from .base_factory import BaseFactory
from .values import lowercase_string, dict_of, concatenate_dicts, dict_with_fixed_keys


class ElementFactory(BaseFactory):

    def build(self, **fixed_parameter) -> Element:
        return super().build(
            [
                ("name", lowercase_string),
                ("attrib", dict_of(lowercase_string, lowercase_string))
            ],
            **fixed_parameter
        )

    def generate(self, name: str, attrib: dict[str, str]):
        return Element(name, attrib)

    def build_element_with_inkscape_label(self, **fixed_parameter) -> Element:
        return super().build(
            [
                ("name", lowercase_string),
                (
                    "attrib",
                    concatenate_dicts(
                        dict_with_fixed_keys([LABEL_KEY], lowercase_string),
                        dict_of(lowercase_string, lowercase_string)
                    )
                )
            ],
            **fixed_parameter
        )