import windowsEdit as we
import databaseRead as dr
import databaseUtil as du


def editTipoProducto(dataSelected):

    id = dr.findTipoProductoId(dataSelected[4])
    dictTipos = we.editTipoProducto(dataSelected)

    if dictTipos == 'Cancel':
        du.popupMessage("Operacion cancelada")
    elif du.verifyDict(dictTipos):
        print(dictTipos)
        print("NOMBRE: " + dictTipos['nombre'])

        # insert = "INSERT INTO TiposProducto (nombre, precio, ganancia, codigoBarras) VALUES (?, ?, ?, ?)",
        # (dictTipos['nombre'], dictTipos['precio'], dictTipos['ganancia'], dictTipos['codigoBarras'])

        strExec = ("UPDATE TiposProducto SET " +
                    "nombre = '" + dictTipos['nombre'] + "', "
                    "precio = " + str(float(dictTipos['precio']) + float(
                        dictTipos['precio']) * float(dictTipos['ganancia'])/100) + ", "
                    "ganancia = " +
                    str(float(dictTipos['precio']) *
                        float(dictTipos['ganancia'])/100) + ", "
                    "codigoBarras = '" + dictTipos['codigoBarras'] + "' "
                    "WHERE id = " + str(id))
        print(strExec)

        if du.execQuery(strExec) != None:
            du.popupMessage("Producto editado exitosamente")
        else:
            du.popupMessage("Producto no se pudo editar correctamente. Favor verifique conexion con la base de datos.")
    else:
        du.popupMessage(
            "Datos ingresados de manera incorrecta, favor verifique que todas las casillas esten llenas con lo que se pide")
