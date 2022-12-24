import sqlite3
import windowsAdd as wa

db = 'Pet-shop.db'

def removeTipoProducto(input):
    try:
        # Making a connection between sqlite3 database and Python Program
        connection = sqlite3.connect(db)
        # If sqlite3 makes a connection with python program then it will print "Connected to SQLite"
        # Otherwise it will show errors
        print("Connected to SQLite")
        c = connection.cursor()

        # insert = "INSERT INTO TiposProducto (nombre, precio, ganancia, codigoBarras) VALUES (?, ?, ?, ?)",
        # (lista['nombre'], lista['precio'], lista['ganancia'], lista['codigoBarras'])

        c.execute("DELETE FROM TiposProducto WHERE " + 
        "nombre = '" + input + 
        "' OR codigoBarras = '" + input + "'")
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