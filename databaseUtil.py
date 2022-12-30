import sqlite3
from PySimpleGUI import popup
from datetime import datetime


dbName = 'Pet-shop.db'


def execQuery(s: str):
    data = None
    try:
        connection = sqlite3.connect(dbName)
        c = connection.cursor()
        c.execute(s)
        data = c.fetchall()
    except sqlite3.Error as error:
        print("Failed to connect with sqlite3 database", error)
    finally:
        if connection:
            connection.commit()
            c.close()
            connection.close()
            print("the sqlite connection is closed")
            return data


def insertRegistro(message: str):
    queryStr = ("""
    INSERT INTO Registro (
        fecha,
        mensaje)
    VALUES ('""" +
                datetime.today().strftime('%Y-%m-%d') + "', '" +
                message + "')")
    print(queryStr)
    execQuery(queryStr)


def verifyDict(dictionary: dict):
    for key in dictionary:
        if dictionary[key] == None:
            return False
    return True


def popupMessage(message: str):
    popup(message)
