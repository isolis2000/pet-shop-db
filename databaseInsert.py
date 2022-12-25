import sqlite3
import windowsAdd as wa
import util

db = 'Pet-shop.db'

def insertTipoProducto():
    try:
        connection = sqlite3.connect(db)
        print("Connected to SQLite")
        c = connection.cursor()

        dictTipos = wa.newTipoProducto()
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
