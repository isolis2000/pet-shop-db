import sqlite3
import PySimpleGUI as sg
from datetime import datetime


db_name = "Pet-shop.db"
iva = 0.13  # 13%


def get_today_date(inverted=False):
    if inverted:
        return datetime.today().strftime("%d-%m-%Y")
    else:
        return datetime.today().strftime("%Y-%m-%d")


def exec_query(s: str):
    data = None
    try:
        connection = sqlite3.connect(db_name)
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
    query_str = f"""
    INSERT INTO Registro (
        fecha,
        mensaje)
    VALUES (
        '{get_today_date()}',
        '{message}'
        )
    """
    exec_query(query_str)


def verify_dict(dictionary: dict):
    for key in dictionary:
        if dictionary[key] is None:
            return False
    return True


def popup_message(message: str, duration_seconds=1):
    if duration_seconds == 0:
        sg.popup(
            message,
            title="",
            auto_close=False,
            no_titlebar=False,
            button_type=sg.POPUP_BUTTONS_NO_BUTTONS,
            any_key_closes=True,
            font="Courier 14",
            grab_anywhere=True,
        )
    else:
        sg.popup(
            message,
            title="",
            auto_close=True,
            auto_close_duration=duration_seconds,
            no_titlebar=True,
            button_type=sg.POPUP_BUTTONS_NO_BUTTONS,
            any_key_closes=True,
            font="Courier 14",
            grab_anywhere=True,
        )


def popup_input(message: str) -> str:
    return sg.popup_get_text(message, size=(len(message) + 1), no_titlebar=True)


def confirmation_popup(message: str) -> bool:
    ans_str = sg.popup(message, custom_text=("Si", "No"), no_titlebar=True)
    if ans_str == "Si":
        return True
    elif ans_str == "No" or ans_str is None:
        return False
