import gui_edit as we
import database_read as dr
import database_util as du
import datetime


def insert_proveedor(name: str):
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


def insert_tipo_producto():

    dict_tipos = we.new_tipo_producto()
    if dict_tipos == "Cancel":
        du.popup_message("Operación cancelada")
        return

    provider_name = dict_tipos["proveedor"]
    proveedor_res = dr.find_proveedor_id(provider_name)
    print(f"proveedor_res: {proveedor_res}")
    if proveedor_res == []:
        insert_proveedor(provider_name)
    id_proveedor = dr.find_proveedor_id(provider_name)[0][0]

    print(f"id_proveedor: {id_proveedor}")
    if du.verify_dict(dict_tipos):
        print(dict_tipos)
        print("NOMBRE: " + dict_tipos["nombre"])

        # insert = "INSERT INTO TiposProducto (nombre, precio, ganancia, codigoBarras) VALUES (?, ?, ?, ?)",
        # (dict_tipos['nombre'], dict_tipos['precio'], dict_tipos['ganancia'], dict_tipos['codigoBarras'])

        # query_str = "INSERT INTO TiposProducto (nombre, precio, ganancia, codigoBarras) VALUES (?, ?, ?, ?)",
        #                 (dict_tipos['nombre'], str(float(dict_tipos['precio']) + float(dict_tipos['precio']) * float(dict_tipos['ganancia'])/100),
        #                  str(float(dict_tipos['precio']) * float(dict_tipos['ganancia'])/100), dict_tipos['codigoBarras'])"
        query_str = f"""
            INSERT INTO TiposProducto (
                nombre, 
                precio, 
                ganancia,
                codigoBarras,
                idProveedor) 
            VALUES (
                '{dict_tipos["nombre"]}',
                {(float(dict_tipos["precio"]) 
                + float(dict_tipos["precio"]) 
                * float(dict_tipos["ganancia"])/100)
                * (1 + du.iva)},
                {float(dict_tipos["precio"]) 
                * float(dict_tipos["ganancia"])/100}, 
                '{dict_tipos["codigoBarras"]}',
                {id_proveedor})
        """
        print(query_str)
        if du.exec_query(query_str) != None:
            registry_str = f"""
                Se inserto un nuevo tipo de producto con los siguientes datos:
                    nombre: {dict_tipos["nombre"]}
                    precio: {dict_tipos["precio"]}
                    ganancia: {dict_tipos["ganancia"]}
                    codigo de barras: {dict_tipos["codigoBarras"]}
                """
            du.insert_registro(registry_str)
        else:
            du.popup_message("Producto no se pudo insertar")
    else:
        du.popup_message(
            "Datos ingresados de manera incorrecta, favor verifique que todas las casillas esten llenas con lo que se pide"
        )


def insert_producto():

    dict_product = we.new_producto()
    if dict_product == "Cancel":
        du.popup_message("Operación cancelada")
    elif du.verify_dict(dict_product):
        id_tipo_producto = dr.find_tipo_producto_id(dict_product["productCode"])
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
            if du.exec_query(query_str) == None:
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


def add_to_venta(empty=False):

    popup_input = du.popup_input("Digite el código del producto")
    if popup_input == None:
        du.popup_message("Operación cancelada")
        return

    products_list = dr.read_productos_n(popup_input)

    if products_list == []:
        du.popup_message("No existe ningún producto con este código o nombre")
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

    product_quantity = int(product_to_add[4])
    amount_to_add = 0
    valid_amount = False

    while not valid_amount:
        amount_to_add = du.popup_input("Digite la cantidad")
        if amount_to_add == None:
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
    #     du.popup_message("Operacion cancelada")
    # elif du.verify_dict(dict_product):
    #     id_tipo_producto = dr.find_tipo_producto_id(dict_product['productCode'])
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
