from os import read
import sqlite3

database = 'Pet-shop.db'


def execQuery(s):
    connection = sqlite3.connect(database)
    c = connection.cursor()
    c.execute(s)
    data = c.fetchall()
    connection.close()
    return data


def readTiposProducto():
    data = execQuery("""
        SELECT 
            nombre, 
            precio, 
            ganancia, 
            codigoBarras 
        FROM 
            TiposProducto
        """)
    # print(data)
    retData = []
    for row in data:
        newRow = (row[0], round(row[1]), str(round((row[2]/(row[1]-row[2]))*100, 2)) +
                  "%", round(row[2], 2), row[3])
        # print(newRow)
        retData.append(newRow)
    # c.execute('SELECT * FROM Productos')
    # data = c.fetchall()
    # print(data)
    # for row in data:
    #     print(row)
    return retData


def readTiposProductoN(input: str):
    data = execQuery("""
    SELECT 
        nombre, 
        precio, 
        ganancia, 
        codigoBarras 
    FROM 
        TiposProducto 
    WHERE 
        nombre='""" + input + 
        "' OR codigoBarras='" + input + "'")
    retData = []
    for row in data:
        newRow = (row[0], round(row[1]), str(round((row[2]/(row[1]-row[2]))*100, 2)) +
                  "%", round(row[2], 2), row[3])
        # print(newRow)
        retData.append(newRow)
    return retData


def findTipoProductoId(codigoBarras: str):
    data = execQuery("""
    SELECT 
        id 
    FROM 
        TiposProducto 
    WHERE 
        codigoBarras='""" + codigoBarras + "'"
    )
    return data[0][0]


def readProductos():
    data = execQuery("""
        SELECT 
            TP.nombre, 
            P.fechaCompra, 
            P.fechaVencimiento, 
            P.descuento, 
            P.cantidad
        FROM 
            TiposProducto AS TP
            INNER JOIN Productos AS P ON TP.id = P.idTipoProducto
        """)
    # print(data)
    retData = []
    for row in data:
        newRow = (row[0], row[1], row[2], str(row[3])+"%" + row[4])
        # print(newRow)
        retData.append(newRow)
    return retData

def readProductosN(input: str):
    data = execQuery("""
        SELECT 
            TP.nombre, 
            P.fechaCompra, 
            P.fechaVencimiento, 
            P.descuento, 
            P.cantidad
        FROM 
            TiposProducto AS TP
            INNER JOIN Productos AS P ON TP.id = P.idTipoProducto
        WHERE
            TP.nombre = '""" + input + "'")
    # print(data)
    retData = []
    for row in data:
        newRow = (row[0], row[1], row[2], str(row[3])+"%" + row[4])
        # print(newRow)
        retData.append(newRow)
    return retData


def readErrores():
    data = execQuery('SELECT * FROM Errores')
    print("\ndatos: ")
    print(data)


# readDB()
