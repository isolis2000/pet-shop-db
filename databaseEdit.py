import sqlite3
import windowsEdit as we
import util
import databaseRead as dr

db = 'Pet-shop.db'

# INSERTS


def insertTipoProducto():
    try:
        connection = sqlite3.connect(db)
        print("Connected to SQLite")
        c = connection.cursor()

        dictTipos = we.newTipoProducto()

        if dictTipos == 'Cancel':
            util.popupMessage("Operacion cancelada")
        elif util.verifyDict(dictTipos):
            print(dictTipos)
            print("NOMBRE: " + dictTipos['nombre'])

            # insert = "INSERT INTO TiposProducto (nombre, precio, ganancia, codigoBarras) VALUES (?, ?, ?, ?)",
            # (dictTipos['nombre'], dictTipos['precio'], dictTipos['ganancia'], dictTipos['codigoBarras'])

            c.execute("INSERT INTO TiposProducto (nombre, precio, ganancia, codigoBarras) VALUES (?, ?, ?, ?)",
                      (dictTipos['nombre'], str(float(dictTipos['precio']) + float(dictTipos['precio']) * float(dictTipos['ganancia'])/100),
                       str(float(dictTipos['precio']) * float(dictTipos['ganancia'])/100), dictTipos['codigoBarras']))
            print("Table ready")
        else:
            util.popupMessage(
                "Datos ingresados de manera incorrecta, favor verifique que todas las casillas esten llenas con lo que se pide")
    except sqlite3.Error as error:
        print("Failed to connect with sqlite3 database", error)
    finally:
        if connection:

            connection.commit()
            c.close()
            connection.close()
            print("the sqlite connection is closed")


def insertProducto():
    try:
        connection = sqlite3.connect(db)
        print("Connected to SQLite")
        c = connection.cursor()

        dictTipos = we.datab()
        if util.verifyDict(dictTipos):
            print(dictTipos)
            print("NOMBRE: " + dictTipos['nombre'])

            # insert = "INSERT INTO TiposProducto (nombre, precio, ganancia, codigoBarras) VALUES (?, ?, ?, ?)",
            # (dictTipos['nombre'], dictTipos['precio'], dictTipos['ganancia'], dictTipos['codigoBarras'])

            c.execute("INSERT INTO TiposProducto (nombre, precio, ganancia, codigoBarras) VALUES (?, ?, ?, ?)",
                      (dictTipos['nombre'], str(float(dictTipos['precio']) + float(dictTipos['precio']) * float(dictTipos['ganancia'])/100),
                       str(float(dictTipos['precio']) * float(dictTipos['ganancia'])/100), dictTipos['codigoBarras']))
            print("Table ready")
    except sqlite3.Error as error:
        print("Failed to connect with sqlite3 database", error)
    finally:
        if connection:

            connection.commit()
            c.close()
            connection.close()
            print("the sqlite connection is closed")

# EDITS


def editTipoProducto(dataSelected):
    try:
        connection = sqlite3.connect(db)
        print("Connected to SQLite")
        c = connection.cursor()

        id = dr.findTipoProductoId(dataSelected[4])
        dictTipos = we.editTipoProducto(dataSelected)

        if dictTipos == 'Cancel':
            util.popupMessage("Operacion cancelada")
        elif util.verifyDict(dictTipos):
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

            c.execute(strExec)
            print("Table ready")
        else:
            util.popupMessage(
                "Datos ingresados de manera incorrecta, favor verifique que todas las casillas esten llenas con lo que se pide")
    except sqlite3.Error as error:
        print("Failed to connect with sqlite3 database", error)
    finally:
        if connection:

            connection.commit()
            c.close()
            connection.close()
            print("the sqlite connection is closed")
