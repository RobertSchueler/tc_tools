from mapper import SVGElement


class SVGImage(SVGElement):
    _href: str = None

    def get_href(self, href):
        self._href = href

    def set_href(self):
        return self._href