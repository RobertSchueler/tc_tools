from processor import base_process, base_process_single_item

"""Should produce 4 copies of the same png in the ./excel directory"""

inkscape_path = 'C:\\Program Files\Inkscape\\bin\inkscape.com'
excel_path = ".\\testdata\\excel\\testmappe_001.xlsx"
svg_path = ".\\testdata\\svg\\testdata_001.svg"

base_process(
    inkscape_path=inkscape_path,
    excel_path=excel_path,
    svg_path=svg_path,
    single_item_process=base_process_single_item
)
