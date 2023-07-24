from .svg_element import SVGElement


class SVGRoot:
    def __init__(self, children: list[SVGElement]):
        self._children = children

    def __iter__(self):
        yield from self._children
