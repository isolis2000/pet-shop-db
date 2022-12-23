import PySimpleGUI as sg
from databaseRead import readTiposProducto

def displayTiposProducto():
    headings = ['Producto', 'Precio', 'Ganancia %', 'Ganancia', 'Codigo de Barras']

    data = readTiposProducto()

    layout = [[sg.Table(data, headings=headings, justification='center', key='-TABLE-')],]
    window = sg.Window("Title", layout, finalize=True)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        print(event, values)

    window.close()

# displayTiposProducto()