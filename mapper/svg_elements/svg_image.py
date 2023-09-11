from .svg_element import SVGElement


class SVGImage(SVGElement):
    _href: str = None

    def set_href(self, href):
        self._href = href

    def get_href(self):
        return self._href