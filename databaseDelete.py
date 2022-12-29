import databaseUtil as du


def removeTipoProducto(input):
    queryStr = """DELETE FROM TiposProducto WHERE
    nombre = '""" + input + "' OR codigoBarras = '" + input + "'"
    if du.execQuery(queryStr) != None:
        du.popupMessage("Producto eliminado exitosamente")
    else:
        du.popupMessage("Producto no se pudo eliminar. Posiblemente por un error en la conexion con la base de datos.")
