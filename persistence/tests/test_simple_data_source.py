import unittest

from persistence import SimpleDataSource


class TestSimpleDataSource(unittest.TestCase):
    def setUp(self) -> None:
        self.test_data = [
            {"a": "a", "b": 1, "c": 0.001},
            {"a": "Hallo Welt", "b": 2, "c": 3.14}
        ]
        self.simple_source = SimpleDataSource(self.test_data)

    def test_iterate_over_simple_data_source(self) -> None:
        for result, expected_output in zip(self.simple_source, self.test_data):
            self.assertEqual(result, expected_output)
