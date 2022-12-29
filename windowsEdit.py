from tkinter.simpledialog import askfloat
import PySimpleGUI as sg
from datetime import datetime

base64Str = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAB0ElEQVRIS+1VvU4CQRDe7QQTf3I+gyaowUQTbdTIG2ClrSWlhfoKkmhrZ6uVvIFGbCg0kR8x+gyehsLD0KzfzB24e7d3QEFMjAfF3Ny38+18M7sjO52OEiN8pI2gXLkHpRQba8sDUZcrD8Ap4FcieCvBHQjUUAS0ITEYgZvPiafDIi+YPz4Aka+gxE+3yUfv5G8eFYUCjPBO6drIwsjAzW8JJaW42i1gtRLbl2cUhUMJ+AMuYjPs0k4B64C/8PEzGolB8AYCt/0lbvf2eReb56fCSaXMaAikE7leFy+BPwF+DAQ3vSwiBPTlxf1gwJwzHS0aMlHIjqShP9mv78ArKWadKfbrMlklYgVI1J4syRKFpUuQKMdy6AWNCB5TdL0BYjNofXp9+152JaI0qbNIrpA9kU7ba8AEDA7qarODz6FGMlSKJ/Da3J7VepPDZBczotZoco9HbGCog9mv2ZThRJo6z3+MIrc8ZIBVtfozHyJarJOxja1nFwK/xaagk+O/JhFqQNo+BhItIYM4u9pAltCOMLpNARJq8C9RhpvgD0tEo5K6ojukk06rf5MGB1+zqaPWV39GbWRkEol52YWupyRWEIbnsnUm973xhgCMnOAbzkiRYGtBf20AAAAASUVORK5CYII="


def newTipoProducto():

    layout = [[sg.Text("Insertar Tipo de Producto")],
              [sg.Text('Nombre:'), sg.InputText(key='nombre')],
              [sg.Text('Precio:'), sg.InputText(key='precio')],
              [sg.Text('Porcentaje de Ganancia:'),
               sg.InputText(key='ganancia')],
              [sg.Text('Codigo de Barras:'), sg.InputText(key='codigoBarras')],
              [sg.Button('Agregar', key='_ADD_'),
               sg.Button('Cancelar', key='_CANCEL_')]
              ]

    window = sg.Window('IBDPs first window', layout, font='Courier 12')
    submited = False
    event, values = window.read()

    while not submited:
        if event == '_ADD_':
            submited = True
        elif event == '_CANCEL_' or event == sg.WIN_CLOSED:
            values = 'Cancel'
            submited = True

    window.close()
    return values


def newProducto():

    layout = [[sg.Text("Agregar Producto")],
              [sg.Text('Fecha de compra:'), sg.InputText(
                  key='buyDate'),
               sg.CalendarButton('', target='buyDate', image_data=base64Str, format='%Y-%m-%d')],
              [sg.Text('Fecha de vencimiento:'),
               sg.InputText(key='expirationDate'),
               sg.CalendarButton('', target='expirationDate', image_data=base64Str, format='%Y-%m-%d')],
              [sg.Text('Porcentaje de descuento:'),
               sg.InputText(key='discount')],
              [sg.Text('Cantidad:'), sg.InputText(key='ammount')],
              [sg.Text('Codigo del producto:'),
               sg.InputText(key='productCode')],
              [sg.Button('Agregar', key='_ADD_'), sg.Button('Cancelar', key='_CANCEL_')]]

    window = sg.Window('IBDPs first window', layout, font='Courier 12')
    submited = False
    event, values = window.read()

    while not submited:
        if event == '_TODAY_':
            window.Element('buyDate').update(
                datetime.today().strftime('%Y-%m-%d'))
        elif event == '_ADD_':
            submited = True
        elif event == '_CANCEL_' or event == sg.WIN_CLOSED:
            values = 'Cancel'
            submited = True

    window.close()
    return values


def editTipoProducto(dataSelected):

    nombre = dataSelected[0]
    precio = str(float(dataSelected[1]) - float(dataSelected[3]))
    porcentajeGanancia = str(dataSelected[2])
    codigoBarras = dataSelected[4]

    layout = [[sg.Text("Insertar Tipo de Producto")],
              [sg.Text('Nombre:'), sg.InputText(nombre, key='nombre')],
              [sg.Text('Precio:'), sg.InputText(precio, key='precio')],
              [sg.Text('Porcentaje de Ganancia:'),
               sg.InputText(porcentajeGanancia, key='ganancia')],
              [sg.Text('Codigo de Barras:'), sg.InputText(
                  codigoBarras, key='codigoBarras')],
              [sg.Button('Agregar', key='_ADD_'),
               sg.Button('Cancelar', key='_CANCEL_')]
              ]

    window = sg.Window('IBDPs first window', layout, font='Courier 12')
    submited = False
    event, values = window.read()

    while not submited:
        if event == '_ADD_':
            submited = True
        elif event == '_CANCEL_' or event == sg.WIN_CLOSED:
            values = 'Cancel'
            submited = True

    window.close()
    return values
