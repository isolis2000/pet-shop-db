import sqlite3

def createAll():
    try:
        connection = sqlite3.connect('Pet-shop.db')
        cursor = connection.cursor()
        createTiposProducto(cursor)
        createProductos(cursor)
        createBitacora(cursor)
        createErrores(cursor)
    except sqlite3.Error as error:
        print("Failed to connect with sqlite3 database", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("the sqlite connection is closed")

def createTiposProducto(cursor):
    cursor.execute("DROP TABLE IF EXISTS TiposProducto")

    command = """ CREATE TABLE TiposProducto (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    precio REAL NOT NULL,
                    ganancia REAL NOT NULL,
                    codigoBarras char(13) NOT NULL
    ); """

    cursor.execute(command)
    print("Table TiposProducto successfully created")


def createProductos(cursor):
    cursor.execute("DROP TABLE IF EXISTS Productos")

    command = """ CREATE TABLE Productos (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    fechaCompra NUMERIC NOT NULL,
                    fechaVencimiento NUMERIC NOT NULL,
                    descuento REAL NOT NULL,
                    cantidad INTEGER NOT NULL,
                    idTipoProducto char(13) NOT NULL,
                    FOREIGN KEY (idTipoProducto) REFERENCES TiposProducto(id)
    ); """

    cursor.execute(command)
    print("Table Productos successfully created")

def createBitacora(cursor):
    cursor.execute("DROP TABLE IF EXISTS Bitacora")

    command = """ CREATE TABLE Bitacora (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    fecha TEXT NOT NULL,
                    mensaje TEXT NOT NULL
    ); """

    cursor.execute(command)
    print("Table Bitacora successfully created")


def createErrores(cursor):
    cursor.execute("DROP TABLE IF EXISTS Errores")

    command = """ CREATE TABLE Errores (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    fecha TEXT NOT NULL,
                    mensaje TEXT NOT NULL
    ); """

    cursor.execute(command)
    print("Table Errores successfully created")


