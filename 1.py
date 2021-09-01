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
root.iconbitmap("fb1.ico")
root.attributes('-alpha', 0.90)

# setting the maximum and minimum size of the window
root.maxsize(width=500, height=560)
root.minsize(width=500, height=560)

# adding image in the background
img=Image.open("fbwp1.jpg")
img=img.resize((500,800),Image.ANTIALIAS)
photo=ImageTk.PhotoImage(img)
lab=Label(root,image=photo)
lab.pack()

# Create a databases or connect to one
conn = sqlite3.connect('inform.db')

# Create cursor
c = conn.cursor()

# creating a table
'''
c.execute(""" CREATE TABLE data(
      Video Link text,
      Browse path text
) """)

print("Table created")
'''

# creating a new window inside root window

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
            messagebox.showerror("URL ERROR","Enter valid URL")
    x = re.match(r'^(https:|)[/][/]www.([^/]+[.])*facebook.com', url)
    if x:
            html = requests.get(url).content.decode('utf-8')
    else:
            messagebox.showerror("ERROR","Cannot fetch the video url")
    hd = re.search('hd_src:"https', html)
    sd = re.search('sd_src:"https', html)
    list = []
    thelist = [hd, sd]
    for id, val in enumerate(thelist):
        if val != None:
                list.append(id)
    print(list)
    if len(list) == 2:
            messagebox.showinfo("ABOUT VIDEO","BOTH HD AND SD AVAILABLE")
    elif list[0] == 0:
            messagebox.showinfo("ABOUT VIDEO", "ONLY HD AVAILABLE")
    elif list[0] == 1:
            messagebox.showinfo("ABOUT VIDEO", "ONLY SD AVAILABLE")
    elif len(list) == 0:
            messagebox.showinfo("ABOUT VIDEO", "NEITHER HD NOR SD AVAILABLE")

    if var.get()==1:
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

    elif var.get()==2:
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





# creating query function for database
def query():
    conn = sqlite3.connect('inform.db')
    c = conn.cursor()
    c.execute("SELECT *, oid FROM data")
    rec = c.fetchall()
    print(rec)
    top = Toplevel()
    top.title("Records")
    top.iconbitmap("fb1.ico")
    # loop through the results
    print_rec = ""
    for record in rec:
        print_rec += "video link:"+' '+str(record[0]) + '     ' + "browse path:"+'  '+str(record[1]) + '    ' + '\t' + str(record[2]) + "\n"
    query_label = Label(top, text=print_rec)
    query_label.pack()
    Button(top, text="Close", command=top.destroy).pack()
    conn.commit()
    conn.close()


# creating delete function
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


# creating an update function
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

    # creating global variable for all text boxes
    global f_editor
    global l_editor

    label_1 = Label(editor, text="Update", bg="crimson", fg="black", width=29, font=("Comic Sans MS", 20))
    label_1.place(x=14, y=20)

    # creating text boxes
    f_editor = Entry(editor, width=40,font=("Comic Sans MS", 11, "bold","italic"),bg="LightCyan2",borderwidth=3)
    f_editor.place(x=125, y=95)
    l_editor = Entry(editor, width=40,font=("Comic Sans MS", 11, "bold","italic"),bg="LightCyan2",borderwidth=3)
    l_editor.place(x=125, y=150)

    # creating textbox labels
    f_lab = Label(editor, text="Video Link :",font=("Comic Sans MS", 11, "bold"),bg="PeachPuff2",width=11,borderwidth=3)
    f_lab.place(x=10, y=94)
    l_lab = Label(editor, text="Browse path :",font=("Comic Sans MS", 11, "bold"),bg="PeachPuff2",width=11,borderwidth=3)
    l_lab.place(x=10, y=149)

    for record in rec:
        f_editor.insert(0, record[0])
        l_editor.insert(0, record[1])

    # creating a save button
    edit_btn = Button(editor, text="SAVE", font=("Comic Sans MS", 10, "bold"), width=59, command=update)
    edit_btn.place(x=10, y=200)

    conn.commit()
    conn.close()


# creating labels
label_2 = Label(root, text="Facebook Video Downloader", bg="#FF4848", fg="#171010", width=29,font=("Comic Sans MS", 20))
label_2.place(x=14, y=20)
lab = Label(root, text="Paste Your Video URL",bg="#ECD662", fg="black", width=25, font=("Comic Sans MS", 13,"bold","italic"),borderwidth=3)
lab.place(x=120, y=80)
lab1 = Label(root, text="Choose Your Browse Path", bg="#9EDE73", fg="black", width=25, font=("Comic Sans MS", 13,"bold","italic"),borderwidth=3)
lab1.place(x=120, y=165)

# input variable
input = StringVar()
input1=Entry(root,textvariable=input,width=40,font=("Comic Sans MS", 11, "bold","italic"),bg="LightCyan2",borderwidth=3)
input1.place(x=125,y=125)
vid = Label(root, text="Video URL :", font=("Comic Sans MS", 11, "bold"),bg="PeachPuff2",width=11,borderwidth=3)
vid.place(x=10, y=125)

# download path variable
down_path=StringVar()
input2=Entry(root,textvariable=down_path,width=40,font=("Comic Sans MS", 11, "bold","italic"),bg="LightCyan2",borderwidth=3)
input2.place(x=125,y=210)
path=Label(root,text="Browse Path :",font=("Comic Sans MS", 11, "bold"),bg="PeachPuff2",width=11,borderwidth=3)
path.place(x=10,y=210)

# creating browse button
browse=Button(root,text="Browse",font=("Comic Sans MS", 10, "bold","italic"),bg="#BEAEE2",width=20,borderwidth=3,height=1,command=browse)
browse.place(x=170,y=248)

# creating a radio button
var = IntVar()
Radiobutton(root, text="HD", variable=var,font=("Comic Sans MS",9, "bold","italic"),bg="#FFBCBC", value=1,width=15,borderwidth=3).place(x=124, y=290)
Radiobutton(root, text="SD", variable=var,font=("Comic Sans MS",9, "bold","italic"),bg="#FFBCBC",value=2,width=15,borderwidth=3).place(x=265,y=290)

lab2=Label(root,text="Resolution :",font=("Comic Sans MS", 11, "bold"),bg="PeachPuff2",width=11,borderwidth=3)
lab2.place(x=10,y=290)

# creating a download button
btn1 = Button(root,text="Download",width=32,borderwidth=3,bg="#FF7A00",font=("Comic Sans MS", 13,"bold","italic"),command=download)
btn1.place(x=85, y=335)

# creating query button
query_btn = Button(root, text="Show info", font=("Comic Sans MS", 10,"bold","italic"),bg="#FFBCBC",borderwidth=3, width=59, command=query)
query_btn.place(x=9, y=390)

# creating a delete label
dlt = Entry(root, width=40, font=("Comic Sans MS", 11,"bold","italic"),borderwidth=3,bg="LightCyan2",fg="black")
dlt.place(x=125, y=445)
dlt_lab=Label(root,text="Delete ID :",font=("Comic Sans MS", 11, "bold"),bg="PeachPuff2",width=11,borderwidth=3)
dlt_lab.place(x=10,y=445)

# creating delete button
dlt_btn = Button(root, text="Delete", font=("Comic Sans MS", 10,"bold","italic"),bg="khaki1",borderwidth=3, width=59,command=delete)
dlt_btn.place(x=9, y=482)

# creating update button
upd_btn = Button(root, text="Update", font=("Comic Sans MS", 10,"bold","italic"),bg="#BEAEE2",borderwidth=3,width=59, command=edit)
upd_btn.place(x=9, y=519)

# commit change
conn.commit()
# close connection
conn.close()

root.mainloop()