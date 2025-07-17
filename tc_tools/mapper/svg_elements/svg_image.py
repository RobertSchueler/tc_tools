from .svg_element import SVGElement


class SVGImage(SVGElement):
    href: str = None
    outer_x: float = None
    outer_y: float = None
    outer_height: float = None
    outer_width: float = None
