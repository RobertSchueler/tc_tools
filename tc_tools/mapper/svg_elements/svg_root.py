from .svg_element import SVGElement
from .svg_collection import SVGCollection


class SVGRoot:
    def __init__(self,
                 children: list[SVGElement]
                 ):
        self._children = children

        self._label_to_element_mapping = self.collect_child_labels(self._children)

    def __iter__(self):
        yield from self._children

    def get_by_label(self, label: str) -> SVGElement:
        return self._label_to_element_mapping[label]

    def collect_child_labels(self, children: list[SVGElement]) -> dict[str, SVGElement]:
        labels = {}
        for child in children:
            if isinstance(child, SVGCollection):
                labels.update(self.collect_child_labels(child.get_children()))
            else:
                labels[child.get_label()] = child
        return labels
