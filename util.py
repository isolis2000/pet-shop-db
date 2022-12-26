from PySimpleGUI import popup

def verifyDict(dictionary):
    for key in dictionary:
        if dictionary[key] == None:
            return False
    return True

def popupMessage(message):
    popup(message)