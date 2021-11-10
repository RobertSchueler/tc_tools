from html2image import Html2Image
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader(searchpath="./templates"))
hti = Html2Image()


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


def box(left, top, width, height, content="", **css_args):
    """
    """
    css_args["left"] = left
    css_args["top"] = top
    css_args["width"] = width
    css_args["height"] = height
    id = next(_box_id)

    _box_html_list.append(_box_html_template.render(content=content, id=id))
    _box_css_list.append(_box_css_template.render(css_args=css_args, id=id))


def image(path, left, top, width, height, **css_args):
    """
    """
    hti.load_file(path)
    content = _img_html_template.render(path=path, width=width, height=height)
    box(content, left, top, width, height, **css_args)


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

    for i, data in enumerate(source):
        _box_html_list, _box_css_list, _box_id = [], [], _box_id_iter()
        render_fun(data, *args, **kwargs)
        content = _card_html_template.render(boxes=_box_html_list)
        html_str = _index_html_template.render(content=content)
        css_str = _card_css_template.render(boxes=_box_css_list)

        hti.screenshot(
            html_str=html_str,
            css_str=css_str,
            #output_path=f"{path}",
            save_as=f"out{i}.jpg"
        )
