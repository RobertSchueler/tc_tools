from .svg_element import SVGElement


class SVGRoot:
    def __init__(self,
                 children: list[SVGElement]
                 ):
        self._children = children
        self._label_to_element_mapping = {
            child.get_label(): child for child in self._children
        }

    def __iter__(self):
        yield from self._children

    def get_by_label(self, label: str) -> SVGElement:
        try:
            return self._label_to_element_mapping[label]
        except KeyError as e:
            raise KeyError(f"No element with label {label} found in SVGRoot", e)


