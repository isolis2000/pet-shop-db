import sqlite3

def createAll():
    try:
        connection = sqlite3.connect('Pet-shop.db')
        cursor = connection.cursor()
        createTiposProducto(cursor)
        createProductos(cursor)
        createClientes(cursor)
        createCompras(cursor)
        createCompras_Productos(cursor)
        createRegistro(cursor)
        createErrores(cursor)
    except sqlite3.Error as error:
        print("Failed to connect with sqlite3 database", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("the sqlite connection is closed")

def createProveedores(cursor):
    cursor.execute("DROP TABLE IF EXISTS Proveedores")

    command = """ CREATE TABLE Proveedores (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL UNIQUE,
                    telefono INTEGER
    ); """

    cursor.execute(command)
    print("Table Proveedores successfully created")

def createTiposProducto(cursor):
    cursor.execute("DROP TABLE IF EXISTS TiposProducto")

    command = """ CREATE TABLE TiposProducto (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL UNIQUE,
                    precio REAL NOT NULL,
                    ganancia REAL NOT NULL,
                    codigoBarras char(13) NOT NULL UNIQUE,
                    idProveedor INTEGER,
                    FOREIGN KEY (idProveedor) REFERENCES Proveedores(id)
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

def createClientes(cursor):
    cursor.execute("DROP TABLE IF EXISTS Clientes")

    command = """ CREATE TABLE Clientes (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    apellido1 TEXT,
                    apellido2 TEXT,
                    telefono TEXT
    ); """

    cursor.execute(command)
    print("Table Clientes successfully created")

def createCompras(cursor):
    cursor.execute("DROP TABLE IF EXISTS Compras")

    command = """ CREATE TABLE Compras (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    fecha TEXT NOT NULL
    ); """

    cursor.execute(command)
    print("Table Compras successfully created")


def createCompras_Productos(cursor):
    cursor.execute("DROP TABLE IF EXISTS Compras_Productos")

    command = """ CREATE TABLE Compras_Productos (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    idCompra INTEGER NOT NULL,
                    idProducto INTEGER NOT NULL,
                    FOREIGN KEY (idCompra) REFERENCES Productos(id),
                    FOREIGN KEY (idProducto) REFERENCES Compras(id)
    ); """

    cursor.execute(command)
    print("Table Compras_Productos successfully created")

def createRegistro(cursor):
    cursor.execute("DROP TABLE IF EXISTS Registro")

    command = """ CREATE TABLE Registro (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    fecha TEXT NOT NULL,
                    mensaje TEXT NOT NULL
    ); """

    cursor.execute(command)
    print("Table Registro successfully created")


def createErrores(cursor):
    cursor.execute("DROP TABLE IF EXISTS Errores")

    command = """ CREATE TABLE Errores (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    fecha TEXT NOT NULL,
                    mensaje TEXT NOT NULL
    ); """

    cursor.execute(command)
    print("Table Errores successfully created")

createAll()
