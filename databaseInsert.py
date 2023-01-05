import windowsEdit as we
import databaseRead as dr
import databaseUtil as du
import datetime


def insert_tipo_producto():

    dict_tipos = we.new_tipo_producto()

    if dict_tipos == 'Cancel':
        du.popup_message("Operacion cancelada")
    elif du.verify_dict(dict_tipos):
        print(dict_tipos)
        print("NOMBRE: " + dict_tipos['nombre'])

        # insert = "INSERT INTO TiposProducto (nombre, precio, ganancia, codigoBarras) VALUES (?, ?, ?, ?)",
        # (dict_tipos['nombre'], dict_tipos['precio'], dict_tipos['ganancia'], dict_tipos['codigoBarras'])

        # query_str = "INSERT INTO TiposProducto (nombre, precio, ganancia, codigoBarras) VALUES (?, ?, ?, ?)",
        #                 (dict_tipos['nombre'], str(float(dict_tipos['precio']) + float(dict_tipos['precio']) * float(dict_tipos['ganancia'])/100),
        #                  str(float(dict_tipos['precio']) * float(dict_tipos['ganancia'])/100), dict_tipos['codigoBarras'])"
        query_str = ("""
            INSERT INTO TiposProducto (
                nombre, 
                precio, 
                ganancia, 
                codigoBarras) 
            VALUES ('""" +
                     dict_tipos['nombre'] + "', " +
                     str(float(dict_tipos['precio']) + float(dict_tipos['precio'])
                         * float(dict_tipos['ganancia'])/100) + ", " +
                     str(float(dict_tipos['precio']) *
                         float(dict_tipos['ganancia'])/100) + ", '" +
                     dict_tipos['codigoBarras'] + "')")
        print(query_str)
        if du.exec_query(query_str) != None:
            registry_str = ("Se inserto un nuevo tipo de producto con los siguientes datos: \n\t" +
                            "nombre: " + dict_tipos['nombre'] + "\n\t" +
                            "precio: " + str(dict_tipos['precio']) + "\n\t" +
                            "ganancia: " + str(dict_tipos['ganancia']) + "\n\t" +
                            "codigo de barras: " + dict_tipos['codigoBarras'])
            du.insert_registro(registry_str)
            du.popup_message("Producto insertado de manera exitosa")
        else:
            du.popup_message("Producto no se pudo insertar")
    else:
        du.popup_message(
            "Datos ingresados de manera incorrecta, favor verifique que todas las casillas esten llenas con lo que se pide")


def insert_producto():

    dict_product = we.new_producto()
    if dict_product == 'Cancel':
        du.popup_message("Operacion cancelada")
    elif du.verify_dict(dict_product):
        id_tipo_producto = dr.find_tipo_producto_id(
            dict_product['productCode'])
        if id_tipo_producto != None:
            query_str = ("""
                INSERT INTO Productos (
                    fechaCompra,
                    fechaVencimiento,
                    descuento,
                    cantidad,
                    idTipoProducto)
                VALUES ('""" +
                         dict_product['buyDate'] + "', '" +
                         dict_product['expirationDate'] + "', " +
                         dict_product['discount'] + ", " +
                         dict_product['ammount'] + ", " +
                         str(id_tipo_producto) + ")")
            print(query_str)
            if du.exec_query(query_str) != None:
                du.popup_message(
                    "Producto agregado al inventario de manera exitosa")
            else:
                du.popup_message(
                    "Producto no se pudo agregar debido a un fallo en la base de datos")
        else:
            du.popup_message(
                "Producto no se pudo agregar, favor verifique que exista este tipo de producto y que el codigo este correcto.")
    else:
        du.popup_message(
            "Datos ingresados de manera incorrecta, favor verifique que todas las casillas esten llenas con lo que se pide")


def add_to_venta(input: str, empty=False):

    products_list = dr.read_productos_n(input)

    if products_list == []:
        du.popup_message("No existe ningún producto con este código o nombre")
        return

    if empty:
        query_str = f"""
                INSERT INTO Compras (
                    fecha,
                    estado)
                VALUES (
                    '{datetime.datetime.today().strftime('%Y-%m-%d')}',
                    'En Progreso')"""
        du.exec_query(query_str)
        print(query_str)

    product_to_add = []
    current_sale = dr.read_current_sale_id()

    if len(products_list) > 1:
        product_to_add = we.popup_select(products_list)
    else:
        product_to_add = products_list

    ammount_to_add = du.popup_input("Digite la cantidad")

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
            {ammount_to_add}
        )
    """

    du.exec_query(query_str)

    # query_str = f"""
    #     INSERT INTO 
    # """
    print(product_to_add)
    print(current_sale)

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
    #             dict_product['ammount'] + ", " +
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
