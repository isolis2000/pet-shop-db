import windowsEdit as we
import databaseRead as dr
import databaseUtil as du


# --------------------------------------------- INSERTS ---------------------------------------------

def insertTipoProducto():

    dictTipos = we.newTipoProducto()

    if dictTipos == 'Cancel':
        du.popupMessage("Operacion cancelada")
    elif du.verifyDict(dictTipos):
        print(dictTipos)
        print("NOMBRE: " + dictTipos['nombre'])

        # insert = "INSERT INTO TiposProducto (nombre, precio, ganancia, codigoBarras) VALUES (?, ?, ?, ?)",
        # (dictTipos['nombre'], dictTipos['precio'], dictTipos['ganancia'], dictTipos['codigoBarras'])

        # queryStr = "INSERT INTO TiposProducto (nombre, precio, ganancia, codigoBarras) VALUES (?, ?, ?, ?)",
        #                 (dictTipos['nombre'], str(float(dictTipos['precio']) + float(dictTipos['precio']) * float(dictTipos['ganancia'])/100),
        #                  str(float(dictTipos['precio']) * float(dictTipos['ganancia'])/100), dictTipos['codigoBarras'])"
        queryStr = ("""
            INSERT INTO TiposProducto (
                nombre, 
                precio, 
                ganancia, 
                codigoBarras) 
            VALUES ('""" +
                dictTipos['nombre'] + "', " +
                str(float(dictTipos['precio']) + float(dictTipos['precio'])
                    * float(dictTipos['ganancia'])/100) + ", " +
                str(float(dictTipos['precio']) *
                    float(dictTipos['ganancia'])/100) + ", '" +
                dictTipos['codigoBarras'] + "')")
        print(queryStr)
        if du.execQuery(queryStr) != None:
            du.popupMessage("Producto insertado de manera exitosa")
        else:
            du.popupMessage("Producto no se pudo insertar")
    else:
        du.popupMessage(
            "Datos ingresados de manera incorrecta, favor verifique que todas las casillas esten llenas con lo que se pide")


def insertProducto():

    dictProduct = we.newProducto()
    print(dictProduct)
    if du.verifyDict(dictProduct):
        idTipoProducto = dr.findTipoProductoId(dictProduct['productCode'])
        if idTipoProducto != None:
            queryStr = ("""
                INSERT INTO Productos (
                    fechaCompra,
                    fechaVencimiento,
                    descuento,
                    cantidad,
                    idTipoProducto)
                VALUES ('""" +
                    dictProduct['buyDate'] + "', '" +
                    dictProduct['expirationDate'] + "', " +
                    dictProduct['discount'] + ", " +
                    dictProduct['ammount'] + ", " +
                    str(idTipoProducto) + ")")
            print(queryStr)
            if du.execQuery(queryStr) != None:
                du.popupMessage(
                    "Producto agregado al inventario de manera exitosa")
            else:
                du.popupMessage("Producto no se pudo agregar debido a un fallo en la base de datos")
        else:
            du.popupMessage(
                "Producto no se pudo agregar, favor verifique que exista este tipo de producto y que el codigo este correcto.")
    else:
        du.popupMessage("Datos ingresados de manera incorrecta, favor verifique que todas las casillas esten llenas con lo que se pide")
