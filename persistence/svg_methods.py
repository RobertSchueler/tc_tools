import os
import xml.etree.ElementTree as ElementTree


def parse_svg_to_element_tree(path: str) -> ElementTree:
    return ElementTree.parse(path)


def write_element_tree_to_svg(etree: ElementTree, path: str) -> None:
    etree.write(path)


def render_svg_to_png(inkscape_path: str, svg_path: str, png_path: str, dpi: int = 300) -> None:
    cmd = f'""{inkscape_path}" --export-filename="{png_path}" --export-dpi={dpi} "{svg_path}""'
    os.system(cmd)
