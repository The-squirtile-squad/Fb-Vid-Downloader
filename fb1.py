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
root.maxsize(width=480, height=450)
root.minsize(width=480, height=450)

# adding image in the background
img=Image.open("fb.jpg")
img=img.resize((500,500),Image.ANTIALIAS)
photo=ImageTk.PhotoImage(img)
lab=Label(root,image=photo)
lab.pack()

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

# creating a new window inside root window
def new():
    global img
    global photo
    top=Toplevel()
    top.title("Facebook Video Downloader")
    top.attributes('-alpha', 0.90)
    top.maxsize(width=500, height=400)
    top.minsize(width=500, height=400)
    top.iconbitmap("fb.ico")

    #adding image in the bg
    lbl1=Label(top,image=photo)
    lbl1.pack()

    # browse function
    def browse():
        down_dir = filedialog.askdirectory(initialdir="YOUR DIR PATH")
        down_path.set(down_dir)

    def download():
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

            messagebox.showinfo("HD: Downloaded", "Successfully downloade in " + str(path))
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

            messagebox.showinfo("HD: Downloaded", "Successfully downloade in " + str(path))
            print("DOWNLOADED")

    # creating labels
    label_2 = Label(top, text="Facebook Video Downloader", bg="#FF4848", fg="#171010", width=29,font=("Comic Sans MS", 20))
    label_2.place(x=14, y=20)
    lab = Label(top, text="Paste Your Video URL",bg="#ECD662", fg="black", width=25, font=("Comic Sans MS", 13,"bold","italic"),borderwidth=3)
    lab.place(x=115, y=80)
    lab1 = Label(top, text="Choose Your Browse Path", bg="#9EDE73", fg="black", width=25, font=("Comic Sans MS", 13,"bold","italic"),borderwidth=3)
    lab1.place(x=115, y=165)

    # input variable
    input=StringVar()
    input1=Entry(top,textvariable=input,width=40,font=("Comic Sans MS", 11, "bold","italic"),bg="LightCyan2",borderwidth=3)
    input1.place(x=125,y=125)
    vid = Label(top, text="Video URL :", font=("Comic Sans MS", 11, "bold"),bg="PeachPuff2",width=11,borderwidth=3)
    vid.place(x=10, y=125)

    # download path variable
    down_path=StringVar()
    input2=Entry(top,textvariable=down_path,width=40,font=("Comic Sans MS", 11, "bold","italic"),bg="LightCyan2",borderwidth=3)
    input2.place(x=125,y=210)
    path=Label(top,text="Browse Path :",font=("Comic Sans MS", 11, "bold"),bg="PeachPuff2",width=11,borderwidth=3)
    path.place(x=10,y=210)

    # creating browse button
    browse=Button(top,text="Browse",font=("Comic Sans MS", 10, "bold","italic"),bg="#BEAEE2",width=15,borderwidth=3,height=1,command=browse)
    browse.place(x=180,y=245)

    # creating a radio button
    var = IntVar()
    Radiobutton(top, text="HD", variable=var,font=("Comic Sans MS",9, "bold","italic"),bg="#FFBCBC", value=1,width=15,borderwidth=3).place(x=125, y=290)
    Radiobutton(top, text="SD", variable=var,font=("Comic Sans MS",9, "bold","italic"),bg="#FFBCBC",value=2,width=15,borderwidth=3).place(x=265,y=290)

    lab2=Label(top,text="Resolution :",font=("Comic Sans MS", 11, "bold"),bg="PeachPuff2",width=11,borderwidth=3)
    lab2.place(x=10,y=290)

    # creating a download button
    btn1 = Button(top,text="Download",width=32,borderwidth=3,bg="#FF7A00",font=("Comic Sans MS", 13,"bold","italic"),command=download)
    btn1.place(x=85, y=340)


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
    top.iconbitmap("fb1.ico")
    # loop through the results
    print_rec = ""
    for record in rec:
        print_rec += ("Username:")+' '+str(record[2]) + '     ' + "Video Link:"+' '+str(record[4]) + '    ' + '\t' + str(record[5]) + "\n"
    query_label = Label(top, text=print_rec)
    query_label.pack()
    Button(top, text="Close", command=top.destroy).pack()
    conn.commit()
    conn.close()


# creating delete function
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

# creating a title label
label_0 = Label(root, text="Login System", bg="#FF4848", fg="#171010", width=28,height=1, font=("Comic Sans MS", 20))
label_0.place(x=14, y=15)

# create text boxes
f = Entry(root, width=40, font=("Comic Sans MS", 10,"bold","italic"),borderwidth=3,bg="LightCyan2",fg="black")
f.place(x=130, y=75)
l = Entry(root, width=40, font=("Comic Sans MS", 10,"bold","italic"),borderwidth=3,bg="LightCyan2",fg="black")
l.place(x=130, y=105)
u = Entry(root, width=40, font=("Comic Sans MS", 10,"bold","italic"),borderwidth=3,bg="LightCyan2",fg="black")
u.place(x=130, y=135)
ei = Entry(root, width=40, font=("Comic Sans MS", 10,"italic","bold"),borderwidth=3,bg="LightCyan2",fg="black")
ei.place(x=130, y=165)
vl = Entry(root, width=40, font=("Comic Sans MS", 10,"bold","italic"),borderwidth=3,bg="LightCyan2",fg="black")
vl.place(x=130, y=195)
# creating a delete box
dlt = Entry(root, width=40, font=("Comic Sans MS", 10,"bold","italic"),borderwidth=3,bg="LightCyan2",fg="black")
dlt.place(x=130, y=308)

# creating labels
f_lab = Label(root, text="First name :", font=("Comic Sans MS", 11, "bold"),width=10,borderwidth=3,bg="PeachPuff2")
f_lab.place(x=20, y=74)
l_lab = Label(root, text="Last name :", font=("Comic Sans MS", 11, "bold"),width=10,borderwidth=3,bg="PeachPuff2")
l_lab.place(x=20, y=104)
u_lab = Label(root, text="User name :", font=("Comic Sans MS", 11, "bold"),width=10,borderwidth=3,bg="PeachPuff2")
u_lab.place(x=20, y=134)
ei_lab = Label(root, text="Email ID :", font=("Comic Sans MS", 11, "bold"),width=10,borderwidth=3,bg="PeachPuff2")
ei_lab.place(x=20, y=164)
vl_lab = Label(root, text="Video Link :", font=("Comic Sans MS", 11, "bold"),width=10,borderwidth=3,bg="PeachPuff2")
vl_lab.place(x=20, y=194)
dlt_lab = Label(root, text="Delete ID :", font=("Comic Sans MS", 11, "bold"),width=10,borderwidth=3,bg="PeachPuff2")
dlt_lab.place(x=20, y=307)

# creating add button
add_btn = Button(root, text="Add info", font=("Comic Sans MS", 10,"bold","italic"),bg="#50CB93", width=38,borderwidth=3, command=submit)
add_btn.place(x=85, y=230)

# creating query button
query_btn = Button(root, text="Show info", font=("Comic Sans MS", 10,"bold","italic"),bg="#FFBCBC",borderwidth=3, width=38, command=query)
query_btn.place(x=85, y=268)

# creating delete button
dlt_btn = Button(root, text="Delete", font=("Comic Sans MS", 10,"bold","italic"),bg="khaki1",borderwidth=3, width=38, command=delete)
dlt_btn.place(x=85, y=340)

# creating update button
upd_btn = Button(root, text="Update", font=("Comic Sans MS", 10,"bold","italic"),bg="#BEAEE2",borderwidth=3,width=38, command=edit)
upd_btn.place(x=85, y=377)

# creating window destroy button
close=Button(root,text="Close",font=("Comic Sans MS", 10,"bold","italic"),bg="OliveDrab2",borderwidth=3,width=25,command=root.destroy)
close.place(x=20,y=413)

# creating next window button
next_btn=Button(root,text="Next",font=("Comic Sans MS", 10,"bold","italic"),bg="OliveDrab2",borderwidth=3,width=26,command=new)
next_btn.place(x=235,y=413)

# commit change
conn.commit()
# close connection
conn.close()

root.mainloop()
