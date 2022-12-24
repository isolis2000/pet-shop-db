from tkinter.simpledialog import askfloat
import PySimpleGUI as sg

def newTipoProducto():

    #     col2 = sg.Column([[sg.Frame('Accounts:', [[sg.Column([[sg.Listbox(['Account '+str(i) for i in range(1,16)],
    #                                                       key='-ACCT-LIST-',size=(15,20)),]],size=(150,400))]])]],pad=(0,0))
    #     col1 = sg.Column([[sg.Text("Segunda columna")],
    #             [sg.Text("Segunda columna 2")]])

    layout = [[sg.Text("Insertar Tipo de Producto")],
              [sg.Text('Nombre:'), sg.InputText(key='nombre')],
              [sg.Text('Precio:'), sg.InputText(key='precio')],
              [sg.Text('Ganancia:'), sg.InputText(key='ganancia')],
              [sg.Text('Codigo de Barras:'), sg.InputText(key='codigoBarras')],
              [sg.Submit(), sg.Cancel()]
              ]

#     layout = [[col1, col3, col2]]
#     layout = [[col]]

    window = sg.Window('IBDPs first window', layout, font='Courier 12')

    event, values = window.read()

    window.close()

    # sg.popup('You entered', values['-IN-'])
    return values