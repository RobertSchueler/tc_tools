import os
from typing import Callable

from mapper import extract_svg_root_from_element_tree, SVGRoot, \
    merge_svg_root_and_element_tree, SVGElement, SVGImage, SVGText
from persistence import create_simple_data_source_from_excel, parse_svg_to_element_tree, \
    write_element_tree_to_svg, render_svg_to_png, parse_configuration_file


# public
def base_process(
        configurations_path: str,
        excel_path: str,
        svg_path: str,
        single_item_process: Callable[[SVGRoot, dict], None]
) -> None:
    inkscape_path = parse_configuration_file(configurations_path)
    data_source = create_simple_data_source_from_excel(excel_path)
    etree = parse_svg_to_element_tree(svg_path)
    for i, data in enumerate(data_source):
        svg_root = extract_svg_root_from_element_tree(etree)
        single_item_process(svg_root, data)
        merged_etree = merge_svg_root_and_element_tree(svg_root, etree)
        write_element_tree_to_svg(merged_etree, "./temp.svg")
        excel_dir = os.path.dirname(os.path.realpath(excel_path))
        render_svg_to_png(
            inkscape_path,
            "./temp.svg",
            os.path.join(excel_dir, f"out{i}.png"),
            200
        )
    os.remove("./temp.svg")


#public
def base_process_single_item(svg_root: SVGRoot, data: dict) -> None:
    for key, value in data.items():
        process_svg_element_by_key(svg_root, key, value)


def get_label_and_attribute_from_key(key):
    if "." not in key:
        return key, None
    return key.split(".")[:2]


def process_svg_element_by_key(svg_root: SVGRoot, key: str, value: str) -> None:
    label, attribute = get_label_and_attribute_from_key(key)
    try:
        svg_element: SVGElement = svg_root.get_by_label(label)
    except KeyError:
        return

    if isinstance(svg_element, SVGImage):
        process_svg_image_by_attribute(svg_element, attribute, value)
    elif isinstance(svg_element, SVGText):
        process_svg_text_by_attribute(svg_element, attribute, value)


def process_svg_image_by_attribute(svg_image: SVGImage, attribute: str | None, value: str):
    if attribute is None:
        attribute = "href"
    if attribute == "href":
        svg_image.set_href(value)


def process_svg_text_by_attribute(svg_text: SVGText, attribute: str | None, value: str):
    if attribute is None:
        attribute = "text"
    if attribute == "text":
        svg_text.set_text_content(value)