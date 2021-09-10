import pytest
import draft0
import sqlite3
from tkinter import messagebox


def tes(cursor):
    # conn = sqlite3.connect('registrations.db')
    # c = conn.cursor()
    cursor.execute("select id from register")
    rec = cursor.fetchall()
    assert len(rec) == 0
#     print(rec)
#     # x = var.get()
#     # y = var1.get()
#     db_username = [record[2] for record in rec]
#     db_password = [record[3] for record in rec]
#     # if x in dat and y in dat1:
#     #     messagebox.showinfo("login", "Correct username and password")
#     # elif x != dat and y != dat1:
#     #     messagebox.showerror("Error", "Username and Password invalid")
#
#     if username in db_username and password in db_password:
#         messagebox.showinfo("login", 'Correct username and password')
#         return True
#     else:
#         messagebox.showinfo("Error", 'Invalid username and password')
#         return False
#
#     # Clear the text boxes
#     # f.delete(0, END)
#     # l.delete(0, END)
#
#
# assert tes('oopsie', '30090')
# # assert tes('invalid_username', 'valid_password')
# # assert tes('Hi', '1234')
# # assert tes('invalid_username', 'invalid_password')




