from tkinter.simpledialog import askfloat
import PySimpleGUI as sg
import databaseRead as dr
import databaseInsert as di
import databaseDelete as dd
import databaseEdit as de
import operator

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
#     dataProducts = dr.readTiposProducto()
#     print(dataProducts)

#     table = sg.Table(values=dataProducts,
#                      headings=headings,
#                      auto_size_columns=False,
#                      max_col_width=30,
#                      def_col_width=30,
#                      # col_widths=60,
#                      display_row_numbers=False,
#                      justification='center',
#                      key='-TABLE_P-',
#                      row_height=35)

#     layout = [[sg.InputText(key='-INPUT_P-'), sg.Button('Buscar', key='_SEARCH_P_'), sg.Button('Agregar', key='_ADD_P_')],
#               [table]
#               ]

#     window = sg.Window('Ventana Principal', layout, font='Courier 12')

#     while True:
#         window.refresh()
#         event, values = window.read()
#         if event == "Exit" or event == sg.WIN_CLOSED:
#             break
#         elif event == '_SEARCH_P_':
#             if values['-INPUT_P-'] == '':
#                 dataProducts = dr.readTiposProducto()
#             else:
#                 dataProducts = dr.readTiposProductoN(values['-INPUT_P-'])

#             window['-TABLE_P-'].update(dataProducts)

#     window.close()

def searchProducts(input):
    if input == '':
        return dr.readTiposProducto()
    else:
        return dr.readTiposProductoN(input)

def sortTable(table, cols):
    """ sort a table by multiple columns
        table: a list of lists (or tuple of tuples) where each inner list
               represents a row
        cols:  a list (or tuple) specifying the column numbers to sort by
               e.g. (1,0) would sort by column 1, then by column 0
    """
    for col in reversed(cols):
        try:
            table = sorted(table, key=operator.itemgetter(col))
        except Exception as e:
            sg.popup_error('Error in sortTable', 'Exception in sortTable', e)
    return table

def mainWindow():

    headingsProducts = ['Nombre', 'Precio',  '%' + ' Ganancia', 'Ganancia', 'Codigo']
    headingsInventory = ['Nombre', 'Compra', 'Expiracion', 'Descuento', 'Cantidad']
    dataProducts = dr.readTiposProducto()
    dataInventory = dr.readProductos()

    tableProducts = sg.Table(values=dataProducts,
                     headings=headingsProducts,
                     auto_size_columns=False,
                     max_col_width=20,
                     def_col_width=20,
                     # col_widths=60,
                     display_row_numbers=False,
                     justification='center',
                     enable_events=True,
                     enable_click_events=True,
                     select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                     key='-TABLE_P-',
                     row_height=35)

    tableInventory = sg.Table(values=dataInventory,
                     headings=headingsInventory,
                     auto_size_columns=False,
                     max_col_width=20,
                     def_col_width=20,
                     # col_widths=60,
                     display_row_numbers=False,
                     justification='center',
                     enable_events=True,
                     enable_click_events=True,
                     select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                     key='-TABLE_I-',
                     row_height=35)

    

    tabProductsLayout = [[sg.InputText(key='-INPUT_P-'),
                          sg.Button('Buscar', key='_SEARCH_P_'),
                          sg.Button('Agregar', key='_ADD_P_'),
                          sg.Button('Eliminar', key='_DELETE_P_'),
                          sg.Button('Editar', key='_EDIT_P_')],
                         [tableProducts]
                         ]

    tabInventoryLayout = [[sg.InputText(key='-INPUT_I-'),
                           sg.Button('Buscar', key='_SEARCH_I_'),
                           sg.Button('Agregar', key='_ADD_I_'),
                           sg.Button('Eliminar', key='_DELETE_I_'),
                           sg.Button('Editar', key='_EDIT_I_')],
                          [tableInventory]
                          ]

    tabSalesLayout = [[sg.Text("Ventas")]]

    layout = [
        [sg.TabGroup([[sg.Tab('Productos', tabProductsLayout),
                       sg.Tab('Inventario', tabInventoryLayout),
                       sg.Tab('Ventas', tabSalesLayout)]])]]

    window = sg.Window('Ventana Principal', layout,
                       font='Courier 12', finalize=True)
    window['-INPUT_P-'].bind("<Return>", "_Enter")
    dataSelected = []

    while True:
        window.refresh()
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if isinstance(event, tuple):
        # TABLE CLICKED Event has value in format ('-TABLE=', '+CLICKED+', (row,col))
            if event[0] == '-TABLE_P-':
                print("Entro")
                if event[2][0] == -1 and event[2][1] != -1:           # Header was clicked and wasn't the "row" column
                    col_num_clicked = event[2][1]
                    dataProducts = searchProducts(values['-INPUT_P-'])
                    new_table = sortTable(dataProducts,(col_num_clicked, 0))
                    window['-TABLE_P-'].update(new_table)
                    dataProducts = [dataProducts[0]] + new_table
        elif event == '_SEARCH_P_' or event == "-INPUT_P-" + "_Enter":
            dataProducts = searchProducts(values['-INPUT_P-'])
            window['-TABLE_P-'].update(dataProducts)
        elif event == '_ADD_P_':
            di.insertTipoProducto()
        elif event == '_DELETE_P_':
            input = sg.popup_get_text('Digite el nombre del producto o su codigo de barras.\n' +
                                      'Nota: no se podra eliminar el producto si aun hay en el inventario.')
            if input != None:
                dd.removeTipoProducto(input)
        elif event == '-TABLE_P-':
            dataSelected = [dataProducts[row] for row in values[event]]
        elif event == '_EDIT_P_' and dataSelected != []:
            de.editTipoProducto(dataSelected[0])
        elif event == '_SEARCH_I_' or event == "-INPUT_I-" + "_Enter":
            if values['-INPUT_I-'] == '':
                dataInventory = dr.readProductos()
            else:
                dataInventory = dr.readProductosN(values['-INPUT_I-'])
            window['-TABLE_I-'].update(dataInventory)
        elif event == '_ADD_I_':
            di.insertProducto()

    window.close()

# URGENTE!!!!!!!!!
# Descuento -> TiposProducto
# Proveedores

# Validar que no se elimine si hay en inventario
# Hacer boton de editar
# Validar que no existan productos con el mismo codigo
# Probar funcionamiento de unique en codigo de barras y nombre

mainWindow()
