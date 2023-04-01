import PySimpleGUI as sg
import database_read as dr
import database_insert as di
import database_delete as dd
import database_edit as de
import operator
import barcodes as bc

# themes = [
#     sg.theme("Reddit"),
#     sg.theme("LightGreen"),
#     sg.theme("LightGrey5"),
#     sg.theme("DarkTanBlue")
#     ]

# # New function added
# def repack(widget, option):
#     pack_info = widget.pack_info()
#     pack_info.update(option)
#     widget.pack(**pack_info)


# Search functions ---------------------------------------------------------------


# def search_products(search_input: str):
#     if search_input == "":
#         return dr.read_product_types()
#     else:
#         return dr.read_product_types(search_input)


# def search_inventory(search_input: str):
#     if search_input == "":
#         return dr.read_products_in_inventory()
#     else:
#         return dr.read_products_in_inventory(search_input)


# def search_current_sale(search_input: str):
#     if search_input == "":
#         return dr.read_current_order()
#     else:
#         return dr.read_current_order(search_input)


# def search_clients(search_input: str):
#     if search_input == "":
#         return dr.read_clients()
#     else:
#         return dr.read_clients(search_input)


# def search_pets(search_input: str):
#     if search_input == "":
#         return dr.read_pets()
#     else:
#         return dr.read_pets(search_input)


# def search_receipts(search_input: str):
#     if search_input == "":
#         return dr.read_past_receipts()
#     else:
#         return dr.read_past_receipts(search_input)


def search(ending: str, search_input: str):
    print(f"search: ending-{ending}, search_input-{search_input}")
    if ending == "P":
        return dr.read_product_types(search_input)
    elif ending == "I":
        return dr.read_products_in_inventory(search_input)
    elif ending == "S":
        return dr.read_current_order(search_input)
    elif ending == "C":
        return dr.read_clients(search_input)
    elif ending == "G":
        return dr.read_pets(search_input)
    elif ending == "R":
        return dr.read_past_receipts(search_input)


def new_insert(ending: str, new_sale=False):
    if ending == "P":
        di.insert_product_type()
    elif ending == "I":
        di.insert_product()
    elif ending == "S":
        di.add_to_sale(new_sale)
    elif ending == "C":
        di.insert_client()


def edit(ending: str, data_selected: list):
    if ending == "P":
        de.edit_product_type(data_selected)
    elif ending == "S":
        de.edit_sale_prod_quantity(data_selected[5])
    elif ending == "C":
        de.edit_client(data_selected[0])


def sort_table(table, cols):
    """sort a table by multiple columns
    table: a list of lists (or tuple of tuples) where each inner list
           represents a row
    cols:  a list (or tuple) specifying the column numbers to sort by
           e.g. (1,0) would sort by column 1, then by column 0
    """
    for col in reversed(cols):
        try:
            table = sorted(table, key=operator.itemgetter(col))
        except Exception as e:
            sg.popup_error("Error in sort_table", "Exception in sort_table", e)
    return table


# Main function -------------------------------------------------------------------


def main_window():

    headings_products = ["Nombre", "Precio", "Ganancia (₡)", "Código", "Proveedor"]
    headings_inventory = ["Nombre", "Compra", "Expiración", "Descuento", "Cantidad"]
    headings_sale = ["Cantidad", "Descripción", "Subtotal", "Descuento", "Código"]
    headings_clients = ["Nombre", "Telefono"]
    headings_grooming = ["Mascota", "Propietario", "Raza", "Notas", "Monto"]
    headings_receipts = ["Numero", "Fecha", "Nombre", "Total", "Tipo de Pago", "Estado"]
    # Click para revisar datos de cliente
    # headings_receipts = ["Fecha", ""]

    data_products = dr.read_product_types()
    data_inventory = dr.read_products_in_inventory()
    data_sale = dr.read_current_order()
    data_grooming = dr.read_grooming()
    data_clients = dr.read_clients()
    data_receipts = dr.read_past_receipts()

    generate_tabs_list = [
        [headings_products, data_products, "P", "Productos"],
        [headings_inventory, data_inventory, "I", "Inventario"],
        [headings_sale, data_sale, "S", "Venta"],
        [headings_clients, data_clients, "C", "Clientes"],
        # [headings_grooming, data_grooming, "G", "Peluquería"],
        [headings_receipts, data_receipts, "R", "Facturas"],
    ]
    generated_tabs_layout = []

    for tup in generate_tabs_list:

        key_letter = tup[2]
        input_key = f"_INPUT_{key_letter}_"
        search_key = f"_SEARCH_{key_letter}_"
        add_key = f"_ADD_{key_letter}_"
        edit_key = f"_EDIT_{key_letter}_"
        table_key = f"_TABLE_{key_letter}_"
        tab_key = f"_TAB_{key_letter}_"

        # generated_tab = None

        generated_table = sg.Table(
            values=tup[1],
            headings=tup[0],
            auto_size_columns=True,
            # max_col_width=20,
            # def_col_width=20,
            # col_widths=60,
            display_row_numbers=False,
            justification="center",
            enable_events=True,
            enable_click_events=True,
            select_mode=sg.TABLE_SELECT_MODE_BROWSE,
            expand_x=True,
            expand_y=True,
            row_height=35,
            key=table_key,
        )

        generated_tab = [
            [
                sg.InputText(size=13, expand_x=True, key=input_key),
                sg.Button("Buscar", key=search_key),
                sg.Button("Agregar", key=add_key),
                sg.Button("Editar", key=edit_key),
            ],
            [generated_table],
        ]

        if key_letter == "S":
            sell_key = f"_SELL_{key_letter}_"
            generated_tab[0] = generated_tab[0][:4]
            generated_tab[0].append(sg.Button("Vender", key=sell_key))
        elif key_letter == "I":
            delete_key = f"_DELETE_{key_letter}_"
            generated_tab[0].append(sg.Button("Eliminar", key=delete_key))
        elif key_letter == "R":
            generated_tab[0] = generated_tab[0][:2]

        generated_tabs_layout.append(sg.Tab(tup[3], generated_tab, key=tab_key))

    other_functions_tab = [
        [sg.Button("Generar codigos", pad=(5, 10), key="_GENERATE_CODES_")],
        [sg.Button("Cierre de Caja", pad=(5, 10), key="_CLOSING_")],
        # [sg.Text("Color de interfaz")],
        # [sg.Slider((0, len(sg.theme_list())), orientation="h",enable_events=True, disable_number_display=True , key='_COLOR_SLIDER_')]
    ]

    other_functions_layout = [
        [sg.VPush()],
        [
            sg.Push(),
            sg.Column(other_functions_tab, element_justification="c"),
            sg.Push(),
        ],
        [sg.VPush()],
    ]

    generated_tabs_layout.append(
        sg.Tab("Otras funciones", other_functions_layout, key="_TAB_O_")
    )

    layout = [
        [
            sg.TabGroup(
                [[tab for tab in generated_tabs_layout]],
                enable_events=True,
                expand_x=True,
                expand_y=True,
                key="_TAB_",
            )
        ]
    ]

    window = sg.Window(
        "Ventana Principal",
        layout,
        size=(1000, 500),
        font="Courier 13",
        resizable=True,
        element_justification="c",
        finalize=True,
    )

    window["_INPUT_P_"].bind("<Return>", "_Enter")
    window["_INPUT_I_"].bind("<Return>", "_Enter")
    window["_INPUT_S_"].bind("<Return>", "_Enter")
    # window["_INPUT_G_"].bind("<Return>", "_Enter")
    window["_INPUT_C_"].bind("<Return>", "_Enter")

    window["_INPUT_P_"].set_focus()
    data_selected = []

    while True:

        window.refresh()
        event, values = window.read()

        print("_------------------------------------------------_")
        print(f"Event: {event}")
        print("_------------------------------------------------_")
        print(f"Values: {values}")

        #     generate_tabs_list = [
        #     (headings_products, data_products, "P", "Productos"),
        #     (headings_inventory, data_inventory, "I", "Inventario"),
        #     (headings_sale, data_sale, "S", "Venta"),
        #     (headings_grooming, data_grooming, "G", "Peluquería"),
        #     (headings_clients, data_clients, "C", "Clientes"),
        # ]

        # General Events ------------------------------------------------------------------------
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        # Sorting Events ----------------------------------------------------------------------
        elif isinstance(event, tuple):
            # TABLE CLICKED Event has value in format ('-TABLE=', '+CLICKED+', (row,col))
            if event[0].startswith("_TABLE"):
                ending = event[0][-2]
                for tup in generate_tabs_list:
                    if tup[2] == ending and (event[2][0] == -1 and event[2][1] != -1):
                        col_num_clicked = event[2][1]
                        tup[1] = search(ending, values[f"_INPUT_{ending}_"])
                        tup[1] = sort_table(tup[1], (col_num_clicked, 0))
                        window[f"_TABLE_{ending}_"].update(tup[1])

        elif event.startswith("_TAB_") and values["_TAB_"] != "_TAB_O_":
            ending = values["_TAB_"][-2]
            search_input = values[f"_INPUT_{ending}_"]
            for tup in generate_tabs_list:
                if tup[2] == ending:
                    tup[1] = search(ending, search_input)
                    window[f"_TABLE_{ending}_"].update(tup[1])
                    window[f"_INPUT_{ending}_"].set_focus()
                    data_selected = []

        elif event.startswith("_SEARCH"):
            ending = event[-2]
            for tup in generate_tabs_list:
                if tup[2] == ending:
                    tup[1] = search(ending, values[f"_INPUT_{ending}_"])
                    window[f"_TABLE_{ending}_"].update(tup[1])

        elif event.startswith("_INPUT") and event.endswith("_Enter"):
            ending = event[-8]
            for tup in generate_tabs_list:
                if tup[2] == ending:
                    tup[1] = search(ending, values[f"_INPUT_{ending}_"])
                    window[f"_TABLE_{ending}_"].update(tup[1])

        elif event.startswith("_ADD"):
            ending = event[-2]
            for tup in generate_tabs_list:
                # print(f"tup: {tup}")
                if tup[2] == ending:
                    # print(f"bool(tup[1]): {tup[1]}")
                    new_insert(ending, not tup[1])
                    tup[1] = search(ending, values[f"_INPUT_{ending}_"])
                    window[f"_TABLE_{ending}_"].update(tup[1])

        elif event.startswith("_TABLE"):
            ending = event[-2]
            for tup in generate_tabs_list:
                if tup[2] == ending:
                    data_selected = [tup[1][row] for row in values[event]]

        elif event.startswith("_EDIT"):
            ending = event[-2]
            for tup in generate_tabs_list:
                if tup[2] == ending and len(data_selected) != 0:
                    edit(ending, data_selected[0])
                    tup[1] = search(ending, values[f"_INPUT_{ending}_"])
                    window[f"_TABLE_{ending}_"].update(tup[1])

        # elif event == "_COLOR_SLIDER_":
        #     sg.theme(sg.theme_list()[int(values[event])])

        # if event[0] == "_TABLE_P_":
        #     if event[2][0] == -1 and event[2][1] != -1:
        #         col_num_clicked = event[2][1]
        #         data_products = search_products(values["_INPUT_P_"])
        #         data_products = sort_table(data_products, (col_num_clicked, 0))
        #         window["_TABLE_P_"].update(data_products)
        # elif event[0] == "_TABLE_I_":
        #     if event[2][0] == -1 and event[2][1] != -1:
        #         col_num_clicked = event[2][1]
        #         data_inventory = search_inventory(values["_INPUT_I_"])
        #         data_inventory = sort_table(data_inventory, (col_num_clicked, 0))
        #         window["_TABLE_I_"].update(data_inventory)
        # elif event[0] == "_TABLE_S_":
        #     if event[2][0] == -1 and event[2][1] != -1:
        #         col_num_clicked = event[2][1]
        #         data_sale = search_current_sale(values["_INPUT_S_"])
        #         data_sale = sort_table(data_sale, (col_num_clicked, 0))
        #         window["_TABLE_S_"].update(data_sale)

        # if values["_TAB_"] == "_TAB_P_":
        #     data_products = search_products(values["_INPUT_P_"])
        #     window["_TABLE_P_"].update(data_products)
        #     window["_INPUT_P_"].set_focus()
        #     data_selected = []
        # elif values["_TAB_"] == "_TAB_I_":
        #     print("Entro")
        #     data_inventory = search_inventory(values["_INPUT_I_"])
        #     window["_TABLE_I_"].update(data_inventory)
        #     window["_INPUT_I_"].set_focus()
        #     data_selected = []
        # elif values["_TAB_"] == "_TAB_S_":
        #     data_sale = search_current_sale(values["_INPUT_S_"])
        #     window["_TABLE_S_"].update(data_sale)
        #     window["_INPUT_S_"].set_focus()
        #     data_selected = []

        # Products Events -----------------------------------------------------------------------
        # elif event == "_SEARCH_P_" or event == "_INPUT_P_" + "_Enter":
        #     data_products = search_products(values["_INPUT_P_"])
        #     window["_TABLE_P_"].update(data_products)
        # elif event == "_ADD_P_":
        #     di.insert_product_type()
        #     data_products = search_products(values["_INPUT_P_"])
        #     window["_TABLE_P_"].update(data_products)
        elif event == "_DELETE_P_":
            input_text = sg.popup_get_text(
                "Digite el nombre del producto o su código de barras.\n"
                + "Nota: no se podrá eliminar el producto si aun hay en el inventario."
            )
            if input_text != None:
                dd.remove_tipo_producto(input_text)
        # elif event == "_TABLE_P_":
        #     data_selected = [data_products[row] for row in values[event]]
        #     print(f"data_selected: {data_selected}")
        # window["_TABLE_P_"].update(data_products)
        # elif event == "_EDIT_P_" and data_selected != []:
        #     de.edit_product_type(data_selected[0])

        # Inventory Events ---------------------------------------------------------------------
        # elif event == "_SEARCH_I_" or event == "_INPUT_I_" + "_Enter":
        #     data_inventory = search_inventory(values["_INPUT_I_"])
        #     window["_TABLE_I_"].update(data_inventory)
        # elif event == "_ADD_I_":
        #     di.insert_product()
        #     data_inventory = search_inventory(values["_INPUT_I_"])
        #     window["_TABLE_I_"].update(data_inventory)
        # elif event == "_TABLE_I_":
        #     data_selected = [data_inventory[row] for row in values[event]]
        #     print(f"data_selected: {data_selected}")

        # Sale Events -------------------------------------------------------------------------
        # elif event == "_SEARCH_S_" or event == "_INPUT_S_" + "_Enter":
        #     data_sale = search_current_sale(values["_INPUT_S_"])
        #     window["_TABLE_S_"].update(data_sale)
        # elif event == "_ADD_S_":
        #     if data_sale == []:
        #         di.add_to_sale(True)
        #     else:
        #         di.add_to_sale()
        #     data_sale = search_current_sale(values["_INPUT_S_"])
        #     window["_TABLE_S_"].update(data_sale)
        # elif event == "_TABLE_S_":
        #     data_selected = [data_sale[row] for row in values[event]]
        # elif event == "_EDIT_S_" and data_selected != []:
        #     print(tup)
        #     print(tup)
        #     de.edit_sale_prod_quantity(data_selected[0][5])
        #     data_sale = search(values["_INPUT_S_"])
        #     window["_TABLE_S_"].update(data_sale)
        elif event == "_SELL_S_":
            print(f"tup: {tup}")

            current_sale = dr.read_current_order()
            print(f"cs: {current_sale}")
            if len(current_sale) > 0:
                de.finalizar_compra()
                data_sale = search(values["_INPUT_S_"])
                window["_TABLE_S_"].update(data_sale)
        elif event == "_GENERATE_CODES_":
            bc.generate_bar_codes_pdf()
        elif event == "_CLOSING_":
            dr.closing_time()

        # print(f"data_selected: {data_selected}")
        # print(f"data_products: {data_products}")
        # print(f"data_inventory: {data_inventory}")
        # print(f"data_sale: {data_sale}")
        # # print(f"values[event]: {values[event]}")
        # print(f"values: {values}")

        # window["_TABLE_P_"].update(data_products)
        # window["_TABLE_I_"].update(data_inventory)
        # window["_TABLE_S_"].update(data_sale)

    window.close()


# finalizar funciones adicionales
# revision completa de bugs
# Arreglar ventas cantidad de producto negativa
# Revisar que descuento funcione de la misma manera


main_window()

# Arreglar edit tipos producto (intentar hacer un cambio para ver error)
# Arreglar edit tipos (provider)
# Cantidad de dígitos después de editar tipo producto
