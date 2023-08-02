import PySimpleGUI as sg

from processor import base_process, base_process_single_item

from .options_parser import parse_options_file

LABEL_SIZE = (7, 1)
INPUT_FIELD_SIZE = (45, 1)

window = sg.Window(
    title="TC Tools Graphical user interface",
    layout=[
        [
            sg.Text('Excel', size=LABEL_SIZE),
            sg.Input(key='-excel_path-', size=INPUT_FIELD_SIZE),
            sg.FileBrowse(file_types=(("Excel Files", "*.xlsx"),))
        ],
        [
            sg.Text('SVG', size=LABEL_SIZE),
            sg.Input(key='-svg_path-', size=INPUT_FIELD_SIZE),
            sg.FileBrowse(file_types=(("SVG Files", "*.svg"),))
        ],
        [
            sg.Text('Options', size=LABEL_SIZE),
            sg.Input(key='-options_path-', size=INPUT_FIELD_SIZE),
            sg.FileBrowse(file_types=(("Text files", "*.txt"),))
        ],
        [sg.Button("Render deck")]
    ],
    margins=(300, 200)
)

while True:
    event, values = window.read()
    if event in ('Exit', 'Quit', None):
        break

    if event == "Render deck":
        try:
            excel_path: str = values['-excel_path-']
            svg_path: str = values['-svg_path-']
            options_path: str = values['-options_path-']
        except KeyError:
            continue

        inkscape_path = parse_options_file(options_path)
        base_process(inkscape_path, excel_path, svg_path, base_process_single_item)
