import database_util as du
import re

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


def read_tipos_producto(user_input=""):
    if user_input == "":
        return du.exec_query(
            """
            SELECT 
                TP.nombre, 
                round(TP.precio, 2), 
                TP.ganancia, 
                TP.codigoBarras,
                P.nombre
            FROM 
                TiposProducto AS TP
                INNER JOIN Proveedores AS P ON P.id = TP.idProveedor
            """
        )
    else:
        return du.exec_query(
            f"""
            SELECT 
                TP.nombre, 
                round(TP.precio, 2), 
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


def find_tipo_producto_id(user_input: str):
    data = du.exec_query(
        f"""
        SELECT 
            id 
        FROM 
            TiposProducto 
        WHERE 
            codigoBarras='{user_input}'
            OR nombre='{user_input}'"""
    )
    return data[0][0]


def find_product_type_bar_code(prod_name: str):
    data = du.exec_query(
        f"""
        SELECT
            codigoBarras
        FROM 
            TiposProducto
        WHERE
            nombre='{prod_name}'
        """
    )
    return data[0][0]


def read_productos(user_input=""):
    print(f"input_type: {type(user_input)}")
    if user_input == "":
        return du.exec_query(
            """
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
        """
        )
    else:
        return du.exec_query(
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
                OR P.id = '{user_input}'
            """
        )


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


# def read_product_id(user_input: str):
#     data = du.exec_query(
#         f"""
#         SELECT
#             id
#         """
#     )


def read_past_receipts(receipt_num=""):
    if receipt_num == "":
        return du.exec_query(
            """
        SELECT  
            C.id,
            C.fecha,
            CL.nombre,
            round(C.totalAPagar, 2),
            TP.nombre,
            C.estado
        FROM 
            Compras AS C
        INNER JOIN 
            Clientes AS CL ON (CL.id = C.idCliente)
        INNER JOIN
            TiposPago AS TP ON (TP.id = C.idTipoPago)
        ORDER BY C.fecha ASC
        """
        )
    else:
        return du.exec_query(
            f"""
            SELECT  
                C.id,
                C.fecha,
                CL.nombre,
                round(C.totalAPagar, 2),
                TP.nombre
            FROM 
                Compras AS C
            INNER JOIN 
                Clientes AS CL ON (CL.id = C.idCliente)
            INNER JOIN
                TiposPago AS TP ON (TP.id = C.idTipoPago)
            WHERE   
                C.id = {receipt_num};
            """
        )


def read_current_order(user_input=""):
    if user_input == "":
        return du.exec_query(
            """
            SELECT  
                CP.Cantidad,
                TP.nombre,
                round((TP.precio - P.descuento) * CP.Cantidad,2) AS subtotal,
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
    else:
        return du.exec_query(
            f"""
            SELECT  
                CP.Cantidad,
                TP.nombre,
                round((TP.precio - P.descuento), 2) AS subtotal,
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


def read_clients(client_name=""):
    if client_name == "":
        return du.exec_query(
            f"""
            SELECT
                nombre,
                CASE
                    WHEN telefono IS NULL
                        THEN 'Sin numero'
                END
            FROM 
                Clientes
            """
        )
    else:
        return du.exec_query(
            f"""
            SELECT
                nombre,
                telefono
            CASE
                WHEN telefono is NULL
                THEN telefono = 'Sin numero'
                END
            FROM 
                Clientes AS C
            WHERE
                C.nombre = '{client_name}'
            """
        )


def read_client_names(name=""):
    query_res = []
    if name == "":
        query_res = du.exec_query(
            """
            SELECT
                nombre
            FROM 
                Clientes
            """
        )
    else:
        query_res = du.exec_query(
            f"""
            SELECT
                nombre
            FROM 
                Clientes
            WHERE
                nombre = '{name}'
            """
        )
    ret_list = []
    for item in query_res:
        ret_list.append(item[0])
    return ret_list


def read_payment_types():
    query_res = du.exec_query(
        f"""
        SELECT
            nombre
        FROM
            TiposPago
        """
    )
    ret_list = []
    for item in query_res:
        ret_list.append(item[0])
    return ret_list


def read_mascotas(pet_name=""):
    if pet_name == "":
        return du.exec_query(
            f"""
            SELECT 
                M.nombre,
                C.nombre,
                R.nombre,
                M.notasAdicionales,
                round(M.monto, 2)
            FROM
                Mascotaspeluqueria AS M
            INNER JOIN 
                Clientes AS C ON M.idCliente = C.id
            INNER JOIN 
                Razas AS R ON M.idRaza = R.id
            """
        )
    else:
        return du.exec_query(
            f"""
        SELECT 
            M.nombre,
            C.nombre,
            R.nombre,
            M.notasAdicionales,
            round(M.monto, 2)
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


def find_payment_type_id(payment_name: str):
    query_res = du.exec_query(
        f"""
        SELECT
            id
        FROM
            TiposPago
        WHERE 
            nombre = '{payment_name}'
        """
    )
    return query_res[0][0]


def find_client_id(client_name: str):
    query_res = du.exec_query(
        f"""
        SELECT
            id
        FROM
            Clientes
        WHERE 
            nombre = '{client_name}'
        """
    )
    return query_res[0][0]


def closing_time() -> list:
    query_res = du.exec_query(
        f"""
        SELECT 
            SUM(C.totalAPagar) AS Pago,
            TP.nombre AS TipoPago
        FROM
            Compras AS C
        INNER JOIN 
            TiposPago AS TP ON (TP.id = C.idTipoPago)
        WHERE
            C.fecha = '{du.get_today_date()}'
         GROUP BY 
            TP.nombre
        """
    )
    ret_str = "Hoy se vendió:\n"
    for res in query_res:
        ret_str += f"₡{res[0]} en {res[1]}\n"
    du.popup_message(ret_str, 0)


def read_registro():
    data = du.exec_query("SELECT * FROM Registro")
    print(f"Registro de datos:\n{data}")


def read_errores():
    data = du.exec_query("SELECT * FROM Errores")
    print("\ndatos: ")
    print(data)
