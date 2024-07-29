import unittest

from tc_tools.factories import SVGElementFactory
from tc_tools.factories.svg_collection_factory import SVGCollectionFactory
from tc_tools.factories.svg_root_factory import SVGRootFactory
from tc_tools.factories.values import lowercase_string, list_of
from tc_tools.mapper import SVGElement


class TestSVGRoot(unittest.TestCase):
    def setUp(self) -> None:
        self.INCORRECT_LABEL = "incorrect_label"
        self.labels = list_of(lowercase_string(forbidden_strings=[self.INCORRECT_LABEL]))()
        self.grandchildren = [
            SVGElementFactory().build(label=label) for label in self.labels
        ]
        self.children = [
            SVGCollectionFactory().build(children=self.grandchildren),
            SVGElementFactory().build()
        ]
        self.svg_root = SVGRootFactory().build(children=self.children)

    def test_get_by_label_returns_element_with_label(self) -> None:
        label_to_fetch: str = self.labels[0]
        fetched_element: SVGElement = self.svg_root.get_by_label(label_to_fetch)
        self.assertEqual(fetched_element.get_label(), label_to_fetch)

    def test_get_by_label_with_incorrect_label_throws_error(self) -> None:
        with self.assertRaises(KeyError) as error:
            self.svg_root.get_by_label(self.INCORRECT_LABEL)
        self.assertEqual(
            f"'{self.INCORRECT_LABEL}'",
            str(error.exception)
        )
