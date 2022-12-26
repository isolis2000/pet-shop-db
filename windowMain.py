from tkinter.simpledialog import askfloat
import PySimpleGUI as sg
import databaseRead as dr
import databaseEdit as de
import databaseDelete as dd

sg.theme("DarkTanBlue")

# def mainWindow():
#     layout =


# def newTipoProducto():

#     #     col2 = sg.Column([[sg.Frame('Accounts:', [[sg.Column([[sg.Listbox(['Account '+str(i) for i in range(1,16)],
#     #                                                       key='-ACCT-LIST-',size=(15,20)),]],size=(150,400))]])]],pad=(0,0))
#     #     col1 = sg.Column([[sg.Text("Segunda columna")],
#     #             [sg.Text("Segunda columna 2")]])

#     layout = [[sg.Text("Insertar Tipo de Producto")],
#               [sg.Text('Nombre:'), sg.InputText(key='nombre')],
#               [sg.Text('Precio:'), sg.InputText(key='precio')],
#               [sg.Text('Ganancia:'), sg.InputText(key='ganancia')],
#               [sg.Text('Codigo de Barras:'), sg.InputText(key='codigoBarras')],
#               [sg.Submit(), sg.Cancel()]
#               ]

# #     layout = [[col1, col3, col2]]
# #     layout = [[col]]

#     window = sg.Window('IBDPs first window', layout, font='Courier 12')

#     event, values = window.read()

#     window.close()

#     # sg.popup('You entered', values['-IN-'])
#     return values


# def searchTiposProducto():

#     headings = ['Nombre', 'Precio',  '%' + ' Ganancia', 'Ganancia', 'Codigo']
#     data = dr.readTiposProducto()
#     print(data)

#     table = sg.Table(values=data,
#                      headings=headings,
#                      auto_size_columns=False,
#                      max_col_width=30,
#                      def_col_width=30,
#                      # col_widths=60,
#                      display_row_numbers=False,
#                      justification='center',
#                      key='-TABLE-',
#                      row_height=35)

#     layout = [[sg.InputText(key='-INPUT-'), sg.Button('Buscar', key='_SEARCH_'), sg.Button('Agregar', key='_ADD_')],
#               [table]
#               ]

#     window = sg.Window('Ventana Principal', layout, font='Courier 12')

#     while True:
#         window.refresh()
#         event, values = window.read()
#         if event == "Exit" or event == sg.WIN_CLOSED:
#             break
#         elif event == '_SEARCH_':
#             if values['-INPUT-'] == '':
#                 data = dr.readTiposProducto()
#             else:
#                 data = dr.readTiposProductoN(values['-INPUT-'])

#             window['-TABLE-'].update(data)

#     window.close()

def mainWindow():

    headings = ['Nombre', 'Precio',  '%' + ' Ganancia', 'Ganancia', 'Codigo']
    data = dr.readTiposProducto()

    table = sg.Table(values=data,
                     headings=headings,
                     auto_size_columns=False,
                     max_col_width=20,
                     def_col_width=20,
                     # col_widths=60,
                     display_row_numbers=False,
                     justification='center',
                     enable_events=True,
                     select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                     key='-TABLE-',
                     row_height=35)

    tabProductsLayout = [[sg.InputText(key='-INPUT-'),
                          sg.Button('Buscar', key='_SEARCH_'),
                          sg.Button('Agregar', key='_ADD_'),
                          sg.Button('Eliminar', key='_DELETE_'),
                          sg.Button('Editar', key='_EDIT_')],
                         [table]
                         ]
    tabInventory = [[sg.InputText(key='-INPUT-'),
                     sg.Button('Buscar', key='_SEARCH_'),
                     sg.Button('Agregar', key='_ADD_'),
                     sg.Button('Eliminar', key='_DELETE_'),
                     sg.Button('Editar', key='_EDIT_')],
                    [table]
                    ]

    tabSalesLayout = [[sg.Text("Ventas")]]

    layout = [
        [sg.TabGroup([[sg.Tab('Productos', tabProductsLayout), sg.Tab('Ventas', tabSalesLayout)]])]]

    window = sg.Window('Ventana Principal', layout, font='Courier 12')
    dataSelected = []

    while True:
        window.refresh()
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        elif event == '_SEARCH_':
            if values['-INPUT-'] == '':
                data = dr.readTiposProducto()
            else:
                data = dr.readTiposProductoN(values['-INPUT-'])
            window['-TABLE-'].update(data)
        elif event == '_ADD_':
            de.insertTipoProducto()
        elif event == '_DELETE_':
            input = sg.popup_get_text('Digite el nombre del producto o su codigo de barras.\n' +
                                      'PRECAUCION: Si hay mas de un producto con este nombre o codigo, todos seran eliminados.\n' +
                                      'Ademas, no se podra eliminar el producto si aun hay en el inventario.')
            print(input)
            if input != None:
                dd.removeTipoProducto(input)
        elif event == '-TABLE-':
            dataSelected = [data[row] for row in values[event]]
        elif event == '_EDIT_' and dataSelected != []:
            print(dataSelected)
            de.editTipoProducto(dataSelected[0])

    window.close()


# Validar que no se elimine si hay en inventario
# Hacer inventario
# Hacer boton de editar
#
mainWindow()
