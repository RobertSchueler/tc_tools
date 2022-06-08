from html2image import Html2Image
from jinja2 import Environment, FileSystemLoader
from fontTools.ttLib import TTFont
import os
import numpy as np

from tc_tools import FORMATS, FACTORS

"""
Contains functions for the rendering of cards.
In order to render the cards, a html file is build automatically and then screenshotted.
These functions can then be used inside a render function with the signature dict, *args, **kwargs -> None.
All changes will be stored privately.
"""


_searchpath = os.path.join(os.path.dirname(__file__), "../templates")
_env = Environment(loader=FileSystemLoader(searchpath=_searchpath))
_hti = Html2Image()


def _box_id_iter():
    i = 1
    while True:
        i += 1
        yield f"box{i}"


_html_list = []
_css_list = []
_css_initial_list = []
_box_id = _box_id_iter()
_fonts = {}

_index_html_template = _env.get_template("index.html")
_card_html_template = _env.get_template("card.html")
_card_css_template = _env.get_template("card.css")
_box_html_template = _env.get_template("box.html")
_box_css_template = _env.get_template("box.css")
_img_html_template = _env.get_template("img.html")
_font_css_template = _env.get_template("font.css")
_text_html_template = _env.get_template("text.html")
_text_css_template = _env.get_template("text.css")

_dpi = 300
_width = 300
_height = 300
_unit = "in"

_x_offset = 0
_y_offset = 0


def _get_text_width(name, text):
    font = _fonts[name]
    cmap = font['cmap']
    t = cmap.getcmap(3, 1).cmap
    s = font.getGlyphSet()
    units_per_em = font['head'].unitsPerEm
    widths = [
        s[t[ord(c)]].width if ord(c) in t and t[ord(c)] in s
        else s['.notdef'].width
        for c in text
    ]
    total = sum(widths)/units_per_em;
    return total


def set_meta_params(dpi=None, fmt=None, unit=None):
    """
    Can be used to set the resolution, format and unit of measurement of the cards.
    All float inputs of the functions of this module will be interpreted in the given unit.
    Recommended usage is right before the call of `render`.

    Parameters
    ----------
    dpi: float, optional
    fmt: str, optional
        a format string supported by the `constants` module.
    unit: str, optional
        a unit string supported by the `constants` module
    """
    global _dpi
    global _width
    global _height
    global _unit

    if dpi:
        _dpi = dpi
    if fmt:
        width, height = FORMATS[fmt]
        _width = int(dpi*width)
        _height = int(dpi*height)
    if unit:
        _unit = unit


def register_font(url, name=None, format_=None, style="normal", weight="normal"):
    """WIP"""

    if name is None or format_ is None:
        name, format_ = url.split("/")[-1].split(".")

    _fonts[name] = TTFont(url)
    _css_initial_list.append(_font_css_template.render(url=url, name=name, format_=format_, style=style, weight=weight))


def _calculate_pixel(val, unit, base):
    if not unit:
        unit = _unit

    if unit == "px":
        return int(val)

    if unit == "%":
        return int(val*base/100)

    factor = FACTORS[unit]
    return int(val*factor*_dpi)


def _convert_to_px(left, top, width, height, unit):
    return (
        _calculate_pixel(left, unit, _width),
        _calculate_pixel(top, unit, _height),
        _calculate_pixel(width, unit, _width),
        _calculate_pixel(height, unit, _height)
    )


def box(left, top, width, height, unit=None, content="", box_id=None, **css_args):
    """
    """

    left, top, width, height = _convert_to_px(left, top, width, height, unit)

    css_args["left"] = _x_offset + left
    css_args["top"] = _y_offset + top
    css_args["width"] = width
    css_args["height"] = height
    if box_id is None:
        box_id = next(_box_id)

    # ########test
    # if "font_family" in css_args and css_args["font_family"].strip('"') in _fonts:
    #     name = css_args["font_family"].strip('"')
    #     try:
    #         p = 0.95
    #         lh = 1/1.5
    #         m = np.sqrt(lh/p*height/width * _get_text_width(name, str(content)))
    #         print(m)
    #         max_by_width = round(m)*p*width / _get_text_width(name, str(content))
    #         print(f"diff: {height - round(m)*max_by_width}, {height} ")
    #         css_args["font_size"] = min(max_by_width, height)
    #     except ZeroDivisionError:
    #         pass
    #     # css_args["font_size"] = "100px"
    # ########

    _html_list.append(_box_html_template.render(content=content, id=box_id))
    _css_list.append(_box_css_template.render(css_args=css_args, id=box_id))


def image(path, left, top, width, height, unit=None, **css_args):
    """
    """
    left, top, width, height = _convert_to_px(left, top, width, height, unit)
    content = _img_html_template.render(path=path, width=width, height=height)
    box(left, top, width, height, "px", content, **css_args)


def text(text, left, top, width, height, unit=None, font_size=20, vertical_align="center",
         horizontal_align="center", **css_args):
    """
    """
    left, top, width, height = _convert_to_px(left, top, width, height, unit)

    text_css = {}
    if vertical_align == "center":
        css_args.update({
            "display": "flex",
            "justify_content": "center",
            "font_size": font_size,
            "align_items": "center"
        })

    box_id = next(_box_id)
    _css_list.append(_text_css_template.render(id=box_id, css_args=text_css))

    content = _text_html_template.render(text=text)
    #content = "Hallo Welt"
    box(left, top, width, height, "px", content=content, text_align=horizontal_align, box_id=box_id, **css_args)


def _screenshot(path, width, height):
    print(f"making screenshot to {path}")

    content = _card_html_template.render(boxes=_html_list, id="main")
    html_str = _index_html_template.render(content=content)
    css_str = _card_css_template.render(boxes=_css_list)

    _hti.screenshot(
        html_str=html_str,
        css_str=css_str,
        save_as=path,
        size=(width, height)
    )


def _reset_screen(path):
    global _html_list
    global _css_list
    global _box_id
    global _hti
    _html_list = []
    _css_list = _css_initial_list
    _box_id = _box_id_iter()
    _hti = Html2Image(output_path = path)


def render(path, render_fun, source, *args, **kwargs):
    """
    Renders all cards according to the function render_fun using the data obtained from source.
    args and kwargs are passed down to render_fun.

    Parameter
    ---------

    path: str,
        the path of the output

    render_fun: (data, *args, **kwargs) -> None,
        a function evoking all the render functions from this submodule.

    source: iteratable yielding dict like objects
    """
    global _x_offset
    global _y_offset

    global _html_list
    global _css_list
    global _box_id
    global _hti

    for i, data in enumerate(source):
        _reset_screen(path)
        render_fun(data, *args, **kwargs)
        _screenshot(f"out{i}.jpg", _width, _height)


def _reset_render_collection(path, h_margin, v_margin, width, height):
    global _x_offset
    global _y_offset

    _reset_screen(path)
    _x_offset, _y_offset = 0, 0
    box(0, 0, width, height, "px", background_color= "white")
    _x_offset, _y_offset = h_margin, v_margin


def render_collection(
        path, render_fun, source,
        fmt = "A4", h_margin = 0, v_margin = 0, h_space = 0, v_space = 0,
        repeat=False, unit=None, *args, **kwargs
    ):
    global _x_offset
    global _y_offset

    global _html_list
    global _css_list
    global _box_id
    global _hti

    container_width, container_height = FORMATS[fmt]
    container_width = int(container_width*_dpi)
    container_height = int(container_height*_dpi)
    h_margin = _calculate_pixel(h_margin, unit, container_width)
    v_margin = _calculate_pixel(v_margin, unit, container_height)
    h_space = _calculate_pixel(h_space, unit, container_width)
    v_space = _calculate_pixel(v_space, unit, container_height)

    if container_width - 2*h_margin < _width:
        raise ValueError("Container width is too small")
    if container_height - 2*v_margin < _height:
        raise ValueError("Container height is too small")

    i = 0
    _reset_render_collection(path, h_margin, v_margin, container_width, container_height)
    for data in source:
        while True:
            #check if there is enough space in the horizontal direction
            if _x_offset + h_space + _width + h_margin <= container_width:
                _x_offset += h_space
                render_fun(data)
                _x_offset += _width
            #check if there is at least space in the vertical direction
            elif _y_offset + v_space + 2*_height + v_margin <= container_height:
                _x_offset = h_margin
                _y_offset += v_space + _height
                render_fun(data)
                _x_offset += _width
            #otherwise begin a new page I guess
            else:
                _screenshot(f"out{i}.jpg", container_width, container_height)
                _reset_render_collection(path, h_margin, v_margin, container_width, container_height)
                i += 1
                if repeat:
                    break
            if not repeat:
                break
    # one last screenshot
    _screenshot(f"out{i}.jpg", container_width, container_height)
