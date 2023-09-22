from persistence import parse_svg_to_element_tree

elementTree = parse_svg_to_element_tree("./manual_tests/testdata/svg/testdata_002.svg")

children = [child for child in elementTree.getroot()]

grandchildren = [grandchild  for child in children for grandchild in child]

print("Hi")