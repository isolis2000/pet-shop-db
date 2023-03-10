import gui_edit as we
import database_read as dr
import database_util as du
import barcodes as bc


def insert_provider(name: str):
    du.exec_query(
        f"""
    INSERT INTO Proveedores (
        nombre
    )
    VALUES (
        '{name}'
    )
    """
    )


def insert_product_type():

    dict_tipos = we.new_product_type()
    if dict_tipos == "Cancel":
        du.popup_message("Operación Cancelada")
        return

    provider_name = dict_tipos["proveedor"]
    proveedor_res = dr.find_provider_id(provider_name)
    print(f"proveedor_res: {proveedor_res}")
    if proveedor_res == []:
        insert_provider(provider_name)

    if du.verify_dict(dict_tipos):
        print(dict_tipos)
        print("NOMBRE: " + dict_tipos["nombre"])

        name = dict_tipos["nombre"]
        price = (
            float(dict_tipos["precio"])
            + float(dict_tipos["precio"]) * float(dict_tipos["ganancia"]) / 100
        ) * (1 + du.iva)
        profit = float(dict_tipos["precio"]) * float(dict_tipos["ganancia"]) / 100
        id_provider = dr.find_provider_id(provider_name)[0][0]

        # insert = "INSERT INTO TiposProducto (nombre, precio, ganancia, codigoBarras) VALUES (?, ?, ?, ?)",
        # (dict_tipos['nombre'], dict_tipos['precio'], dict_tipos['ganancia'], dict_tipos['codigoBarras'])

        # query_str = "INSERT INTO TiposProducto (nombre, precio, ganancia, codigoBarras) VALUES (?, ?, ?, ?)",
        #                 (dict_tipos['nombre'], str(float(dict_tipos['precio']) + float(dict_tipos['precio']) * float(dict_tipos['ganancia'])/100),
        #                  str(float(dict_tipos['precio']) * float(dict_tipos['ganancia'])/100), dict_tipos['codigoBarras'])"
        query_str = "SELECT MAX(seq)  FROM SQLITE_SEQUENCE WHERE name='TiposProducto'"
        id_to_insert = 1
        query_res = du.exec_query(query_str)[0][0]
        if query_res is not None:
            id_to_insert = int(query_res) + 1
        bar_code = bc.generate_code(id_to_insert, name)

        query_str = f"""
            INSERT INTO TiposProducto (
                nombre, 
                precio, 
                ganancia,
                codigoBarras,
                idProveedor) 
            VALUES (
                '{name}',
                {price},
                {profit},
                {bar_code},
                {id_provider})
        """
        print(query_str)
        if du.exec_query(query_str) != None:
            registry_str = f"""
                Se inserto un nuevo tipo de producto con los siguientes datos:
                    nombre: {dict_tipos["nombre"]}
                    precio: {dict_tipos["precio"]}
                    ganancia: {dict_tipos["ganancia"]}
                """
            du.insert_registro(registry_str)
        else:
            du.popup_message("Producto no se pudo insertar")
    else:
        du.popup_message(
            "Datos ingresados de manera incorrecta, favor verifique que todas las casillas esten llenas con lo que se pide"
        )


def insert_product():

    dict_product = we.new_product()
    if dict_product == "Cancel":
        du.popup_message("Operación Cancelada")
    elif du.verify_dict(dict_product):
        id_tipo_producto = dr.find_product_type_id(dict_product["productCode"])
        if id_tipo_producto != None:
            query_str = f"""
                INSERT INTO Productos (
                    fechaCompra,
                    fechaVencimiento,
                    descuento,
                    cantidad,
                    idTipoProducto)
                VALUES ('{dict_product["buyDate"]}', 
                '{dict_product["expirationDate"]}',
                {dict_product["discount"]},
                {dict_product["amount"]},
                {str(id_tipo_producto)})
            """
            print(query_str)
            if du.exec_query(query_str) is None:
                du.popup_message(
                    "Producto no se pudo agregar debido a un fallo en la base de datos"
                )
        else:
            du.popup_message(
                "Producto no se pudo agregar, favor verifique que exista este tipo de producto y que el codigo este correcto."
            )
    else:
        du.popup_message(
            "Datos ingresados de manera incorrecta, favor verifique que todas las casillas esten llenas con lo que se pide"
        )


def add_to_sale(empty=False):

    popup_input = du.popup_input("Digite el código del producto")
    if popup_input is None:
        du.popup_message("Operación Cancelada")
        return

    print(f"input: {popup_input}")
    products_list = dr.read_products_in_inventory(popup_input)
    print(f"list: {products_list}")

    if products_list == []:
        du.popup_message("No existe ningún producto con este código")
        return

    if empty:
        query_str = f"""
                INSERT INTO Compras (
                    fecha,
                    estado,
                    totalAPagar,
                    vuelto,
                    idTipoPago,
                    idCliente
                    )
                VALUES (
                    '{du.get_today_date()}',
                    'En Progreso',
                    0,
                    0,
                    0,
                    0)
        """
        du.exec_query(query_str)
        print(query_str)

    product_to_add = []
    current_sale = dr.read_current_sale_id()

    if len(products_list) > 1:
        product_to_add = we.popup_select(products_list)
    else:
        product_to_add = products_list[0]

    print(f"Pl: {product_to_add}")

    if product_to_add is None or product_to_add == []:
        return

    product_quantity = int(product_to_add[4])
    amount_to_add = 0
    valid_amount = False

    while not valid_amount:
        amount_to_add = du.popup_input("Digite la cantidad")
        if amount_to_add is None:
            return
        elif int(amount_to_add) <= product_quantity:
            valid_amount = True

    print(product_to_add)

    product_id = product_to_add[5]

    query_str = f"""
        INSERT INTO Compras_Productos (
            idCompra,
            idProducto,
            cantidad
        ) VALUES (
            {current_sale},
            {product_id},
            {amount_to_add}
        )
    """

    du.exec_query(query_str)

    # query_str = f"""
    #     INSERT INTO
    # """
    print(product_to_add)
    print(current_sale)


def insert_client():
    dict_client = we.new_client()

    if dict_client["name"] == "":
        du.popup_message("Es necesario un nombre para agregar un cliente")
    else:
        query_str = ""
        if dict_client["phone"] == "":
            query_str = f"""
                    INSERT INTO Clientes (nombre)
                    VALUES ('{dict_client["name"]}')
                """
        else:
            query_str = f"""
                    INSERT INTO Clientes (nombre, telefono)
                    VALUES (
                        '{dict_client["name"]}',
                        '{dict_client["phone"]}')
                """
        print(query_str)
        du.exec_query(query_str)

    # if dict_product == 'Cancel':
    #     du.popup_message("Operación Cancelada")
    # elif du.verify_dict(dict_product):
    #     id_tipo_producto = dr.find_product_type_id(dict_product['productCode'])
    #     if id_tipo_producto != None:
    # query_str = ("""
    #     INSERT INTO Productos (
    #         fechaCompra,
    #         fechaVencimiento,
    #         descuento,
    #         cantidad,
    #         id_tipo_producto)
    #     VALUES ('""" +
    #             dict_product['buyDate'] + "', '" +
    #             dict_product['expirationDate'] + "', " +
    #             dict_product['discount'] + ", " +
    #             dict_product['amount'] + ", " +
    #             str(id_tipo_producto) + ")")
    #         print(query_str)
    #         if du.exec_query(query_str) != None:
    #             du.popup_message(
    #                 "Producto agregado al inventario de manera exitosa")
    #         else:
    #             du.popup_message(
    #                 "Producto no se pudo agregar debido a un fallo en la base de datos")
    #     else:
    #         du.popup_message(
    #             "Producto no se pudo agregar, favor verifique que exista este tipo de producto y que el codigo este correcto.")
    # else:
    #     du.popup_message(
    #         "Datos ingresados de manera incorrecta, favor verifique que todas las casillas esten llenas con lo que se pide")
