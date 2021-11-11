from html2image import Html2Image
from jinja2 import Environment, FileSystemLoader

from tc_tools import FORMATS, FACTORS

env = Environment(loader=FileSystemLoader(searchpath="./templates"))
_hti = Html2Image()


def _box_id_iter():
    i = 1
    while True:
        i += 1
        yield f"box{i}"


_box_html_list = []
_box_css_list = []
_box_id = _box_id_iter()

_index_html_template = env.get_template("index.html")
_card_html_template = env.get_template("card.html")
_card_css_template = env.get_template("card.css")
_box_html_template = env.get_template("box.html")
_box_css_template = env.get_template("box.css")
_img_html_template = env.get_template("img.html")

_dpi = 300
_width = 300
_height = 300
_unit = "in"


def set_meta_params(dpi=None, fmt=None, unit=None):
    """
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


def _calculate_pixel(val, unit, base):
    if not unit:
        unit = _unit

    if unit == "%":
        return int(val*base/100)

    factor = FACTORS[unit]
    return int(val*factor*_dpi)


def box(left, top, width, height, unit=None, content="", **css_args):
    """
    """
    css_args["left"] = _calculate_pixel(left, _width)
    css_args["top"] = _calculate_pixel(top, _height)
    css_args["width"] = _calculate_pixel(width, _width)
    css_args["height"] = _calculate_pixel(height, _height)
    box_id = next(_box_id)

    _box_html_list.append(_box_html_template.render(content=content, id=box_id))
    _box_css_list.append(_box_css_template.render(css_args=css_args, id=box_id))


def image(path, left, top, width, height, **css_args):
    """
    """
    _hti.load_file(path)
    content = _img_html_template.render(path=path, width=width, height=height)
    box(left, top, width, height, content, **css_args)


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
    global _box_html_list
    global _box_css_list
    global _box_id
    global _hti

    for i, data in enumerate(source):
        _box_html_list, _box_css_list, _box_id, _hti = [], [], _box_id_iter(), Html2Image(output_path=path)
        render_fun(data, *args, **kwargs)
        content = _card_html_template.render(boxes=_box_html_list, id="main")
        html_str = _index_html_template.render(content=content)
        css_str = _card_css_template.render(boxes=_box_css_list)

        _hti.screenshot(
            html_str=html_str,
            css_str=css_str,
            save_as=f"out{i}.jpg"
        )
