import PySimpleGUI as sg

sg.Window(
    title="TC Tools Graphical user interface",
    layout=[
        [sg.FileBrowse("Browse for excel sheet"),
         sg.FileBrowse("Browse for svg template"),
         sg.FileBrowse("Browse for options file")],
        [sg.Button("Render deck")]
    ],
    margins=(300, 200)
).read()
