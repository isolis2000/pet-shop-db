import PySimpleGUI as sg
from DatabaseRead import read_tipos_producto


def display_tipos_producto():
    headings = ["Producto", "Precio", "Ganancia %", "Ganancia", "Codigo de Barras"]

    data = read_tipos_producto()

    layout = [
        [sg.Table(data, headings=headings, justification="center", key="-TABLE-")],
    ]
    window = sg.Window("Title", layout, finalize=True)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        print(event, values)

    window.close()


# display_tipos_producto()
