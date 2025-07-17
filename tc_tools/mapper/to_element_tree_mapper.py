import copy
from random import random
from xml.etree.ElementTree import ElementTree, Element, SubElement

import imagesize

from tc_tools.mapper import SVGRoot, SVGElement, SVGImage, SVGCollection, SVGText
from .to_svg_mapper import IMAGE_TAG


# public
def merge_svg_root_and_element_tree(root: SVGRoot, etree: ElementTree) -> ElementTree:
    copied_etree = copy.deepcopy(etree)
    for svg_child, etree_child in zip(root, copied_etree.getroot()):
        merge_svg_and_element(svg_child, etree_child)
    return copied_etree


# public
def merge_svg_and_element(svg_element: SVGElement, element: Element) -> Element:
    if isinstance(svg_element, SVGCollection):
        return merge_svg_collection_and_element(svg_element, element)
    if isinstance(svg_element, SVGImage):
        return merge_svg_image_and_element(svg_element, element)
    if isinstance(svg_element, SVGText):
        return merge_svg_text_and_element(svg_element, element)
    return element


def merge_svg_text_and_element(svg_text: SVGText, element: Element) -> Element:
    #kill all children because text in inkscape is saved via weird tspans
    for child in list(element):
        element.remove(child)

    element.text = ""

    for line in svg_text.get_text_content().split("\n"):
        subelement = SubElement(element, "ns0:tspan", attrib={
            "ns2:role": "line",
            "style": "stroke-width:0.264583",
            "x": str(element.attrib.get("x")),
            "y": str(element.attrib.get("y")),
            "id": str("tspan" + str(int(random() * 100000))),
        })
        subelement.text = line

    return element


def merge_svg_collection_and_element(
        svg_collection: SVGCollection, element: Element
) -> Element:
    merged_children = [
        merge_svg_and_element(svg_child_element, child_element)
        for svg_child_element, child_element in zip(svg_collection, element)
    ]
    element.clear()
    element.extend(merged_children)
    return element


def merge_svg_image_and_element(svg_image: SVGImage, element: Element) -> Element:
    if not(element.tag.endswith(IMAGE_TAG)):
        return element

    override_element_attribute(element, "href", svg_image.href)

    image_width, image_height = imagesize.get(svg_image.href)
    scale = min(svg_image.outer_width/image_width, svg_image.outer_height/image_height)
    width_border_size = svg_image.outer_width - scale*image_width
    heigth_border_size = svg_image.outer_height - scale*image_height

    override_element_attribute(element, "x", svg_image.outer_x + 1/2*width_border_size)
    override_element_attribute(element, "y", svg_image.outer_y + 1/2*heigth_border_size)
    override_element_attribute(element, "width", scale*image_width)
    override_element_attribute(element, "height", scale*image_height)

    return element


def override_element_attribute(element: Element, override_key: str, value: str):
    extended_attribute = next(
        (key for key in element.attrib.keys() if key.endswith(override_key)), override_key
    )
    element.set(extended_attribute, str(value))
