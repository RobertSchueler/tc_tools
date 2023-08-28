from processor import base_process, base_process_single_item

"""Should produce 4 copies of the same png in the './testdata/excel' directory named
'out0.png' up to 'out3.png' """

configurations_path = ".\\testdata\\configurations\\configurations.txt"
excel_path = ".\\testdata\\excel\\testmappe_001.xlsx"
svg_path = ".\\testdata\\svg\\testdata_001.svg"

base_process(
    configurations_path=configurations_path,
    excel_path=excel_path,
    svg_path=svg_path,
    single_item_process=base_process_single_item
)
