from tkinter.simpledialog import askfloat
import PySimpleGUI as sg
from datetime import datetime


def newTipoProducto():

    #     col2 = sg.Column([[sg.Frame('Accounts:', [[sg.Column([[sg.Listbox(['Account '+str(i) for i in range(1,16)],
    #                                                       key='-ACCT-LIST-',size=(15,20)),]],size=(150,400))]])]],pad=(0,0))
    #     col1 = sg.Column([[sg.Text("Segunda columna")],
    #             [sg.Text("Segunda columna 2")]])

    layout = [[sg.Text("Insertar Tipo de Producto")],
              [sg.Text('Nombre:'), sg.InputText(key='nombre')],
              [sg.Text('Precio:'), sg.InputText(key='precio')],
              [sg.Text('Porcentaje de Ganancia:'),
               sg.InputText(key='ganancia')],
              [sg.Text('Codigo de Barras:'), sg.InputText(key='codigoBarras')],
              [sg.Button('Agregar', key='_ADD_'), sg.Button('Cancelar', key='_CANCEL_')]
              ]

#     layout = [[col1, col3, col2]]
#     layout = [[col]]

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

    # sg.popup('You entered', values['-IN-'])
    return values


def newProducto():

    #     col2 = sg.Column([[sg.Frame('Accounts:', [[sg.Column([[sg.Listbox(['Account '+str(i) for i in range(1,16)],
    #                                                       key='-ACCT-LIST-',size=(15,20)),]],size=(150,400))]])]],pad=(0,0))
    #     col1 = sg.Column([[sg.Text("Segunda columna")],
    #             [sg.Text("Segunda columna 2")]])

    layout = [[sg.Text("Agregar Producto")],
              [sg.Text('Fecha de compra:'), sg.InputText(
                  key='buyDate'), sg.Button('Hoy', key='_TODAY_')],
              [sg.Text('Fecha de vencimiento:'),
               sg.InputText(key='expirationDate')],
              [sg.Text('Porcentaje de descuento:'),
               sg.InputText(key='discount')],
              [sg.Text('Cantidad:'), sg.InputText(key='ammount')],
              [sg.Text('Codigo del producto:'),
               sg.InputText(key='productCode')],
              [sg.Button('Agregar', key='_ADD_'), sg.Button('Cancelar', key='_CANCEL_')]]
#     layout = [[col1, col3, col2]]
#     layout = [[col]]

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

    # sg.popup('You entered', values['-IN-'])
    return values

def editTipoProducto(dataSelected):

    #     col2 = sg.Column([[sg.Frame('Accounts:', [[sg.Column([[sg.Listbox(['Account '+str(i) for i in range(1,16)],
    #                                                       key='-ACCT-LIST-',size=(15,20)),]],size=(150,400))]])]],pad=(0,0))
    #     col1 = sg.Column([[sg.Text("Segunda columna")],
    #             [sg.Text("Segunda columna 2")]])
    nombre = dataSelected[0]
    precio = str(float(dataSelected[1]) - float(dataSelected[3]))
    porcentajeGanancia = str(dataSelected[2])
    codigoBarras = dataSelected[4]

    layout = [[sg.Text("Insertar Tipo de Producto")],
              [sg.Text('Nombre:'), sg.InputText(nombre, key='nombre')],
              [sg.Text('Precio:'), sg.InputText(precio, key='precio')],
              [sg.Text('Porcentaje de Ganancia:'),
               sg.InputText(porcentajeGanancia, key='ganancia')],
              [sg.Text('Codigo de Barras:'), sg.InputText(codigoBarras, key='codigoBarras')],
              [sg.Button('Agregar', key='_ADD_'), sg.Button('Cancelar', key='_CANCEL_')]
              ]

#     layout = [[col1, col3, col2]]
#     layout = [[col]]

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

    # sg.popup('You entered', values['-IN-'])
    return values
