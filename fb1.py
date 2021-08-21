from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import sqlite3

# creating a window
root = Tk()
root.title("Facebook Video Downloader")
root.iconbitmap("fb1.ico")
root.attributes('-alpha', 0.9)

# setting the maximun and minimum size of the window
root.maxsize(width=500, height=450)
root.minsize(width=500, height=450)

# Create a databases or connect to one
conn = sqlite3.connect('infor.db')
# Create cursor
c = conn.cursor()

# creating a table
'''
c.execute(""" CREATE TABLE info(
      Firstname text,
      Lastname text,
      Username text,
      Email text,
      Link text

) """)
print("Table created")
'''


# creating insert function for databases
def submit():
    conn = sqlite3.connect("infor.db")
    c = conn.cursor()
    c.execute("INSERT INTO info VALUES (:first, :last, :user, :email, :link)", {
        'first': f.get(),
        'last': l.get(),
        'user': u.get(),
        'email': ei.get(),
        'link': vl.get()
    })
    messagebox.showinfo("Login Info", "INSERTED SUCCESSFULLY")
    conn.commit()
    conn.close()
    # clear the text boxes
    f.delete(0, END)
    l.delete(0, END)
    u.delete(0, END)
    ei.delete(0, END)
    vl.delete(0, END)


# creating query function for database
def query():
    conn = sqlite3.connect('infor.db')
    c = conn.cursor()
    c.execute("SELECT *, oid FROM info")
    rec = c.fetchall()
    print(rec)
    top = Toplevel()
    top.title("Records")
    # loop through the results
    print_rec = ""
    for record in rec:
        print_rec += str(record[2]) + ' ' + str(record[4]) + ' ' + '\t' + str(record[5]) + "\n"
    query_label = Label(top, text=print_rec)
    query_label.pack()
    Button(top, text="Close", command=top.destroy).pack()
    conn.commit()
    conn.close()


# ccreating delete function
def delete():
    conn = sqlite3.connect('infor.db')
    c = conn.cursor()
    c.execute("DELETE from info WHERE oid =" + dlt.get())
    print("DELETED SUCCESSFULLY")
    c.execute("SELECT *, oid FROM info")
    rec = c.fetchall()
    top1 = Toplevel()
    top1.title("New records")
    # lopp through the results
    print_rec = ""
    for record in rec:
        print_rec += str(record[2]) + ' ' + str(record[4]) + ' ' + '\t' + str(record[5]) + "\n"
    qur_label = Label(top1, text=print_rec)
    qur_label.pack()
    Button(top1, text="Close", command=top1.destroy).pack()
    conn.commit()
    conn.close()


# creating an update function
def update():
    conn = sqlite3.connect('infor.db')
    c = conn.cursor()
    record_id = dlt.get()
    c.execute(""" UPDATE info SET
         Firstname = :fname,
         Lastname = :lname,
         Username = :uname,
         Email = :email,
         Link = :link
         WHERE oid = :oid""",
              {'fname': f_editor.get(),
               'lname': l_editor.get(),
               'uname': u_editor.get(),
               'email': ei_editor.get(),
               'link': vl_editor.get(),
               'oid': record_id
               }
              )
    conn.commit()
    conn.close()
    # Destroying all the data and closing window
    editor.destroy()


def edit():
    global editor
    editor = Toplevel()
    editor.title("Update Info")
    editor.maxsize(width=500, height=300)
    editor.minsize(width=500, height=300)
    # connecting the database
    conn = sqlite3.connect('infor.db')
    # create cursor
    c = conn.cursor()
    record_id = dlt.get()
    c.execute("SELECT * FROM info WHERE oid=" + record_id)
    rec = c.fetchall()

    # creating global variable for all text boxes
    global f_editor
    global l_editor
    global u_editor
    global ei_editor
    global vl_editor

    label_1 = Label(editor, text="Update", bg="crimson", fg="black", width=29, font=("Comic Sans MS", 20))
    label_1.place(x=14, y=20)

    # creating textboxes
    f_editor = Entry(editor, width=40, font=("Comic Sans MS", 10))
    f_editor.place(x=120, y=95)
    l_editor = Entry(editor, width=40, font=("Comic Sans MS", 10))
    l_editor.place(x=120, y=125)
    u_editor = Entry(editor, width=40, font=("Comic Sans MS", 10))
    u_editor.place(x=120, y=155)
    ei_editor = Entry(editor, width=40, font=("Comic Sans MS", 10))
    ei_editor.place(x=120, y=185)
    vl_editor = Entry(editor, width=40, font=("Comic Sans MS", 10))
    vl_editor.place(x=120, y=215)

    # creating textbox labels
    f_lab = Label(editor, text="First name :", font=("Comic Sans MS", 11, "bold"))
    f_lab.place(x=10, y=90)
    l_lab = Label(editor, text="Last name :", font=("Comic Sans MS", 11, "bold"))
    l_lab.place(x=10, y=120)
    u_lab = Label(editor, text="User name :", font=("Comic Sans MS", 11, "bold"))
    u_lab.place(x=10, y=150)
    ei_lab = Label(editor, text="Email ID :", font=("Comic Sans MS", 11, "bold"))
    ei_lab.place(x=10, y=180)
    vl_lab = Label(editor, text="Video Link :", font=("Comic Sans MS", 11, "bold"))
    vl_lab.place(x=10, y=210)

    for record in rec:
        f_editor.insert(0, record[0])
        l_editor.insert(0, record[1])
        u_editor.insert(0, record[2])
        ei_editor.insert(0, record[3])
        vl_editor.insert(0, record[4])

    edit_btn = Button(editor, text="SAVE", font=("Comic Sans MS", 10,"bold"), width=59, command=update)
    edit_btn.place(x=10, y=245)

    conn.commit()
    conn.close()


label_0 = Label(root, text="Login System", bg="crimson", fg="black", width=29, font=("Comic Sans MS", 20))
label_0.place(x=14, y=20)

# create text boxes
f = Entry(root, width=40, font=("Comic Sans MS", 10))
f.place(x=120, y=95)
l = Entry(root, width=40, font=("Comic Sans MS", 10))
l.place(x=120, y=125)
u = Entry(root, width=40, font=("Comic Sans MS", 10))
u.place(x=120, y=155)
ei = Entry(root, width=40, font=("Comic Sans MS", 10))
ei.place(x=120, y=185)
vl = Entry(root, width=40, font=("Comic Sans MS", 10))
vl.place(x=120, y=215)
# creating a delete box
dlt = Entry(root, width=40, font=("Comic Sans MS", 10))
dlt.place(x=120, y=318)

# creating labels
f_lab = Label(root, text="First name :", font=("Comic Sans MS", 11, "bold"))
f_lab.place(x=10, y=90)
l_lab = Label(root, text="Last name :", font=("Comic Sans MS", 11, "bold"))
l_lab.place(x=10, y=120)
u_lab = Label(root, text="User name :", font=("Comic Sans MS", 11, "bold"))
u_lab.place(x=10, y=150)
ei_lab = Label(root, text="Email ID :", font=("Comic Sans MS", 11, "bold"))
ei_lab.place(x=10, y=180)
vl_lab = Label(root, text="Video Link :", font=("Comic Sans MS", 11, "bold"))
vl_lab.place(x=10, y=210)
dlt_lab = Label(root, text="Delete ID :", font=("Comic Sans MS", 11, "bold"))
dlt_lab.place(x=10, y=313)

# creating add button
add_btn = Button(root, text="Add info", font=("Comic Sans MS", 10,"bold"), width=59, command=submit)
add_btn.place(x=10, y=245)
# creating query button
query_btn = Button(root, text="Show info", font=("Comic Sans MS", 10,"bold"), width=59, command=query)
query_btn.place(x=10, y=278)
# creating delete button
dlt_btn = Button(root, text="Delete", font=("Comic Sans MS", 10,"bold"), width=59, command=delete)
dlt_btn.place(x=10, y=348)
# creating update button
upd_btn = Button(root, text="Update", font=("Comic Sans MS", 10,"bold"), width=59, command=edit)
upd_btn.place(x=10, y=381)
# commit change
conn.commit()
# close connection
conn.close()
root.mainloop()
