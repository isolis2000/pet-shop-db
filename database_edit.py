import gui_edit as we
import database_read as dr
import database_util as du
import printing as pr


def edit_tipo_producto(data_selected):

    print(f"data_selected: {data_selected}")
    id_producto = dr.find_tipo_producto_id(data_selected[4])
    data_product = dr.read_tipos_producto_n(data_selected[4])
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
    new_value = du.popup_input("Escriba la nueva cantidad de este producto")
    str_exec = f"""
    UPDATE Compras_Productos
        SET cantidad = {new_value}
        WHERE id = {prod_id}
    """
    du.exec_query(str_exec)


def finalizar_compra():

    curr_sale = dr.read_current_order()
    payments_list = dr.read_payment_types()
    clients_list = dr.read_client_names()
    print(f"lists: {payments_list}, {clients_list}")
    answers = we.popup_finalize_sale(payments_list, clients_list)
    if answers == None:
        du.popup_message("Operacion cancelada")
        return

    if du.confirmation_popup("¿Seguro que desea finalizar la compra?"):

        payment = answers["_PAYMENT_"]
        client = answers["_CLIENT_"]

        print(f"payment: {payment}, client: {client}")

        update_inventory_after_sale()

        keys_list = ["cantidad", "descripcion", "subtotal", "descuento"]
        res_lst = []
        for curr_item in curr_sale:
            res_lst.append(
                {keys_list[i]: curr_item[i] for i in range(0, len(keys_list))}
            )

        pr.generate_receipt(curr_sale[6], "Huu", res_lst, du.get_today_date(True))

        order_id = dr.read_current_sale_id()
        str_exec = f"""
        UPDATE Compras
            SET estado = 'Finalizada'
            WHERE id = {order_id}
        """
        du.exec_query(str_exec)
