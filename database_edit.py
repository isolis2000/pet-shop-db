import gui_edit as we
import database_read as dr
import database_util as du
import printing as pr


def edit_tipo_producto(data_selected):

    print(f"data_selected: {data_selected}")
    id_producto = dr.find_tipo_producto_id(data_selected[4])
    data_product = dr.read_tipos_producto(data_selected[4])
    dict_tipos = we.edit_tipo_producto(data_product[0], du.iva)

    if dict_tipos == "Cancel":
        du.popup_message("Operación cancelada")
    elif du.verify_dict(dict_tipos):
        print(dict_tipos)
        print("NOMBRE: " + dict_tipos["nombre"])

        # insert = "INSERT INTO TiposProducto (nombre, precio, ganancia, codigoBarras) VALUES (?, ?, ?, ?)",
        # (dict_tipos['nombre'], dict_tipos['precio'], dict_tipos['ganancia'], dict_tipos['codigoBarras'])

        str_exec = f"""
            UPDATE TiposProducto 
                SET nombre = '{dict_tipos["nombre"]}',
                    precio = {float(dict_tipos["precio"]) 
                                + float(dict_tipos["precio"]) 
                                * float(dict_tipos["ganancia"])/100
                              }, 
                    ganancia = {float(dict_tipos["precio"]) 
                                * float(dict_tipos["ganancia"])/100
                                },
                    codigoBarras = '{dict_tipos["codigoBarras"]}'
                WHERE 
                    id = {id_producto}
            """

        print(str_exec)

        if du.exec_query(str_exec) != None:
            du.popup_message("Producto editado exitosamente")
        else:
            du.popup_message(
                "Producto no se pudo editar correctamente. Favor verifique conexion con la base de datos."
            )
    else:
        du.popup_message(
            "Datos ingresados de manera incorrecta, favor verifique que todas las casillas esten llenas con lo que se pide"
        )


def update_inventory_after_sale():
    sale_lst = dr.read_current_order()
    print(f"sale lst: {sale_lst}")
    for prod in sale_lst:
        str_exec = f"""
        UPDATE Productos
            SET cantidad = cantidad - {prod[0]}
            WHERE id = {prod[6]}
        """
        print(f"exec: {str_exec}")
        du.exec_query(str_exec)


def edit_sale_prod_quantity(prod_id: int):
    product = dr.read_productos(prod_id)[0]
    product_quantity = int(product[4])
    new_value = int(du.popup_input("Escriba la nueva cantidad de este producto"))
    if new_value <= product_quantity:
        str_exec = f"""
        UPDATE Compras_Productos
            SET cantidad = {new_value}
            WHERE id = {prod_id}
        """
        du.exec_query(str_exec)
    else:
        du.popup_message("Cantidad del producto excede la cantidad en inventario")


def finalizar_compra() -> bool:
    curr_sale = dr.read_current_order()
    payments_list = dr.read_payment_types()
    clients_list = dr.read_client_names()
    print(f"lists: {payments_list}, {clients_list}")

    keys_list = ["cantidad", "descripcion", "subtotal", "descuento"]
    res_lst = []
    for curr_item in curr_sale:
        res_lst.append({keys_list[i]: curr_item[i] for i in range(0, len(keys_list))})

    final_price = 0.0
    for item in res_lst:
        final_price += item["subtotal"] * (1 - item["descuento"] / 100)

    answers = we.popup_finalize_sale(payments_list, clients_list, final_price)
    if answers == None:
        du.popup_message("Operacion cancelada")
        return False

    print(f"payment: {answers}")
    payment_type = answers[0]
    client = answers[1]

    print(f"final_price: {final_price}")
    confirmation_text = ""
    if len(answers) == 3:
        payment = abs(float(answers[2]))
        change = 0
        if payment != 0:
            change = payment - final_price

        if change < 0:
            du.popup_message(f"Hace falta ₡{abs(change)}, favor intente de nuevo")
            return False
        elif change == 0:
            confirmation_text = "¿Seguro que desea finalizar la compra?"
        else:
            change_txt = f"El vuelto es {change}"
            confirmation_text = f"""{change_txt:^40},
            {'¿Seguro que desea finalizar la compra?':^40}"""

    if du.confirmation_popup(confirmation_text):

        print(f"payment: {payment_type}, client: {client}")

        update_inventory_after_sale()

        pr.generate_receipt(
            curr_sale[0][6], client, res_lst, du.get_today_date(True), final_price
        )

        order_id = dr.read_current_sale_id()
        change = 0
        client_id = dr.find_client_id(client)
        payment_type_id = dr.find_payment_type_id(payment_type)

        str_exec = f"""
        UPDATE Compras
            SET 
                estado = 'Finalizada',
                totalAPagar = {final_price},
                vuelto = {change},
                idTipoPago = {payment_type_id},
                idCliente = {client_id}
            WHERE id = {order_id}
        """
        print(str_exec)
        du.exec_query(str_exec)
        return True
    else:
        return False
