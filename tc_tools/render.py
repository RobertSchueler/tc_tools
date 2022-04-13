from html2image import Html2Image
from jinja2 import Environment, FileSystemLoader

from tc_tools import FORMATS, FACTORS

"""
Contains functions for the rendering of cards.
In order to render the cards, a html file is build automatically and then screenshotted.
These functions can then be used inside a render function with the signature dict, *args, **kwargs -> None.
All changes will be stored privately.
"""

_env = Environment(loader=FileSystemLoader(searchpath="./templates"))
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

_index_html_template = _env.get_template("index.html")
_card_html_template = _env.get_template("card.html")
_card_css_template = _env.get_template("card.css")
_box_html_template = _env.get_template("box.html")
_box_css_template = _env.get_template("box.css")
_img_html_template = _env.get_template("img.html")
_font_css_template = _env.get_template("font.css")

_dpi = 300
_width = 300
_height = 300
_unit = "in"


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


def box(left, top, width, height, unit=None, content="", **css_args):
    """
    """
    left, top, width, height = _convert_to_px(left, top, width, height, unit)

    css_args["left"] = left
    css_args["top"] = top
    css_args["width"] = width
    css_args["height"] = height
    box_id = next(_box_id)

    _html_list.append(_box_html_template.render(content=content, id=box_id))
    _css_list.append(_box_css_template.render(css_args=css_args, id=box_id))


def image(path, left, top, width, height, unit=None, **css_args):
    """
    """
    left, top, width, height = _convert_to_px(left, top, width, height, unit)
    content = _img_html_template.render(path=path, width=width, height=height)
    box(left, top, width, height, "px", content, **css_args)


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
    global _html_list
    global _css_list
    global _box_id
    global _hti

    for i, data in enumerate(source):
        _html_list, _css_list, _box_id, _hti = [], _css_initial_list, _box_id_iter(), Html2Image(output_path=path)
        render_fun(data, *args, **kwargs)
        content = _card_html_template.render(boxes=_html_list, id="main")
        html_str = _index_html_template.render(content=content)
        css_str = _card_css_template.render(boxes=_css_list)

        _hti.screenshot(
            html_str=html_str,
            css_str=css_str,
            save_as=f"out{i}.jpg"
        )
