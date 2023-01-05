from tkinter.simpledialog import askfloat
import PySimpleGUI as sg
import databaseRead as dr
import databaseInsert as di
import databaseDelete as dd
import databaseEdit as de
import operator

sg.theme("DarkAmber")

# def main_window():
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
#     data_products = dr.read_tipos_producto()
#     print(data_products)

#     table = sg.Table(values=data_products,
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
#                 data_products = dr.read_tipos_producto()
#             else:
#                 data_products = dr.readTiposProductoN(values['-INPUT_P-'])

#             window['-TABLE_P-'].update(data_products)

#     window.close()

def search_products(input):
    if input == '':
        return dr.read_tipos_producto()
    else:
        return dr.readTiposProductoN(input)


def sort_table(table, cols):
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
            sg.popup_error('Error in sort_table', 'Exception in sort_table', e)
    return table


def main_window():

    headings_products = ['Nombre', 'Precio',
                        '%' + ' Ganancia', 'Ganancia', 'Código']
    headings_inventory = ['Nombre', 'Compra',
                         'Expiración', 'Descuento', 'Cantidad']
    headings_sale = ['Cantidad', 'Descripción',
                    'Subtotal', 'Descuento', 'Código']

    data_products = dr.read_tipos_producto()
    data_inventory = dr.read_productos()
    data_sale = dr.read_current_sale()

    print(data_sale)

    generate_tabs_list = [(headings_products, data_products, 'P', 'Productos'),
                        (headings_inventory, data_inventory, 'I', 'Inventario'),
                        (headings_sale, data_sale, 'S', 'Venta')
                        ]
    generated_tabs_layout = []

    # tableProducts = sg.Table(values=data_products,
    #                          headings=headings_products,
    #                          auto_size_columns=False,
    #                          max_col_width=20,
    #                          def_col_width=20,
    #                          # col_widths=60,
    #                          display_row_numbers=False,
    #                          justification='center',
    #                          enable_events=True,
    #                          enable_click_events=True,
    #                          select_mode=sg.TABLE_SELECT_MODE_BROWSE,
    #                          key='-TABLE_P-',
    #                          row_height=35)

    # tableInventory = sg.Table(values=data_inventory,
    #                           headings=headings_inventory,
    #                           auto_size_columns=False,
    #                           max_col_width=20,
    #                           def_col_width=20,
    #                           # col_widths=60,
    #                           display_row_numbers=False,
    #                           justification='center',
    #                           enable_events=True,
    #                           enable_click_events=True,
    #                           select_mode=sg.TABLE_SELECT_MODE_BROWSE,
    #                           key='-TABLE_I-',
    #                           row_height=35)

    # tableSales = sg.Table(values=data_sale,
    #                       headings=headings_sale,
    #                       auto_size_columns=False,
    #                       max_col_width=20,
    #                       def_col_width=20,
    #                       # col_widths=60,
    #                       display_row_numbers=True,
    #                       justification='center',
    #                       enable_events=True,
    #                       enable_click_events=True,
    #                       select_mode=sg.TABLE_SELECT_MODE_BROWSE,
    #                       key='-TABLE_V-',
    #                       row_height=35)

    for tup in generate_tabs_list:

        input_key = '-INPUT_' + tup[2] + '-'
        search_key = '_SEARCH_' + tup[2] + '_'
        add_key = '_ADD_' + tup[2] + '_'
        delete_key = '_DELETE_' + tup[2] + '_'
        edit_key = '_EDIT_' + tup[2] + '_'
        table_key = '-TABLE_' + tup[2] + '-'
        tab_key = '-TAB_' + tup[2] + '-'

        generated_table = sg.Table(values=tup[1],
                                  headings=tup[0],
                                  auto_size_columns=False,
                                  max_col_width=20,
                                  def_col_width=20,
                                  # col_widths=60,
                                  display_row_numbers=False,
                                  justification='center',
                                  enable_events=True,
                                  enable_click_events=True,
                                  select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                                  key=table_key,
                                  row_height=35)

        generated_tab = [[sg.InputText(size=(59), key=input_key),
                         sg.Button('Buscar', key=search_key),
                         sg.Button('Agregar', key=add_key),
                         sg.Button('Eliminar', key=delete_key),
                         sg.Button('Editar', key=edit_key)],
                        [generated_table]
                        ]

        generated_tabs_layout.append(sg.Tab(tup[3], generated_tab, key=tab_key))

    # tabProductsLayout = [[sg.InputText(key='-INPUT_P-'),
    #                       sg.Button('Buscar', key='_SEARCH_P_'),
    #                       sg.Button('Agregar', key='_ADD_P_'),
    #                       sg.Button('Eliminar', key='_DELETE_P_'),
    #                       sg.Button('Editar', key='_EDIT_P_')],
    #                      [tableProducts]
    #                      ]

    # tabInventoryLayout = [[sg.InputText(key='-INPUT_I-'),
    #                        sg.Button('Buscar', key='_SEARCH_I_'),
    #                        sg.Button('Agregar', key='_ADD_I_'),
    #                        sg.Button('Eliminar', key='_DELETE_I_'),
    #                        sg.Button('Editar', key='_EDIT_I_')],
    #                       [tableInventory]
    #                       ]

    # tabSalesLayout = [[sg.InputText(key='-INPUT_I-'),
    #                    sg.Button('Buscar', key='_SEARCH_I_'),
    #                    sg.Button('Agregar', key='_ADD_I_'),
    #                    sg.Button('Eliminar', key='_DELETE_I_'),
    #                    sg.Button('Editar', key='_EDIT_I_')],
    #                   [tableInventory]
    #                   ]

    # layout = [[sg.TabGroup([[sg.Tab('Productos', generated_tabs_layout, key='-TAB_P-'),
    #                          sg.Tab('Inventario', tabInventoryLayout,
    #                                 key='-TAB_I-'),
    #                          sg.Tab('Ventas', tabSalesLayout, key='-TAB_V-')]])]
    #           ]

    # [print(i) for i in x]

    layout = [[sg.TabGroup([[tab for tab in generated_tabs_layout]])]]

    window = sg.Window('Ventana Principal', layout,
                       font='Courier 12', finalize=True)

    window['-INPUT_P-'].bind("<Return>", "_Enter")
    window['-INPUT_I-'].bind("<Return>", "_Enter")
    window['-INPUT_S-'].bind("<Return>", "_Enter")

    window['-INPUT_P-'].set_focus()
    data_selected = []

    # TP.nombre,
    # (TP.precio - P.descuento) AS precio,
    # P.fechaCompra,
    # P.fechaVencimiento,
    # P.descuento,
    # P.cantidad

    while True:
        window.refresh()
        event, values = window.read()

        # General Events
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        elif event == '-TAB_P-':
            window['-INPUT_P-'].set_focus()
        elif event == '-TAB_I-':
            window['-INPUT_I-'].set_focus()
        elif event == '-TAB_V-':
            window['-INPUT_I-'].set_focus()

        # Products Events
        elif isinstance(event, tuple):
            # TABLE CLICKED Event has value in format ('-TABLE=', '+CLICKED+', (row,col))
            if event[0] == '-TABLE_P-':
                print("Entro")
                if event[2][0] == -1 and event[2][1] != -1:
                    col_num_clicked = event[2][1]
                    data_products = search_products(values['-INPUT_P-'])
                    new_table = sort_table(data_products, (col_num_clicked, 0))
                    window['-TABLE_P-'].update(new_table)
                    data_products = [data_products[0]] + new_table
        elif event == '_SEARCH_P_' or event == "-INPUT_P-" + "_Enter":
            data_products = search_products(values['-INPUT_P-'])
            window['-TABLE_P-'].update(data_products)
        elif event == '_ADD_P_':
            di.insert_tipo_producto()
        elif event == '_DELETE_P_':
            input = sg.popup_get_text('Digite el nombre del producto o su codigo de barras.\n' +
                                      'Nota: no se podra eliminar el producto si aun hay en el inventario.')
            if input != None:
                dd.remove_tipo_producto(input)
        elif event == '-TABLE_P-':
            data_selected = [data_products[row] for row in values[event]]
        elif event == '_EDIT_P_' and data_selected != []:
            de.edit_tipo_producto(data_selected[0])

        # Inventory Events
        elif event == '_SEARCH_I_' or event == "-INPUT_I-" + "_Enter":
            if values['-INPUT_I-'] == '':
                data_inventory = dr.read_productos()
            else:
                data_inventory = dr.read_productos_n(values['-INPUT_I-'])
            window['-TABLE_I-'].update(data_inventory)
        elif event == '_ADD_I_':
            di.insert_producto()
            if values['-INPUT_I-'] == '':
                data_inventory = dr.read_productos()
            else:
                data_inventory = dr.read_productos_n(values['-INPUT_I-'])
            window['-TABLE_I-'].update(data_inventory)

        # Sale Events
        elif event == '_SEARCH_S_' or event == "-INPUT_S-" + "_Enter":
            if values['-INPUT_S-'] == '':
                data_sale = dr.read_current_sale()
            # else:
            #     data_sale = dr.read_current_sale_n(values['-INPUT_S-'])
            window['-TABLE_I-'].update(data_sale)
        elif event == '_ADD_S_' and values['-INPUT_S-'] != '':
            if data_sale == []:
                di.add_to_venta(values['-INPUT_S-'], True)
            else:
                di.add_to_venta(values['-INPUT_S-'])
            if values['-INPUT_S-'] == '':
                data_sale = dr.read_current_sale()
            # else:
            #     data_sale = dr.read_productos_n(values['-INPUT_S-'])
            window['-TABLE_I-'].update(data_sale)
            # data_sale = 

    window.close()

# Arreglar cantidades en venta

# Proveedores

# Validar que no se elimine si hay en inventario
# Hacer boton de editar
# Validar que no existan productos con el mismo codigo
# Probar funcionamiento de unique en codigo de barras y nombre

main_window()
