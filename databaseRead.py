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
    data = execQuery('SELECT nombre, precio, ganancia, codigoBarras FROM TiposProducto')
    # print(data)
    retData = []
    for row in data:
        newRow = (row[0], row[1], str(row[2]) +
                  "%", row[1] * row[2]/100, row[3])
        # print(newRow)
        retData.append(newRow)
    # c.execute('SELECT * FROM Productos')
    # data = c.fetchall()
    # print(data)
    # for row in data:
    #     print(row)
    return retData

def readTiposProductoN(nombre):
    data = execQuery("SELECT nombre, precio, ganancia, codigoBarras FROM TiposProducto WHERE nombre='" + nombre + "'")
    retData = []
    for row in data:
        newRow = (row[0], row[1], str(row[2]) +
                  "%", row[1] * row[2]/100, row[3])
        # print(newRow)
        retData.append(newRow)
    return retData

def readProductos():
    data = execQuery('SELECT ')

def readErrores():
    data = execQuery('SELECT * FROM Errores')
    print("\ndatos: ")
    print(data)


# readDB()
