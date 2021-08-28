from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import sqlite3
from tkinter import filedialog
import requests
import re
from datetime import datetime
import os

# creating a window
root = Tk()
root.title("Facebook Video Downloader")
root.iconbitmap("fb2.ico")
root.attributes('-alpha', 0.90)

# setting the maximum and minimum size of the window
root.maxsize(width=950, height=600)
root.minsize(width=950, height=600)

# adding image in the background
img = Image.open("back.jpg")
img = img.resize((950, 600), Image.ANTIALIAS)
photo = ImageTk.PhotoImage(img)
lab = Label(root, image=photo)
lab.pack()

# Create a databases or connect to one
conn = sqlite3.connect('inform.db')

# Create cursor
c = conn.cursor()


# creating a table

# c.execute(""" CREATE TABLE data(
#       Video Link text,
#       Browse path text
# ) """)
#
# print("Table created")

# Creating a new window inside root window

# browse function
def browse():
    down_dir = filedialog.askdirectory(initialdir="YOUR DIR PATH")
    down_path.set(down_dir)


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
    x = re.match(r'^(https:|)[/][/]www.([^/]+[.])*facebook.com', url)
    if x:
        html = requests.get(url).content.decode('utf-8')
    else:
        messagebox.showerror("ERROR", "Cannot fetch the video url")
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
    top.title("Records")
    top.iconbitmap("fb.ico")
    # loop through the results
    print_rec = ""
    for record in rec:
        print_rec += "video link:" + ' ' + str(record[0]) + '     ' + "browse path:" + '  ' + str(
            record[1]) + '    ' + '\t' + str(record[2]) + "\n"
    query_label = Label(top, text=print_rec)
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
    # loop through the results
    print_rec = ""
    for record in rec:
        print_rec += str(record[0]) + ' ' + str(record[1]) + ' ' + '\t' + str(record[2]) + "\n"
    qur_label = Label(top1, text=print_rec)
    qur_label.pack()
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


def edit():
    global editor
    editor = Toplevel()
    editor.title("Update Info")
    editor.maxsize(width=500, height=250)
    editor.minsize(width=500, height=250)
    # connecting the database
    conn = sqlite3.connect('inform.db')
    # create cursor
    c = conn.cursor()
    record_id = dlt.get()
    c.execute("SELECT * FROM data WHERE oid=" + record_id)
    rec = c.fetchall()

    # Creating global variable for all text boxes
    global f_editor
    global l_editor

    label_1 = Label(editor, text="Update", bg="crimson", fg="black", width=29, font=("Comic Sans MS", 20))
    label_1.place(x=14, y=20)

    # creating text boxes
    f_editor = Entry(editor, width=40, font=("Comic Sans MS", 11, "bold", "italic"), bg="LightCyan2", borderwidth=3)
    f_editor.place(x=125, y=95)
    l_editor = Entry(editor, width=40, font=("Comic Sans MS", 11, "bold", "italic"), bg="LightCyan2", borderwidth=3)
    l_editor.place(x=125, y=150)

    # creating textbox labels
    f_lab = Label(editor, text="Video Link :", font=("Comic Sans MS", 11, "bold"), bg="PeachPuff2", width=11,
                  borderwidth=3)
    f_lab.place(x=10, y=94)
    l_lab = Label(editor, text="Browse path :", font=("Comic Sans MS", 11, "bold"), bg="PeachPuff2", width=11,
                  borderwidth=3)
    l_lab.place(x=10, y=149)

    for record in rec:
        f_editor.insert(0, record[0])
        l_editor.insert(0, record[1])

    # creating a save button
    edit_btn = Button(editor, text="SAVE", font=("Comic Sans MS", 10, "bold"), width=59, command=update)
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
dlt_btn = Button(root, text="Delete", font='Helvetica 15', bg="royal blue4", fg='light cyan', width=15, padx=7, pady=7, command=delete)
dlt_btn.place(x=160, y=500)

# Creating update button
upd_btn = Button(root, text="Update", font='Helvetica 15', bg="royal blue3", fg='light cyan', width=15, padx=7, pady=7, command=edit)
upd_btn.place(x=365, y=500)

# Commit change
conn.commit()

# Close connection
conn.close()

root.mainloop()
