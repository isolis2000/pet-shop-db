from tkinter.simpledialog import askfloat
import PySimpleGUI as sg
import datetime

base64_str = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAB0ElEQVRIS+1VvU4CQRDe7QQTf3I+gyaowUQTbdTIG2ClrSWlhfoKkmhrZ6uVvIFGbCg0kR8x+gyehsLD0KzfzB24e7d3QEFMjAfF3Ny38+18M7sjO52OEiN8pI2gXLkHpRQba8sDUZcrD8Ap4FcieCvBHQjUUAS0ITEYgZvPiafDIi+YPz4Aka+gxE+3yUfv5G8eFYUCjPBO6drIwsjAzW8JJaW42i1gtRLbl2cUhUMJ+AMuYjPs0k4B64C/8PEzGolB8AYCt/0lbvf2eReb56fCSaXMaAikE7leFy+BPwF+DAQ3vSwiBPTlxf1gwJwzHS0aMlHIjqShP9mv78ArKWadKfbrMlklYgVI1J4syRKFpUuQKMdy6AWNCB5TdL0BYjNofXp9+152JaI0qbNIrpA9kU7ba8AEDA7qarODz6FGMlSKJ/Da3J7VepPDZBczotZoco9HbGCog9mv2ZThRJo6z3+MIrc8ZIBVtfozHyJarJOxja1nFwK/xaagk+O/JhFqQNo+BhItIYM4u9pAltCOMLpNARJq8C9RhpvgD0tEo5K6ojukk06rf5MGB1+zqaPWV39GbWRkEol52YWupyRWEIbnsnUm973xhgCMnOAbzkiRYGtBf20AAAAASUVORK5CYII="


def new_product_type():

    layout = [
        [sg.Text("Insertar Tipo de Producto")],
        [sg.Text("Nombre:"), sg.InputText(key="nombre")],
        [sg.Text("Precio:"), sg.InputText(key="precio")],
        [sg.Text("Porcentaje de Ganancia:"), sg.InputText(key="ganancia")],
        [sg.Text("Nombre del Proveedor:"), sg.InputText(key="proveedor")],
        [sg.Button("Agregar", key="_ADD_"), sg.Button("Cancelar", key="_CANCEL_")],
    ]

    window = sg.Window("", layout, font="Courier 13")
    submited = False
    event, values = window.read()

    while not submited:
        if event == "_ADD_":
            submited = True
        elif event == "_CANCEL_" or event == sg.WIN_CLOSED:
            values = "Cancel"
            submited = True

    window.close()
    return values


def new_product():

    layout = [
        [sg.Text("Agregar Producto")],
        [
            sg.Text("Fecha de compra:"),
            sg.InputText(key="buyDate"),
            sg.CalendarButton(
                "", target="buyDate", image_data=base64_str, format="%Y-%m-%d"
            ),
        ],
        [
            sg.Text("Fecha de vencimiento:"),
            sg.InputText(key="expirationDate"),
            sg.CalendarButton(
                "", target="expirationDate", image_data=base64_str, format="%Y-%m-%d"
            ),
        ],
        [sg.Text("Porcentaje de descuento:"), sg.InputText(key="discount")],
        [sg.Text("Cantidad:"), sg.InputText(key="amount")],
        [sg.Text("Codigo del producto:"), sg.InputText(key="productCode")],
        [sg.Button("Agregar", key="_ADD_"), sg.Button("Cancelar", key="_CANCEL_")],
    ]

    window = sg.Window("", layout, font="Courier 13")
    submited = False
    event, values = window.read()

    while not submited:
        if event == "_TODAY_":
            window.Element("buyDate").update(
                datetime.datetime.today().strftime("%Y-%m-%d")
            )
        elif event == "_ADD_":
            submited = True
        elif event == "_CANCEL_" or event == sg.WIN_CLOSED:
            values = "Cancel"
            submited = True

    window.close()
    return values


def edit_product_type(product: list, iva: int):
    print(f"product: {product}")
    nombre = product[0]
    precio = str(product[1] * (1 - iva))
    porcentaje_ganancia = str(product[2])
    codigo_barras = product[3]
    proveedor = product[4]

    layout = [
        [sg.Text("Editar Tipo de Producto")],
        [sg.Text("Nombre:"), sg.InputText(nombre, key="nombre")],
        [sg.Text("Precio:"), sg.InputText(precio, key="precio")],
        [
            sg.Text("Porcentaje de Ganancia:"),
            sg.InputText(porcentaje_ganancia, key="ganancia"),
        ],
        [sg.Text("Codigo de Barras:"), sg.InputText(codigo_barras, key="codigoBarras")],
        [sg.Text("Proveedor:"), sg.InputText(proveedor, key="proveedor")],
        [sg.Button("Editar", key="_EDIT_"), sg.Button("Cancelar", key="_CANCEL_")],
    ]

    window = sg.Window("", layout, font="Courier 13")
    submited = False
    event, values = window.read()

    while not submited:
        if event == "_EDIT_":
            submited = True
        elif event == "_CANCEL_" or event == sg.WIN_CLOSED:
            values = "Cancel"
            submited = True

    window.close()
    return values


def edit_client(selected_client: list):
    name = selected_client[0]
    phone_num = selected_client[1]
    if phone_num == "Sin numero":
        phone_num = ""
    layout = [
        [
            sg.Text(
                "Cambie los datos que desee y recuerde que el número\ntelefónico va sin separacion de ningún tipo"
            )
        ],
        [sg.Text("Nombre:"), sg.InputText(name, key="name")],
        [sg.Text("Número:"), sg.InputText(phone_num, key="phone")],
        [sg.Button("Editar", key="_EDIT_"), sg.Button("Cancelar", key="_CANCEL_")],
    ]

    window = sg.Window("", layout, font="Courier 13")
    submited = False
    event, values = window.read()

    while not submited:
        if event == "_EDIT_":
            submited = True
        elif event == "_CANCEL_" or event == sg.WIN_CLOSED:
            values = "Cancel"
            submited = True

    window.close()
    return values


def new_client():
    layout = [
        [sg.Text("Digite los datos del cliente")],
        [sg.Text("Nombre:"), sg.InputText(key="name")],
        [sg.Text("Número:"), sg.InputText(key="phone")],
        [sg.Button("Agregar", key="_ADD_"), sg.Button("Cancelar", key="_CANCEL_")],
    ]

    window = sg.Window("", layout, font="Courier 13")
    event, values = window.read()

    while True:
        if event == "_ADD_":
            break
        elif event == "_CANCEL_" or event == sg.WIN_CLOSED:
            values = "Cancel"
            break

    window.close()
    return values


def popup_select(the_list: list, select_multiple=False):
    layout = [
        [
            sg.Listbox(
                the_list,
                size=(45, len(the_list)),
                select_mode="extended" if select_multiple else "single",
                bind_return_key=True,
                key="_LIST_",
            ),
            sg.OK(),
        ]
    ]
    window = sg.Window("", layout=layout, font="Courier 13", resizable=False)
    event, values = window.read()
    window.close()
    del window
    if select_multiple or values["_LIST_"] is None or len(values["_LIST_"]) == 0:
        return values["_LIST_"]
    else:
        return values["_LIST_"][0]


def popup_select_combo(the_list: list):
    layout = [
        [
            sg.Combo(
                the_list,
                default_value=the_list[0],
                bind_return_key=True,
                key="_SELECTION_",
            ),
            sg.Ok(),
        ]
    ]
    window = sg.Window("", layout=layout, font="Courier 13", resizable=False)
    event, values = window.read()
    window.close()
    del window
    return values["_SELECTION_"]


def popup_finalize_sale(payments_list: list, clients_list: list, final_price: float):
    layout = [
        [sg.Text(f"Precio total: ₡{final_price}")],
        [
            sg.Text("Tipo de pago:"),
            sg.Combo(
                payments_list, default_value=payments_list[0], key="_PAYMENT_TYPE_"
            ),
        ],
        [
            sg.Text("Cliente:"),
            sg.Combo(clients_list, default_value=clients_list[0], key="_CLIENT_"),
        ],
        [sg.Ok()],
    ]
    window = sg.Window("", layout, font="Courier 13", resizable=True)
    event, values = window.read()
    window.close()
    final_values = [values["_PAYMENT_TYPE_"], values["_CLIENT_"]]
    if (
        values["_PAYMENT_TYPE_"] is None
        or values["_CLIENT_"] is None
        or values["_PAYMENT_TYPE_"] == ""
        or values["_CLIENT_"] == ""
    ):
        return None
    elif values["_PAYMENT_TYPE_"] == "Efectivo":
        payment_text = """
            ¿Con cuánto va a cancelar?
        Escriba un 0 si es el monto exacto.
        """
        layout = [
            [sg.Text(payment_text)],
            [sg.InputText("", key="_PAYMENT_")],
            [sg.Ok()],
        ]
        window = sg.Window("", layout, font="Courier 13", resizable=True)
        event, values = window.read()
        window.close()
        final_values.append(values["_PAYMENT_"])
    return final_values


# edit_client(["1","2"])


# usage examples
# nbr = popup_select([1,2,3]) # returns single number
# lst = popup_select([1,2,3],select_multiple=True) # returns list of selected items

# print(
#     popup_finalize_sale(
#         ["No especificado", "Efectivo", "Tarjeta", "SINPE"], ["Huu", "Chan"]
#     )
# )
