import WindowsEdit as we
import DatabaseRead as dr
import DatabaseUtil as du
import printing as pr
import datetime


def edit_tipo_producto(dataSelected):

    id = dr.find_tipo_producto_id(dataSelected[4])
    dict_tipos = we.edit_tipo_producto(dataSelected)

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
                    id = {id}
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


def edit_sale_prod_quantity(prod_id: int):
    new_value = du.popup_input("Escriba la nueva cantidad de este producto")
    str_exec = f"""
    UPDATE Compras_Productos
        SET cantidad = {new_value}
        WHERE id = {prod_id}
    """
    du.exec_query(str_exec)


def edit_estado_compra(str_state: str):
    if du.confirmation_popup("¿Seguro que desea finalizar la compra?"):

        curr_sale = dr.read_current_sale()
        keys_list = ["cantidad", "descripcion", "subtotal", "descuento"]
        res_lst = []
        for curr_item in curr_sale:
            res_lst.append(
                {keys_list[i]: curr_item[i] for i in range(0, len(keys_list))}
            )
        today = datetime.datetime.today().strftime("%Y-%m-%d")
        pr.generate_receipt(123, "Huu", res_lst, today)

        sell_id = dr.read_current_sale_id()
        str_exec = f"""
        UPDATE Compras
            SET estado = '{str_state}'
            WHERE id = {sell_id}
        """
        du.exec_query(str_exec)
