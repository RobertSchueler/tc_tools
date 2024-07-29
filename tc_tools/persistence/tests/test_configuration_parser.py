from tc_tools.factories import ConfigurationTextFactory
from tc_tools.factories.values import full_string
from tc_tools.persistence import parse_configuration_file
import os
import unittest


class TestParseOptionsFile(unittest.TestCase):
    def setUp(self) -> None:
        self.test_file_path = "./testfile.txt"
        self.inkscape_path = full_string()()
        self.test_file_content = ConfigurationTextFactory().build(
            inkscape_path=self.inkscape_path
        )
        with open(self.test_file_path, "w", encoding="utf-8") as file:
            file.write(self.test_file_content)

    def test_parse_options_should_parse_file_correctly(self) -> None:
        result = parse_configuration_file(self.test_file_path)
        self.assertEqual(result, self.inkscape_path)

    def tearDown(self) -> None:
        os.remove(self.test_file_path)

