import databaseUtil as du


def remove_tipo_producto(input):
    query_str = """DELETE FROM TiposProducto WHERE
    nombre = '""" + input + "' OR codigoBarras = '" + input + "'"
    if du.exec_query(query_str) != None:
        du.popup_message("Producto eliminado exitosamente")
    else:
        du.popup_message("Producto no se pudo eliminar. Posiblemente por un error en la conexion con la base de datos.")
