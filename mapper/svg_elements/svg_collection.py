from .svg_element import SVGElement


class SVGCollection(SVGElement):
    def __init__(self):
        self._children = []

    def __iter__(self):
        yield from self._children

    def add_child(self, child: SVGElement):
        self._children.append(child)

    def add_children(self, children: list[SVGElement]):
        self._children.extend(children)

    def get_children(self):
        return self._children