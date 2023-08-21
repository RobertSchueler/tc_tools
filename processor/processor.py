import os
from typing import Callable

from mapper import extract_svg_root_from_element_tree, SVGRoot, \
    merge_svg_root_and_element_tree
from persistence import create_simple_data_source_from_excel, parse_svg_to_element_tree, \
    write_element_tree_to_svg, render_svg_to_png, parse_configuration_file


def base_process(
        options_path: str,
        excel_path: str,
        svg_path: str,
        single_item_process: Callable[[SVGRoot, dict], None]
) -> None:
    inkscape_path = parse_configuration_file(options_path)
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


def base_process_single_item(svg_root: SVGRoot, data: dict) -> None:
    pass
