from tc_tools.processor import base_process, base_process_single_item
from unittest import TestCase
import os
from matplotlib.testing.compare import compare_images


class ManualTestcases(TestCase):
    def setUp(self) -> None:
        self.configurations_path = ".\\testdata\\configurations\\configurations.txt"

    def assertImagesEqual(self, path: str, other_path: str) -> None:
        comparison_result = compare_images(path, other_path, tol=0)
        self.assertIsNone(comparison_result)

    def clean_remove(self, path:str) -> None:
        if os.path.isfile(path):
            os.remove(path)

    def test_testcase_001_should_produce_4_copies_of_same_image_in_excel_dir(self) -> None:
        excel_path = ".\\testdata\\excel\\testmappe_001.xlsx"
        svg_path = ".\\testdata\\svg\\testdata_001.svg"
        result_image_path = ".\\testdata\\results\\test_001\\out.png"

        base_process(
            configurations_path=self.configurations_path,
            excel_path=excel_path,
            svg_path=svg_path,
            single_item_process=base_process_single_item
        )

        self.assertImagesEqual(".\\testdata\\excel\\out0.png", result_image_path)
        self.assertImagesEqual(".\\testdata\\excel\\out1.png", result_image_path)
        self.assertImagesEqual(".\\testdata\\excel\\out2.png", result_image_path)
        self.assertImagesEqual(".\\testdata\\excel\\out3.png", result_image_path)

    def test_testcase_002_should_produce_4_different_images(self) -> None:
        excel_path = ".\\testdata\\excel\\testmappe_002.xlsx"
        svg_path = ".\\testdata\\svg\\testdata_002.svg"

        base_process(
            configurations_path=self.configurations_path,
            excel_path=excel_path,
            svg_path=svg_path,
            single_item_process=base_process_single_item
        )

        self.assertImagesEqual(
            ".\\testdata\\excel\\out0.png",
            ".\\testdata\\results\\test_002\\out0.png"
        )
        self.assertImagesEqual(
            ".\\testdata\\excel\\out1.png",
            ".\\testdata\\results\\test_002\\out1.png"
        )
        self.assertImagesEqual(
            ".\\testdata\\excel\\out2.png",
            ".\\testdata\\results\\test_002\\out2.png"
        )
        self.assertImagesEqual(
            ".\\testdata\\excel\\out3.png",
            ".\\testdata\\results\\test_002\\out3.png"
        )

    def test_testcase_003_should_have_different_images_and_titles(self) -> None:
        excel_path = ".\\testdata\\excel\\testmappe_003.xlsx"
        svg_path = ".\\testdata\\svg\\testdata_003.svg"

        base_process(
            configurations_path=self.configurations_path,
            excel_path=excel_path,
            svg_path=svg_path,
            single_item_process=base_process_single_item
        )

        self.assertImagesEqual(
            ".\\testdata\\excel\\out0.png",
            ".\\testdata\\results\\test_003\\out0.png"
        )
        self.assertImagesEqual(
            ".\\testdata\\excel\\out1.png",
            ".\\testdata\\results\\test_003\\out1.png"
        )
        self.assertImagesEqual(
            ".\\testdata\\excel\\out2.png",
            ".\\testdata\\results\\test_003\\out2.png"
        )
        self.assertImagesEqual(
            ".\\testdata\\excel\\out3.png",
            ".\\testdata\\results\\test_003\\out3.png"
        )

    def test_testcase_004_should_have_multiline_text(self) -> None:
        excel_path = ".\\testdata\\excel\\testmappe_004.xlsx"
        svg_path = ".\\testdata\\svg\\testdata_004.svg"

        base_process(
            configurations_path=self.configurations_path,
            excel_path=excel_path,
            svg_path=svg_path,
            single_item_process=base_process_single_item
        )

        self.assertImagesEqual(
            ".\\testdata\\excel\\out0.png",
            ".\\testdata\\results\\test_004\\out0.png"
        )
        self.assertImagesEqual(
            ".\\testdata\\excel\\out1.png",
            ".\\testdata\\results\\test_004\\out1.png"
        )
        self.assertImagesEqual(
            ".\\testdata\\excel\\out2.png",
            ".\\testdata\\results\\test_004\\out2.png"
        )
        self.assertImagesEqual(
            ".\\testdata\\excel\\out3.png",
            ".\\testdata\\results\\test_004\\out3.png"
        )

    def tearDown(self) -> None:
        pass
        self.clean_remove(".\\testdata\\excel\\out0.png")
        self.clean_remove(".\\testdata\\excel\\out1.png")
        self.clean_remove(".\\testdata\\excel\\out2.png")
        self.clean_remove(".\\testdata\\excel\\out3.png")
