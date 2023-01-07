from tkinter.simpledialog import askfloat
import PySimpleGUI as sg
import datetime

base64_str = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAB0ElEQVRIS+1VvU4CQRDe7QQTf3I+gyaowUQTbdTIG2ClrSWlhfoKkmhrZ6uVvIFGbCg0kR8x+gyehsLD0KzfzB24e7d3QEFMjAfF3Ny38+18M7sjO52OEiN8pI2gXLkHpRQba8sDUZcrD8Ap4FcieCvBHQjUUAS0ITEYgZvPiafDIi+YPz4Aka+gxE+3yUfv5G8eFYUCjPBO6drIwsjAzW8JJaW42i1gtRLbl2cUhUMJ+AMuYjPs0k4B64C/8PEzGolB8AYCt/0lbvf2eReb56fCSaXMaAikE7leFy+BPwF+DAQ3vSwiBPTlxf1gwJwzHS0aMlHIjqShP9mv78ArKWadKfbrMlklYgVI1J4syRKFpUuQKMdy6AWNCB5TdL0BYjNofXp9+152JaI0qbNIrpA9kU7ba8AEDA7qarODz6FGMlSKJ/Da3J7VepPDZBczotZoco9HbGCog9mv2ZThRJo6z3+MIrc8ZIBVtfozHyJarJOxja1nFwK/xaagk+O/JhFqQNo+BhItIYM4u9pAltCOMLpNARJq8C9RhpvgD0tEo5K6ojukk06rf5MGB1+zqaPWV39GbWRkEol52YWupyRWEIbnsnUm973xhgCMnOAbzkiRYGtBf20AAAAASUVORK5CYII="


def new_tipo_producto():

    layout = [
        [sg.Text("Insertar Tipo de Producto")],
        [sg.Text("Nombre:"), sg.InputText(key="nombre")],
        [sg.Text("Precio:"), sg.InputText(key="precio")],
        [sg.Text("Porcentaje de Ganancia:"), sg.InputText(key="ganancia")],
        [sg.Text("Codigo de Barras:"), sg.InputText(key="codigoBarras")],
        [sg.Button("Agregar", key="_ADD_"), sg.Button("Cancelar", key="_CANCEL_")],
    ]

    window = sg.Window("IBDPs first window", layout, font="Courier 12")
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


def new_producto():

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

    window = sg.Window("IBDPs first window", layout, font="Courier 12")
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


def edit_tipo_producto(data_selected):

    nombre = data_selected[0]
    precio = str(float(data_selected[1]) - float(data_selected[3]))
    porcentaje_ganancia = str(data_selected[2])
    codigo_barras = data_selected[4]

    layout = [
        [sg.Text("Insertar Tipo de Producto")],
        [sg.Text("Nombre:"), sg.InputText(nombre, key="nombre")],
        [sg.Text("Precio:"), sg.InputText(precio, key="precio")],
        [
            sg.Text("Porcentaje de Ganancia:"),
            sg.InputText(porcentaje_ganancia, key="ganancia"),
        ],
        [sg.Text("Codigo de Barras:"), sg.InputText(codigo_barras, key="codigoBarras")],
        [sg.Button("Agregar", key="_ADD_"), sg.Button("Cancelar", key="_CANCEL_")],
    ]

    window = sg.Window("IBDPs first window", layout, font="Courier 12")
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


def popup_select(the_list, select_multiple=False):
    layout = [
        [
            sg.Listbox(
                the_list,
                key="_LIST_",
                size=(45, len(the_list)),
                select_mode="extended" if select_multiple else "single",
                bind_return_key=True,
            ),
            sg.OK(),
        ]
    ]
    window = sg.Window("Select One", layout=layout)
    event, values = window.read()
    window.close()
    del window
    if select_multiple or values["_LIST_"] is None:
        return values["_LIST_"]
    else:
        return values["_LIST_"][0]


# usage examples
# nbr = popup_select([1,2,3]) # returns single number
# lst = popup_select([1,2,3],select_multiple=True) # returns list of selected items
