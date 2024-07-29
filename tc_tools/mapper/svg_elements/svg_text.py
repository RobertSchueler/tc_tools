from .svg_element import SVGElement


class SVGText(SVGElement):
    _text_content = None

    def set_text_content(self, text_content: str):
        self._text_content = text_content

    def get_text_content(self):
        return self._text_content