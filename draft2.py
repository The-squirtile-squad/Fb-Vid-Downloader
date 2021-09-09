from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import sqlite3
from tkinter import filedialog
import requests
import re
from datetime import datetime
import os

# Window
h = Tk()
h.title("Facebook Video Downloader")
h.iconbitmap("fb1.ico")
# h.attributes('-alpha', 0.90)

# Setting the maximum and minimum size of the window
h.maxsize(width=500, height=280)
h.minsize(width=500, height=280)

# Adding image in the background
img = Image.open("fbwp2.jpg")
img = img.resize((950, 600), Image.ANTIALIAS)
photo = ImageTk.PhotoImage(img)
lab = Label(h, image=photo)
lab.pack()


# Login check system
def tes():
    conn = sqlite3.connect('registrations.db')
    c = conn.cursor()
    c.execute("SELECT *, oid FROM register")
    rec = c.fetchall()
    print(rec)
    x = var.get()
    y = var1.get()
    dat = [record[2] for record in rec]
    dat1 = [record[3] for record in rec]
    if x in dat and y in dat1:
        messagebox.showinfo("Login", "Correct username and password")
    elif x != dat and y != dat1:
        messagebox.showerror("Error", "Username and Password invalid")

    # Clear the text boxes
    f.delete(0, END)
    l.delete(0, END)


# Registration system
def regis():
    main = Toplevel()
    main.title("Registration")
    main.iconbitmap("fb.ico")
    # main.attributes('-alpha', 0.95)
    global img
    global photo
    lab1 = Label(main, image=photo)
    lab1.pack()
    # setting the maximum and minimum size of the window
    main.maxsize(width=550, height=300)
    main.minsize(width=550, height=300)

    # Create a databases or connect to one
    conn = sqlite3.connect('registrations.db')

    # Create cursor
    c = conn.cursor()

    # Creating a table registration

    # c.execute(""" CREATE TABLE register(
    #       First name text,
    #       Last name text,
    #       User name text,
    #       password text,
    #       Mail text
    # ) """)
    # print("Table created")

    def add():
        conn = sqlite3.connect("registrations.db")
        c = conn.cursor()
        c.execute("INSERT INTO register VALUES (:First, :Last, :User, :password, :Mail)", {
            'First': f.get(),
            'Last': l.get(),
            'User': u.get(),
            'password': ei.get(),
            'Mail': vl.get()
        })
        messagebox.showinfo("Login Info", "REGISTERED SUCCESSFULLY")
        conn.commit()
        conn.close()

        # clear the text boxes
        f.delete(0, END)
        l.delete(0, END)
        u.delete(0, END)
        ei.delete(0, END)
        vl.delete(0, END)

    # Creating labels
    lab_1 = Label(main, text="REGISTRATION", bg="black", fg="deep sky blue", font=("Geneva", 24, 'bold'))
    lab_1.place(x=10, y=10)

    # Create text boxes first name, last name, username, password and email ID
    f = Entry(main, width=40, font=("Helvetica", 10, "bold", "italic"), borderwidth=3, bg="LightCyan2", fg="black")
    f.place(x=130, y=75)
    l = Entry(main, width=40, font=("Helvetica", 10, "bold", "italic"), borderwidth=3, bg="LightCyan2", fg="black")
    l.place(x=130, y=105)
    u = Entry(main, width=40, font=("Helvetica", 10, "bold", "italic"), borderwidth=3, bg="LightCyan2", fg="black")
    u.place(x=130, y=135)
    ei = Entry(main, width=40, font=("Helvetica", 10, "italic", "bold"), borderwidth=3, bg="LightCyan2", fg="black")
    ei.place(x=130, y=165)
    vl = Entry(main, width=40, font=("Helvetica", 10, "bold", "italic"), borderwidth=3, bg="LightCyan2", fg="black")
    vl.place(x=130, y=195)

    # Creating labels for first name, last name, username, password and email ID
    f_lab = Label(main, text="First name :", font=("Helvetica", 11, "bold"), width=10, borderwidth=3, fg="royal blue3", bg="black")
    f_lab.place(x=20, y=73)
    l_lab = Label(main, text="Last name :", font=("Helvetica", 11, "bold"), width=10, borderwidth=3, fg="royal blue3", bg="black")
    l_lab.place(x=20, y=103)
    u_lab = Label(main, text="User name :", font=("Helvetica", 11, "bold"), width=10, borderwidth=3, fg="royal blue3", bg="black")
    u_lab.place(x=20, y=133)
    vl_lab = Label(main, text="Password :", font=("Helvetica", 11, "bold"), width=10, borderwidth=3, fg="royal blue3", bg="black")
    vl_lab.place(x=20, y=163)
    ei_lab = Label(main, text="Email ID :", font=("Helvetica", 11, "bold"), width=10, borderwidth=3, fg="royal blue3", bg="black")
    ei_lab.place(x=20, y=193)

    # Creating a save button
    but1 = Button(main, text="SAVE", font=("Helvetica", 11, "bold"), bg="royal blue2", width=35,
                  command=lambda: [add(), main.destroy()])
    but1.place(x=130, y=250)


# Downloader window
def new():
    global root
    # creating a window
    root = Toplevel()
    root.title("Facebook Video Downloader")
    root.iconbitmap("fb.ico")
    # root.attributes('-alpha', 0.90)
    global img
    global photo
    lab1 = Label(root, image=photo)
    lab1.pack()

    # setting the maximum and minimum size of the window
    root.maxsize(width=950, height=600)
    root.minsize(width=950, height=600)

    # Create a databases or connect to one
    conn = sqlite3.connect('inform.db')

    # Create cursor
    c = conn.cursor()

    # Creating a table for link and browse path

    # c.execute(""" CREATE TABLE data(
    #       Video Link text,
    #       Browse path text
    # ) """)
    #
    # print("Table created")

    # Browse function
    def browse():
        down_dir = filedialog.askdirectory(initialdir="YOUR DIR PATH")
        down_path.set(down_dir)

    # Download function
    def download():
        conn = sqlite3.connect("inform.db")
        c = conn.cursor()
        c.execute("INSERT INTO data VALUES (:vid_url, :browse_path)", {
            'vid_url': input1.get(),
            'browse_path': input2.get()
        })
        messagebox.showinfo("Video Info", "INSERTED SUCCESSFULLY")
        conn.commit()
        conn.close()

        url = input.get()
        if "www.facebook.com" in url:
            url = url
        else:
            try:
                url = requests.head(url).headers['location']
            except:
                messagebox.showerror("URL ERROR", "Enter valid URL")
                return
        x = re.match(r'^(https:|)[/][/]www.([^/]+[.])*facebook.com', url)
        if x:
            html = requests.get(url).content.decode('utf-8')
        else:
            messagebox.showerror("ERROR", "Cannot fetch the video url")
            return
        hd = re.search('hd_src:"https', html)
        sd = re.search('sd_src:"https', html)
        empty = []
        theempty = [hd, sd]
        for id, val in enumerate(theempty):
            if val != None:
                empty.append(id)
        print(empty)
        if len(empty) == 2:
            messagebox.showinfo("ABOUT VIDEO", "Both HD and SD are available")
        elif empty[0] == 0:
            messagebox.showinfo("ABOUT VIDEO", "Only HD is available")
        elif empty[0] == 1:
            messagebox.showinfo("ABOUT VIDEO", "Only SD is available")
        elif len(empty) == 0:
            messagebox.showinfo("ABOUT VIDEO", "Neither HD nor SD is available")

        # Standard Definition : SD
        if var.get() == 1:
            video_url = re.search(rf'hd_src:"(.+?)"', html).group(1)
            file_size_request = requests.get(video_url, stream=True)
            block_size = 1024
            print("DOWNLOADING.................")
            filename = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')
            path = down_path.get()
            with open(os.path.join(path, filename) + '.mp4', 'wb') as f:
                for data in file_size_request.iter_content(block_size):
                    f.write(data)

            messagebox.showinfo("HD: Downloaded", "Successfully downloaded in " + str(path))
            print("DOWNLOADED")

        # High Definition : HD
        elif var.get() == 2:
            video_url = re.search(rf'sd_src:"(.+?)"', html).group(1)

            file_size_request = requests.get(video_url, stream=True)
            print("DOWNLOADING.................")
            block_size = 1024
            filename = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')
            path = down_path.get()
            with open(os.path.join(path, filename) + '.mp4', 'wb') as f:
                for data in file_size_request.iter_content(block_size):
                    f.write(data)

            messagebox.showinfo("HD: Downloaded", "Successfully downloaded in " + str(path))
            print("DOWNLOADED")

    # Creating query function for database
    def query():
        conn = sqlite3.connect('inform.db')
        c = conn.cursor()
        c.execute("SELECT *, oid FROM data")
        rec = c.fetchall()
        print(rec)
        top = Toplevel()
        top.configure(bg='royal blue3')
        top.title("Records")
        top.iconbitmap("fb.ico")
        # Loop through the results
        print_rec = ""
        for record in rec:
            print_rec += "video link:" + ' ' + str(record[0]) + '     ' + "browse path:" + '  ' + str(
                record[1]) + '    ' + '\t' + str(record[2]) + "\n"

        query_label = Label(top, text=print_rec,  font=("cambria", 12, "bold"), bg="royal blue3", fg="white")
        query_label.pack()
        Button(top, text="Close", command=top.destroy).pack()
        conn.commit()
        conn.close()

    # Creating delete function
    def delete():
        conn = sqlite3.connect('inform.db')
        c = conn.cursor()
        c.execute("DELETE from data WHERE oid =" + dlt.get())
        print("DELETED SUCCESSFULLY")
        c.execute("SELECT *, oid FROM data")
        rec = c.fetchall()
        top1 = Toplevel()
        top1.title("New records")
        top1.configure(bg='royal blue3')
        # Loop through the results
        print_rec = ""
        for record in rec:
            print_rec += str(record[0]) + ' ' + str(record[1]) + ' ' + '\t' + str(record[2]) + "\n"
        query_label = Label(top1, text=print_rec, font=("cambria", 12, "bold"), bg="royal blue3", fg="white")
        query_label.pack()
        Button(top1, text="Close", command=top1.destroy).pack()
        conn.commit()
        conn.close()

    # Creating an update function
    def update():
        conn = sqlite3.connect('inform.db')
        c = conn.cursor()
        record_id = dlt.get()
        c.execute(""" UPDATE data SET
             Video Link = :video link,
             Browse path = :browse path
             WHERE oid = :oid""",
                  {'video link': f_editor.get(),
                   'browse path': l_editor.get(),
                   'oid': record_id
                   }
                  )
        conn.commit()
        conn.close()
        # Destroying all the data and closing window
        editor.destroy()

    # Edit function
    def edit():
        global editor
        editor = Toplevel()
        editor.title("Update Info")
        editor.maxsize(width=500, height=250)
        editor.minsize(width=500, height=250)
        # Connecting the database
        conn = sqlite3.connect('inform.db')
        # Create cursor
        c = conn.cursor()
        record_id = dlt.get()
        c.execute("SELECT * FROM data WHERE oid=" + record_id)
        rec = c.fetchall()

        # Creating global variable for all text boxes
        global f_editor
        global l_editor

        label_1 = Label(editor, text="Update", bg="crimson", fg="black", width=29, font=("Helvetica", 20))
        label_1.place(x=14, y=20)

        # Creating text boxes
        f_editor = Entry(editor, width=40, font=("Helvetica", 11, "bold", "italic"), bg="LightCyan2", borderwidth=3)
        f_editor.place(x=125, y=95)
        l_editor = Entry(editor, width=40, font=("Helvetica", 11, "bold", "italic"), bg="LightCyan2", borderwidth=3)
        l_editor.place(x=125, y=150)

        # Creating textbox labels
        f_lab = Label(editor, text="Video Link :", font=("Helvetica", 11, "bold"), bg="PeachPuff2", width=11, borderwidth=3)
        f_lab.place(x=10, y=94)
        l_lab = Label(editor, text="Browse path :", font=("Helvetica", 11, "bold"), bg="PeachPuff2", width=11, borderwidth=3)
        l_lab.place(x=10, y=149)

        for record in rec:
            f_editor.insert(0, record[0])
            l_editor.insert(0, record[1])

        # Creating a save button
        edit_btn = Button(editor, text="SAVE", font=("Helvetica", 10, "bold"), width=59, command=update)
        edit_btn.place(x=10, y=200)

        conn.commit()
        conn.close()

    # Creating labels
    label_2 = Label(root, text="Facebook", bg="black", fg="royal blue3", font=("Geneva", 24, 'bold'))
    label_2.place(x=10, y=10)
    label_2 = Label(root, text="Video Downloader", bg="black", fg="deep sky blue", font=("Helvetica", 18, 'bold'))
    label_2.place(x=170, y=18)
    lab = Label(root, text="Paste Your Video URL", bg="black", fg="steel blue", font='Helvetica 18 bold italic', borderwidth=3)
    lab.place(x=160, y=85)
    lab1 = Label(root, text="Choose Your Browse Path", bg="black", fg="steel blue", font='Helvetica 18 bold italic', borderwidth=3)
    lab1.place(x=160, y=160)

    # Input variable
    input = StringVar()
    input1 = Entry(root, textvariable=input, width=35, font='Helvetica 15', bg="light cyan", relief='flat')
    input1.place(x=160, y=125)
    vid = Label(root, text="Video URL :", font=('Helvetica', 15, 'bold'), bg="black", fg="deep sky blue2", width=10)
    vid.place(x=10, y=125)

    # Download path variable
    down_path = StringVar()
    input2 = Entry(root, textvariable=down_path, width=35, font='Helvetica 15', bg="LightCyan2", relief='flat')
    input2.place(x=160, y=200)
    path = Label(root, text="Browse Path : ", font=('Helvetica', 15, 'bold'), bg="black", fg="deep sky blue3", width=12)
    path.place(x=10, y=200)

    # Creating browse button
    browse = Button(root, text="Browse", font='Helvetica 15', bg="royal blue3", fg='light cyan', width=35, height=1, command=browse)
    browse.place(x=160, y=240)

    # Creating a radio button
    var = IntVar()
    Radiobutton(root, text="HD", variable=var, font=("Helvetica", 15, "bold"), bg="royal blue", fg='black', value=1, width=10, borderwidth=3).place(x=160, y=290)
    Radiobutton(root, text="SD", variable=var, font=("Helvetica", 15, "bold"), bg="royal blue", fg='black', value=2, width=10, borderwidth=3).place(x=360, y=290)

    lab2 = Label(root, text="Resolution : ", font=('Helvetica', 15, 'bold'), bg="black", fg="deep sky blue3", width=10, borderwidth=3)
    lab2.place(x=10, y=290)

    # Creating a download button
    btn1 = Button(root, text="Download", width=35, bg="royal blue4", fg='light cyan', font='Helvetica 15', command=download)
    btn1.place(x=160, y=340)

    # Creating query button
    query_btn = Button(root, text="Show info", width=35, font='Helvetica 15', bg="royal blue2", fg='light cyan', command=query)
    query_btn.place(x=160, y=390)

    # Creating a delete label
    dlt = Entry(root, width=35, font='Helvetica 15', bg="LightCyan2", fg="black", relief='flat')
    dlt.place(x=160, y=445)
    dlt_lab = Label(root, text="Delete ID : ", font=('Helvetica', 15, 'bold'), bg="black", fg="deep sky blue3", width=10)
    dlt_lab.place(x=10, y=445)

    # Creating delete button
    dlt_btn = Button(root, text="Delete", font='Helvetica 15', bg="royal blue4", fg='light cyan', width=15, padx=7,
                     pady=7, command=delete)
    dlt_btn.place(x=160, y=500)

    # Creating update button
    upd_btn = Button(root, text="Update", font='Helvetica 15', bg="royal blue3", fg='light cyan', width=15, padx=7,
                     pady=7, command=edit)
    upd_btn.place(x=365, y=500)

    # Commit change
    conn.commit()

    # Close connection
    conn.close()


# Creating a title label
label_2 = Label(h, text="LOGIN", bg="black", fg="royal blue3", font=("Geneva", 24, 'bold'))
label_2.place(x=10, y=10)
label_2 = Label(h, text="System", bg="black", fg="royal blue3", font=("Geneva", 18, 'bold'))
label_2.place(x=120, y=14)

# Create text boxes
var = StringVar()
f = Entry(h, textvariable=var, width=45, font=("Helvetica", 10, "bold", "italic"), borderwidth=3, bg="LightCyan2",  fg="black")
f.place(x=120, y=75)
var1 = StringVar()
l = Entry(h, show='*', textvariable=var1, width=45, font=("Helvetica", 10, "bold", "italic"), borderwidth=3, bg="LightCyan2", fg="black")
l.place(x=120, y=105)

# Creating labels
f_lab = Label(h, text="User name :", font=("Helvetica", 11, "bold"), width=10, borderwidth=3, bg="black", fg="deep sky blue2")
f_lab.place(x=10, y=73)
l_lab = Label(h, text="Password :", font=("Helvetica", 11, "bold"), width=10, bg="black", fg="deep sky blue2", borderwidth=3)
l_lab.place(x=10, y=103)

# Creating a login button
bu = Button(h, text="Login", width=20, font=("Helvetica", 10, "bold", "italic"), borderwidth=3, command=lambda: [tes(), new()]).place(x=170, y=150)

# Creating a label
lab_0 = Label(h, text="OR", font=("Helvetica", 12, "bold"), bg="black", fg="royal blue3").place(x=241, y=190)

# Creating a signup button
bu1 = Button(h, text="Sign-up", width=20, font=("Helvetica", 10, "bold", "italic"), command=regis).place(x=170, y=225)

h.mainloop()
