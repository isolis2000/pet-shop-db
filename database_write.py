import sqlite3


def create_all():
    try:
        connection = sqlite3.connect("Pet-shop.db")
        cursor = connection.cursor()
        create_proveedores(cursor)
        create_tipos_producto(cursor)
        create_productos(cursor)
        create_clientes(cursor)
        insert_clientes(cursor)
        create_razas(cursor)
        create_clientes_peluqueria(cursor)
        create_tipos_pago(cursor)
        insert_tipos_pago(cursor)
        create_compras(cursor)
        create_compras_productos(cursor)
        create_registro(cursor)
        create_errores(cursor)
    except sqlite3.Error as error:
        print("Failed to connect with sqlite3 database", error)
    finally:
        if connection:
            connection.commit()
            cursor.close()
            connection.close()
            print("the sqlite connection is closed")


def create_proveedores(cursor):
    cursor.execute("DROP TABLE IF EXISTS Proveedores")

    command = """ CREATE TABLE Proveedores (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL UNIQUE,
                    telefono INTEGER
    ); """

    cursor.execute(command)
    print("Table Proveedores successfully created")


def create_tipos_producto(cursor):
    cursor.execute("DROP TABLE IF EXISTS TiposProducto")

    command = """ CREATE TABLE TiposProducto (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL UNIQUE,
                    precio REAL NOT NULL,
                    ganancia REAL NOT NULL,
                    codigoBarras char(9),
                    idProveedor INTEGER,
                    FOREIGN KEY (idProveedor) REFERENCES Proveedores(id)
    ); """

    cursor.execute(command)
    print("Table TiposProducto successfully created")


def create_productos(cursor):
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


def create_clientes(cursor):  # datos por definir
    cursor.execute("DROP TABLE IF EXISTS Clientes")

    command = """ CREATE TABLE Clientes (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    telefono TEXT
    ); """

    cursor.execute(command)
    print("Table Clientes successfully created")


def insert_clientes(cursor):
    cursor.execute("INSERT INTO Clientes (id, nombre) VALUES (0, 'Sin definir')")
    print("Client 'Sin definir' created")


def create_razas(cursor):
    cursor.execute("DROP TABLE IF EXISTS Razas")

    command = """ CREATE TABLE Razas (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL
    ); """

    cursor.execute(command)
    print("Table Razas successfully created")


def create_clientes_peluqueria(cursor):  # datos por definir
    cursor.execute("DROP TABLE IF EXISTS MascotasPeluqueria")

    command = """ CREATE TABLE MascotasPeluqueria (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    notasAdicionales TEXT,
                    monto INTEGER NOT NULL,
                    idRaza INTEGER,
                    idCliente INTEGER,
                    FOREIGN KEY (idRaza) REFERENCES Razas(id),
                    FOREIGN KEY (idCliente) REFERENCES Clientes(id)
    ); """

    cursor.execute(command)
    print("Table MascotasPeluqueria successfully created")


def create_tipos_pago(cursor):
    cursor.execute("DROP TABLE IF EXISTS TiposPago")

    command = """ CREATE TABLE TiposPago (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL
    ); """

    cursor.execute(command)

    print("Table TiposPago successfully created")


def insert_tipos_pago(cursor):
    payment_types = ["Otro", "Efectivo", "SINPE", "Tarjeta"]

    for payment in payment_types:
        command = f"""
            INSERT INTO TiposPago (nombre)
            VALUES ('{payment}')
        """
        print(command)
        cursor.execute(command)
        print(f"payment {payment} added")


def create_compras(cursor):
    cursor.execute("DROP TABLE IF EXISTS Compras")

    command = """ CREATE TABLE Compras (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    fecha TEXT NOT NULL,
                    estado TEXT NOT NULL,
                    totalAPagar REAL NOT NULL,
                    vuelto REAL NOT NULL,
                    idTipoPago INTEGER NOT NULL,
                    idCliente INTEGER NOT NULL,
                    FOREIGN KEY (idTipoPago) REFERENCES TiposPago(id),
                    FOREIGN KEY (idCliente) REFERENCES Clientes(id)
    ); """  # resultados: En Progreso, Exitosa, Cancelada

    cursor.execute(command)
    print("Table Compras successfully created")


def create_compras_productos(cursor):
    cursor.execute("DROP TABLE IF EXISTS Compras_Productos")

    command = """ CREATE TABLE Compras_Productos (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    idCompra INTEGER NOT NULL,
                    idProducto INTEGER NOT NULL,
                    cantidad INTEGER NOT NULL,
                    UNIQUE(idCompra, idProducto)
                    FOREIGN KEY (idCompra) REFERENCES Productos(id),
                    FOREIGN KEY (idProducto) REFERENCES Compras(id)
    ); """

    cursor.execute(command)
    print("Table Compras_Productos successfully created")


def create_registro(cursor):
    cursor.execute("DROP TABLE IF EXISTS Registro")

    command = """ CREATE TABLE Registro (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    fecha TEXT NOT NULL,
                    mensaje TEXT NOT NULL
    ); """

    cursor.execute(command)
    print("Table Registro successfully created")


def create_errores(cursor):
    cursor.execute("DROP TABLE IF EXISTS Errores")

    command = """ CREATE TABLE Errores (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    fecha TEXT NOT NULL,
                    mensaje TEXT NOT NULL
    ); """

    cursor.execute(command)
    print("Table Errores successfully created")


create_all()
