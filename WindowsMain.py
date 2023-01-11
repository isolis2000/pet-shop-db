import PySimpleGUI as sg
import DatabaseRead as dr
import DatabaseInsert as di
import DatabaseDelete as dd
import DatabaseEdit as de
import operator

sg.theme("DarkAmber")


# Search functions ---------------------------------------------------------------


def search_products(input: str):
    if input == "":
        return dr.read_tipos_producto()
    else:
        return dr.read_tipos_producto_n(input)


def search_inventory(input: str):
    if input == "":
        return dr.read_productos()
    else:
        return dr.read_productos_n(input)


def search_current_sale(input: str):
    if input == "":
        return dr.read_current_sale()
    else:
        return dr.read_current_sale_n(input)


# Generic functions ---------------------------------------------------------------


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

    headings_products = ["Nombre", "Precio", "%" + " Ganancia", "Ganancia", "Código"]
    headings_inventory = ["Nombre", "Compra", "Expiración", "Descuento", "Cantidad"]
    headings_sale = ["Cantidad", "Descripción", "Subtotal", "Descuento", "Código"]

    data_products = dr.read_tipos_producto()
    data_inventory = dr.read_productos()
    data_sale = dr.read_current_sale()

    print(data_sale)
    generate_tabs_list = [
        (headings_products, data_products, "P", "Productos"),
        (headings_inventory, data_inventory, "I", "Inventario"),
        (headings_sale, data_sale, "S", "Venta"),
    ]
    generated_tabs_layout = []

    for tup in generate_tabs_list:

        key_letter = tup[2]
        input_key = f"-INPUT_{key_letter}-"
        search_key = f"_SEARCH_{key_letter}_"
        add_key = f"_ADD_{key_letter}_"
        delete_key = f"_DELETE_{key_letter}_"
        edit_key = f"_EDIT_{key_letter}_"
        table_key = f"-TABLE_{key_letter}-"
        tab_key = f"-TAB_{key_letter}-"

        generated_tab = None

        generated_table = sg.Table(
            values=tup[1],
            headings=tup[0],
            auto_size_columns=False,
            max_col_width=20,
            def_col_width=20,
            # col_widths=60,
            display_row_numbers=False,
            justification="center",
            enable_events=True,
            enable_click_events=True,
            select_mode=sg.TABLE_SELECT_MODE_BROWSE,
            key=table_key,
            row_height=35,
        )

        if key_letter == "S":
            sell_key = f"_SELL_{key_letter}_"
            sell_text = "Vender"
            generated_tab = [
                [
                    sg.InputText(size=(59 - 4 - len(sell_text)), key=input_key),
                    sg.Button("Buscar", key=search_key),
                    sg.Button("Agregar", key=add_key),
                    sg.Button("Eliminar", key=delete_key),
                    sg.Button("Editar", key=edit_key),
                    sg.Button(sell_text, key=sell_key),
                ],
                [generated_table],
            ]
        else:
            generated_tab = [
                [
                    sg.InputText(size=(59), key=input_key),
                    sg.Button("Buscar", key=search_key),
                    sg.Button("Agregar", key=add_key),
                    sg.Button("Eliminar", key=delete_key),
                    sg.Button("Editar", key=edit_key),
                ],
                [generated_table],
            ]

        generated_tabs_layout.append(sg.Tab(tup[3], generated_tab, key=tab_key))

    layout = [[sg.TabGroup([[tab for tab in generated_tabs_layout]])]]

    window = sg.Window("Ventana Principal", layout, font="Courier 12", finalize=True)

    window["-INPUT_P-"].bind("<Return>", "_Enter")
    window["-INPUT_I-"].bind("<Return>", "_Enter")
    window["-INPUT_S-"].bind("<Return>", "_Enter")

    window["-INPUT_P-"].set_focus()
    data_selected = []

    while True:
        window["-TABLE_P-"].update(data_products)
        window["-TABLE_I-"].update(data_inventory)
        window["-TABLE_S-"].update(data_sale)
        window.refresh()
        event, values = window.read()
        print(event)

        # General Events ------------------------------------------------------------------------
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        elif event == "-TAB_P-":
            window["-INPUT_P-"].set_focus()
            data_selected = []
        elif event == "-TAB_I-":
            window["-INPUT_I-"].set_focus()
            data_selected = []
        elif event == "-TAB_S-":
            window["-INPUT_S-"].set_focus()
            data_selected = []

        # Products Events -----------------------------------------------------------------------
        elif event == "_SEARCH_P_" or event == "-INPUT_P-" + "_Enter":
            data_products = search_products(values["-INPUT_P-"])
        elif event == "_ADD_P_":
            di.insert_tipo_producto()
            data_products = search_products(values["-INPUT_P-"])
        elif event == "_DELETE_P_":
            input = sg.popup_get_text(
                "Digite el nombre del producto o su código de barras.\n"
                + "Nota: no se podrá eliminar el producto si aun hay en el inventario."
            )
            if input != None:
                dd.remove_tipo_producto(input)
        elif event == "-TABLE_P-":
            data_selected = [data_products[row] for row in values[event]]
        elif event == "_EDIT_P_" and data_selected != []:
            de.edit_tipo_producto(data_selected[0])

        # Inventory Events ---------------------------------------------------------------------
        elif event == "_SEARCH_I_" or event == "-INPUT_I-" + "_Enter":
            data_inventory = search_inventory(values["-INPUT_I-"])
        elif event == "_ADD_I_":
            di.insert_producto()
            data_inventory = search_inventory(values["-INPUT_I-"])
        elif event == "-TABLE_I-":
            data_selected = [data_inventory[row] for row in values[event]]

        # Sale Events -------------------------------------------------------------------------
        elif event == "_SEARCH_S_" or event == "-INPUT_S-" + "_Enter":
            data_sale = search_current_sale(values["-INPUT_S-"])
        elif event == "_ADD_S_":
            if data_sale == []:
                di.add_to_venta(True)
            else:
                di.add_to_venta()
            data_sale = search_current_sale(values["-INPUT_S-"])
        elif event == "-TABLE_S-":
            data_selected = [data_sale[row] for row in values[event]]
        elif event == "_EDIT_S_" and data_selected != []:
            de.edit_sale_prod_quantity(data_selected[0][5])
            data_sale = search_current_sale(values["-INPUT_S-"])
        elif event == "_SELL_S_":
            de.edit_estado_compra("finalizado")
            data_sale = search_current_sale(values["-INPUT_S-"])

        # Sorting Events ----------------------------------------------------------------------
        elif isinstance(event, tuple):
            # TABLE CLICKED Event has value in format ('-TABLE=', '+CLICKED+', (row,col))
            if event[0] == "-TABLE_P-":
                if event[2][0] == -1 and event[2][1] != -1:
                    col_num_clicked = event[2][1]
                    data_products = search_products(values["-INPUT_P-"])
                    new_table = sort_table(data_products, (col_num_clicked, 0))
                    data_products = [data_products[0]] + new_table
            elif event[0] == "-TABLE_I-":
                if event[2][0] == -1 and event[2][1] != -1:
                    col_num_clicked = event[2][1]
                    data_inventory = search_inventory(values["-INPUT_I-"])
                    new_table = sort_table(data_inventory, (col_num_clicked, 0))
                    data_inventory = [data_inventory[0]] + new_table
            elif event[0] == "-TABLE_S-":
                if event[2][0] == -1 and event[2][1] != -1:
                    col_num_clicked = event[2][1]
                    data_sale = search_current_sale(values["-INPUT_S-"])
                    new_table = sort_table(data_sale, (col_num_clicked, 0))
                    data_sale = [data_sale[0]] + new_table

    window.close()


# Proveedores
# Cambiar el test.pdf por nombre real
# Remover items de inventario con la compra
# Tabla facturas para visualizar lo que se ha hecho

# Validar que no se elimine si hay en inventario
# Hacer boton de editar
# Validar que no existan productos con el mismo codigo
# Probar funcionamiento de unique en codigo de barras y nombre


main_window()
