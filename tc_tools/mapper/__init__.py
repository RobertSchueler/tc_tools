from .svg_elements import SVGElement, SVGRoot, SVGImage, SVGCollection, SVGText
from .to_svg_mapper import (
    extract_svg_root_from_element_tree, extract_svg_element_from_element
)
from .to_element_tree_mapper import (
    merge_svg_root_and_element_tree, merge_svg_and_element
)