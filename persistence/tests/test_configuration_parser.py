from TestDataFactory import TestDataFactory
from persistence import parse_options_file
import os
import unittest


class TestParseOptionsFile(unittest.TestCase):
    def setUp(self) -> None:
        self.test_file_path = "./testfile.txt"
        with open(self.test_file_path, "w", encoding="utf-8") as file:
            file.write(TestDataFactory.create_options_text())

    def test_parse_options_should_parse_file_correctly(self) -> None:
        result = parse_options_file(self.test_file_path)
        self.assertEqual(result, "ink:scape:path")

    def tearDown(self) -> None:
        os.remove(self.test_file_path)

