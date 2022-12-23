import sqlite3
import windows

db = 'Pet-shop.db'

def insertTipoProducto():
    try:
        # Making a connection between sqlite3 database and Python Program
        connection = sqlite3.connect(db)
        # If sqlite3 makes a connection with python program then it will print "Connected to SQLite"
        # Otherwise it will show errors
        print("Connected to SQLite")
        c = connection.cursor()

        lista = windows.newTipoProducto()
        print("NOMBRE: " + lista['nombre'])

        # insert = "INSERT INTO TiposProducto (nombre, precio, ganancia, codigoBarras) VALUES (?, ?, ?, ?)",
        # (lista['nombre'], lista['precio'], lista['ganancia'], lista['codigoBarras'])

        c.execute("INSERT INTO TiposProducto (nombre, precio, ganancia, codigoBarras) VALUES (?, ?, ?, ?)",
        (lista['nombre'], lista['precio'] + lista['ganancia']/100, lista['ganancia'], lista['codigoBarras']))
        print("Table ready")
    except sqlite3.Error as error:
        print("Failed to connect with sqlite3 database", error)
    finally:
        # Inside Finally Block, If connection is open, we need to close it
        if connection:

            connection.commit()
            c.close()
            # using close() method, we will close the connection
            connection.close()
            # After closing connection object, we will print "the sqlite connection is closed"
            print("the sqlite connection is closed")