import unittest

from factories import SVGElementFactory
from factories.svg_root_factory import SVGRootFactory
from factories.values import lowercase_string, list_of
from mapper import SVGElement


class TestSVGRoot(unittest.TestCase):
    def setUp(self) -> None:
        self.labels = list_of(lowercase_string)()
        self.children = [
            SVGElementFactory().build(label=label) for label in self.labels
        ]
        self.svg_root = SVGRootFactory().build(children=self.children)

    def test_get_by_label_returns_element_with_label(self) -> None:
        label_to_fetch: str = self.labels[0]
        fetched_element: SVGElement = self.svg_root.get_by_label(label_to_fetch)
        self.assertEqual(fetched_element.get_label(), label_to_fetch)

    def test_get_by_label_with_incorrect_label_throws_error(self) -> None:
        pass
