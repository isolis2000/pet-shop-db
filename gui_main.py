import PySimpleGUI as sg
import database_read as dr
import database_insert as di
import database_delete as dd
import database_edit as de
import operator
import barcodes as bc


def search(ending: str, search_input: str):
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

        generated_table = sg.Table(
            values=tup[1],
            headings=tup[0],
            auto_size_columns=True,
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

        # General Events ----------------------------------------------------------------------
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        # Sorting Events ----------------------------------------------------------------------
        elif isinstance(event, tuple):
            if event[0].startswith("_TABLE"):
                ending = event[0][-2]
                for tup in generate_tabs_list:
                    if tup[2] == ending and (event[2][0] == -1 and event[2][1] != -1):
                        col_num_clicked = event[2][1]
                        tup[1] = search(ending, values[f"_INPUT_{ending}_"])
                        tup[1] = sort_table(tup[1], (col_num_clicked, 0))
                        window[f"_TABLE_{ending}_"].update(tup[1])
        # Other  Events -----------------------------------------------------------------------
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
                if tup[2] == ending:
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
        elif event == "_DELETE_P_":
            input_text = sg.popup_get_text(
                "Digite el nombre del producto o su código de barras.\n"
                + "Nota: no se podrá eliminar el producto si aun hay en el inventario."
            )
            if input_text != None:
                dd.remove_tipo_producto(input_text)
        elif event == "_SELL_S_":
            ending = event[-2]
            current_sale = dr.read_current_order()
            if len(current_sale) > 0:
                de.finalizar_compra()
                data_sale = search(ending, values["_INPUT_S_"])
                window["_TABLE_S_"].update(data_sale)
        elif event == "_GENERATE_CODES_":
            bc.generate_bar_codes_pdf(dr.read_product_types())
        elif event == "_CLOSING_":
            dr.closing_time()

    window.close()


main_window()
