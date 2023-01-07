import DatabaseUtil as du

database = "Pet-shop.db"


def read_tipos_producto():
    data = du.exec_query(
        """
        SELECT 
            nombre, 
            precio, 
            ganancia, 
            codigoBarras 
        FROM 
            TiposProducto
        """
    )
    # print(data)
    ret_data = []
    for row in data:
        new_row = (
            row[0],
            round(row[1]),
            str(round((row[2] / (row[1] - row[2])) * 100, 2)) + "%",
            round(row[2], 2),
            row[3],
        )
        # print(new_row)
        ret_data.append(new_row)
    # c.execute('SELECT * FROM Productos')
    # data = c.fetchall()
    # print(data)
    # for row in data:
    #     print(row)
    return ret_data


def read_tipos_producto_n(input: str):
    data = du.exec_query(
        f"""
    SELECT 
        nombre, 
        precio, 
        ganancia, 
        codigoBarras 
    FROM 
        TiposProducto 
    WHERE 
        nombre='{input}'
        OR codigoBarras='{input}'
    """
    )
    ret_data = []
    for row in data:
        new_row = (
            row[0],
            round(row[1]),
            str(round((row[2] / (row[1] - row[2])) * 100, 2)) + "%",
            round(row[2], 2),
            row[3],
        )
        # print(new_row)
        ret_data.append(new_row)
    return ret_data


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
    ret_data = []
    for row in data:
        new_row = (row[0], row[1], row[2], str(row[3]) + "%", row[4])
        # print(new_row)
        ret_data.append(new_row)
    return ret_data


def read_productos_n(input: str):
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
            TP.nombre = '{input}'
            OR TP.codigoBarras = '{input}'
        """
    )
    # print(data)
    ret_data = []
    for row in data:
        new_row = (row[0], row[1], row[2], str(row[3]) + "%", row[4], row[5])
        # print(new_row)
        ret_data.append(new_row)
    return ret_data


def read_product_plus_discount(input: str):
    data = du.exec_query(
        f"""
        SELECT 
            TP.nombre, 
            (TP.precio - P.descuento) AS precio,
            P.fechaCompra, 
            P.fechaVencimiento, 
            P.descuento, 
            P.cantidad
        FROM 
            TiposProducto AS TP
            INNER JOIN Productos AS P ON TP.id = P.idTipoProducto
        WHERE
            TP.nombre = '{input}'
            OR TP.codigoBarras = '{input}'"""
    )
    # print(data)
    ret_data = []
    for row in data:
        new_row = (row[0], row[1], row[2], str(row[3]) + "%", row[4])
        # print(new_row)
        ret_data.append(new_row)
    return ret_data


def read_current_sale():
    return du.exec_query(
        """
        SELECT  
            CP.Cantidad,
            TP.nombre,
            (TP.precio - P.descuento) AS subtotal,
            P.descuento, 
            TP.codigoBarras
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


def read_current_sale_n(input: str):
    print(f"input: {input}")
    return du.exec_query(
        f"""
        SELECT  
            CP.Cantidad,
            TP.nombre,
            (TP.precio - P.descuento) AS subtotal,
            P.descuento, 
            TP.codigoBarras
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
                (TP.nombre = '{input}'
                OR TP.codigoBarras = '{input}');
    """
    )


def read_current_sale_id():
    return du.exec_query("SELECT MAX(id) FROM Compras")[0][0]


def read_registro():
    data = du.exec_query("SELECT * FROM Registro")
    print(f"Registro de datos:\n{data}")


def read_errores():
    data = du.exec_query("SELECT * FROM Errores")
    print("\ndatos: ")
    print(data)
