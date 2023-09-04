import unittest

from factories.values import any_type, lowercase_string, dict_of, list_of
from persistence import SimpleDataSource


class TestSimpleDataSource(unittest.TestCase):
    def setUp(self) -> None:
        self.test_data = list_of(dict_of(lowercase_string, any_type))()
        self.simple_source = SimpleDataSource(self.test_data)

    def test_iterate_over_simple_data_source(self) -> None:
        for result, expected_output in zip(self.simple_source, self.test_data):
            self.assertEqual(result, expected_output)
