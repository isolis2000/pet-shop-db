import database_util as du

database = "Pet-shop.db"


def tipos_producto_ret_data(data: list):
    ret_data = []
    print(f"data: {data}")
    for row in data:

        name = row[0]
        price = row[1]
        price_no_iva = price / (1 + du.iva)
        profit = row[2]
        profit_percentage = round((profit / (price_no_iva - profit)) * 100, 2)
        profit_str = f"{profit} ({profit_percentage}%)"
        bar_code = row[3]
        provider_name = row[4]
        print("----------------------------------------------------------")
        print(f"price: {price}")
        print(f"price no iva: {price_no_iva}")
        print(f"profit: {profit}")

        new_row = (
            name,
            round(price),
            profit_str,
            provider_name,  # Proveedores
            bar_code,
        )
        # print(new_row)
        ret_data.append(new_row)

    return ret_data


def productos_ret_data(data: list):
    ret_data = []
    for row in data:
        new_row = (row[0], row[1], row[2], str(row[3]) + "%", row[4])
        # print(new_row)
        ret_data.append(new_row)
    return ret_data


def read_tipos_producto():
    data = du.exec_query(
        """
        SELECT 
            TP.nombre, 
            TP.precio, 
            TP.ganancia, 
            TP.codigoBarras,
            P.nombre
        FROM 
            TiposProducto AS TP
            INNER JOIN Proveedores AS P ON P.id = TP.idProveedor
        """
    )
    return tipos_producto_ret_data(data)


def read_tipos_producto_n(user_input: str):
    print(f"user_input: {user_input}")
    data = du.exec_query(
        f"""
        SELECT 
                TP.nombre, 
                TP.precio, 
                TP.ganancia, 
                TP.codigoBarras,
                P.nombre
            FROM 
                TiposProducto AS TP
                INNER JOIN Proveedores AS P ON P.id = TP.idProveedor
        WHERE 
            TP.nombre='{user_input}'
            OR TP.codigoBarras='{user_input}'
    """
    )

    return tipos_producto_ret_data(data)


def find_tipo_producto_id(codigo_barras: str):
    data = du.exec_query(
        f"""
    SELECT 
        id 
    FROM 
        TiposProducto 
    WHERE 
        codigoBarras='{codigo_barras}'"""
    )
    return data[0][0]


def read_productos():
    data = du.exec_query(
        """
        SELECT 
            TP.nombre, 
            P.fechaCompra, 
            P.fechaVencimiento, 
            P.descuento, 
            P.cantidad
        FROM 
            TiposProducto AS TP
            INNER JOIN Productos AS P ON TP.id = P.idTipoProducto
        """
    )
    # print(data)
    return productos_ret_data(data)


def read_productos_n(user_input: str):
    data = du.exec_query(
        f"""
        SELECT 
            TP.nombre, 
            P.fechaCompra, 
            P.fechaVencimiento, 
            P.descuento, 
            P.cantidad,
            P.id
        FROM 
            TiposProducto AS TP
            INNER JOIN Productos AS P ON TP.id = P.idTipoProducto
        WHERE
            TP.nombre = '{user_input}'
            OR TP.codigoBarras = '{user_input}'
        """
    )
    # print(data)
    return productos_ret_data(data)


# def read_product_plus_discount(user_input: str):
#     data = du.exec_query(
#         f"""
#         SELECT
#             TP.nombre,
#             (TP.precio - P.descuento) AS precio,
#             P.fechaCompra,
#             P.fechaVencimiento,
#             P.descuento,
#             P.cantidad
#         FROM
#             TiposProducto AS TP
#             INNER JOIN Productos AS P ON TP.id = P.idTipoProducto
#         WHERE
#             TP.nombre = '{user_input}'
#             OR TP.codigoBarras = '{user_input}'"""
#     )
#     # print(data)
#     ret_data = []
#     for row in data:
#         new_row = (row[0], row[1], row[2], str(row[3]) + "%", row[4])
#         # print(new_row)
#         ret_data.append(new_row)
#     return ret_data


def read_product_id(user_input: str):
    data = du.exec_query(
        f"""
        SELECT 
            id
        """
    )


def read_past_receipt(receipt_number):
    return du.exec_query(
        """
        SELECT  
            C.id,
            C.fecha,
            C.estado,
            (SUM())
        FROM 
            Compras_Productos AS CP
        INNER JOIN 
            Compras AS C ON (C.id = CP.idCompra)
        INNER JOIN
            Productos AS P ON (P.id = CP.idProducto)
        INNER JOIN
            TiposProducto AS TP ON (TP.id = P.idTipoProducto)
        WHERE   
            C.id = (
                SELECT MAX(C.id)  
                FROM Compras AS C
                WHERE C.estado = 'En Progreso');
    """
    )


def read_current_order():
    return du.exec_query(
        """
        SELECT  
            CP.Cantidad,
            TP.nombre,
            (TP.precio - P.descuento) * CP.Cantidad AS subtotal,
            P.descuento, 
            TP.codigoBarras,
            CP.id,
            P.id
        FROM 
            Compras_Productos AS CP
        INNER JOIN 
            Compras AS C ON (C.id = CP.idCompra)
        INNER JOIN
            Productos AS P ON (P.id = CP.idProducto)
        INNER JOIN
            TiposProducto AS TP ON (TP.id = P.idTipoProducto)
        WHERE   
            C.id = (
                SELECT MAX(C.id)  
                FROM Compras AS C
                WHERE C.estado = 'En Progreso');
    """
    )


def read_current_order_n(user_input: str):
    return du.exec_query(
        f"""
        SELECT  
            CP.Cantidad,
            TP.nombre,
            (TP.precio - P.descuento) AS subtotal,
            P.descuento, 
            TP.codigoBarras,
            CP.id
        FROM 
            Compras_Productos AS CP
        INNER JOIN 
            Compras AS C ON (C.id = CP.idCompra)
        INNER JOIN
            Productos AS P ON (P.id = CP.idProducto)
        INNER JOIN
            TiposProducto AS TP ON (TP.id = P.idTipoProducto)
        WHERE   
            C.id = (
                SELECT MAX(C.id)  
                FROM Compras AS C
                WHERE C.estado = 'En Progreso')
            AND 
                (TP.nombre = '{user_input}'
                OR TP.codigoBarras = '{user_input}');
    """
    )


def read_current_sale_id():
    return du.exec_query("SELECT MAX(id) FROM Compras")[0][0]


def find_proveedor_id(provider_name: str):
    return du.exec_query(
        f"""
        SELECT  
            id
        FROM 
            Proveedores
        WHERE   
            nombre = '{provider_name}'
        """
    )


def read_grooming():
    return []


def read_clients():
    return du.exec_query(
        f"""
        SELECT
            C.nombre,
            C.telefono,
            COUNT(M.nombre)
        FROM 
            Clientes AS C
        INNER JOIN 
            MascotasPeluqueria AS M ON M.idCliente = C.id
        """
    )


def read_clients_n(client_name: str):
    return du.exec_query(
        f"""
        SELECT
            C.nombre,
            C.telefono,
            COUNT(M.nombre)
        FROM 
            Clientes AS C
        INNER JOIN 
            MascotasPeluqueria AS M ON M.idCliente = C.id
        WHERE
            C.nombre = '{client_name}'
        GROUP BY
            C.nombre
        """
    )


def read_mascotas():
    return du.exec_query(
        f"""
        SELECT 
            M.nombre,
            C.nombre,
            R.nombre,
            M.notasAdicionales
        FROM
            Mascotaspeluqueria AS M
        INNER JOIN 
            Clientes AS C ON M.idCliente = C.id
        INNER JOIN 
            Razas AS R ON M.idRaza = R.id
        """
    )


def read_mascotas_n(pet_name: str):
    return du.exec_query(
        f"""
        SELECT 
            M.nombre,
            C.nombre,
            R.nombre,
            M.notasAdicionales
        FROM
            Mascotaspeluqueria AS M
        INNER JOIN 
            Clientes AS C ON M.idCliente = C.id
        INNER JOIN 
            Razas AS R ON M.idRaza = R.id
        WHERE
            M.nombre = '{pet_name}'
        """
    )


def read_registro():
    data = du.exec_query("SELECT * FROM Registro")
    print(f"Registro de datos:\n{data}")


def read_errores():
    data = du.exec_query("SELECT * FROM Errores")
    print("\ndatos: ")
    print(data)
