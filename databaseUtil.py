import sqlite3
import PySimpleGUI as sg
from datetime import datetime


dbName = 'Pet-shop.db'


def exec_query(s: str):
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


def insert_registro(message: str):
    query_str = ("""
    INSERT INTO Registro (
        fecha,
        mensaje)
    VALUES ('""" +
                datetime.today().strftime('%Y-%m-%d') + "', '" +
                message + "')")
    print(query_str)
    exec_query(query_str)


def verify_dict(dictionary: dict):
    for key in dictionary:
        if dictionary[key] == None:
            return False
    return True


def popup_message(message: str):
    sg.popup(message)

def popup_input(message: str) -> str:
    return sg.popup_get_text(message, default_text="1", size=(len(message)+1))
