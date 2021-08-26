from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import sqlite3
import requests
import re
from datetime import datetime
import os

# Window
root = Tk()
root.geometry('900x600')
root.resizable(0, 0)
root.title("Video Downloader")
root.iconbitmap('fb.ico')
root.config(bg="steel blue4")

photo2 = Image.open('fbwp1.jpg')
resized = photo2.resize((900, 600), Image.ANTIALIAS)
converted = ImageTk.PhotoImage(resized)
label = Label(root, image=converted, width=900, height=600)
label.pack()

# Creating a database using sqlite3
con = sqlite3.connect('links.db')
c = con.cursor()

# Table
# c.execute('''CREATE TABLE links(link text, path text)''')
# print('Table created')


# Show function to show the used links and file location
def show():
    con = sqlite3.connect('links.db')
    c = con.cursor()
    c.execute('SELECT *, oid FROM links')
    records = c.fetchall()
    display = Toplevel()
    display.title('Data')
    display.geometry('500x300')

    print(records)
    print_records = ''
    for record in records:
        print_records += 'Link' + '\n' + str(record[0]) + '\n'
    lab = Label(display, text=print_records, font=('cambria', 10))
    lab.grid(row=2, column=1)

    print_records2 = ''
    for record1 in records:
        print_records2 += 'Path' + '\n' + str(record1[1]) + '\n'
    lab = Label(display, text=print_records2, font=('cambria', 10))
    lab.grid(row=2, column=2)
    but = Button(display, text="Close", font=('cambria', 10), command=display.destroy)
    but.grid(row=5, column=1)


# Delete function to delete the data
def delete():
    con = sqlite3.connect('links.db')
    c = con.cursor()
    c.execute("DELETE from links WHERE oid =" + Id.get())
    print('Deleted Successfully')
    c.execute("SELECT *, oid FROM links")
    records = c.fetchall()
    print(records)
    print_records = ''
    for record in records:
        print_records += str(record[0]) + ' ' + '\t' + str(record[1]) + '\n'
    lab = Label(root, text=print_records, font="Helvetica 10", bg='steel blue4')
    lab.place(x=350, y=530)
    con.commit()
    con.close()


# For downloading HD
def download_hd():
    global video_url
    con = sqlite3.connect('links.db')
    c = con.cursor()
    c.execute('INSERT INTO links VALUES ( :video_url, :download_path)',
              {'video_url': video_url.get(), 'download_path': download_path.get()})
    messagebox.showinfo('links', 'Added')
    con.commit()
    con.close

    url = input_url.get()
    # Checks if the url is facebook's or not
    if "www.facebook.com" in url:
        url = url
    else:
        try:
            url = requests.head(url).headers['location']
        except:
            details.config(text="Error : Not a facebook urk")
    x = re.match(r'^(https:|)[/][/]www.([^/]+[.])*facebook.com', url)

    # After getting the url converts it into html by decoding utf 8
    if x:
        html = requests.get(url).content.decode('utf-8')
    else:
        details.config("cannot fetch the video url")

    # Get HD and SD
    hd = re.search('hd_src:"https', html)
    sd = re.search('sd_src:"https', html)

    # Check for availability of download quality (High Definition - HD, Standard Definition - SD)
    empty = []
    list_quality = [hd, sd]

    for id, val in enumerate(list_quality):
        if val != None:
            empty.append(id)
    print(empty)
    if len(empty) == 2:
        details.config(text="Both HD and SD are available")
    elif empty[0] == 0:
        details.config(text="Only HD is available")
    elif empty[0] == 1:
        details.config(text="Only SD is available")
    elif len(empty) == 0:
        details.config(text="Neither HD nor SD is available")

    # Set the download destination and download
    video_url = re.search(rf'hd_src:"(.+?)"', html).group(1)
    file_size_request = requests.get(video_url, stream=True)
    block_size = 1024
    filename = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')
    path = download_path.get()

    # Use write mode in file handling to download the video
    with open(os.path.join(path, filename) + '.mp4', 'wb') as f:
        for data in file_size_request.iter_content(block_size):
            f.write(data)
    messagebox.showinfo("HD: Downloaded Successfully", "Successfully downloaded in " + str(path))


# For downloading SD
def download_sd():
    global video_url
    con = sqlite3.connect('links.db')
    c = con.cursor()
    c.execute('INSERT INTO links VALUES ( :video_url, :download_path)',
              {'video_url': video_url.get(), 'download_path': download_path.get()})
    messagebox.showinfo('links', 'Added')
    con.commit()
    con.close

    url = input_url.get()

    # Checks if the url is facebook's or not
    if "www.facebook.com" in url:
        url = url
    else:
        try:
            url = requests.head(url).headers['location']
        except:
            details.config(text="Something error error")
    x = re.match(r'^(https:|)[/][/]www.([^/]+[.])*facebook.com', url)

    # After getting the url converts it into html by decoding utf 8
    if x:
        html = requests.get(url).content.decode('utf-8')
    else:
        details.config("cannot fetch the video url")
    hd = re.search('hd_src:"https', html)
    sd = re.search('sd_src:"https', html)

    # Check for availability of download quality (High Definition - HD, Standard Definition - SD)
    empty = []
    quality = [hd, sd]
    for id, val in enumerate(quality):
        if val != None:
            empty.append(id)
    print(empty)
    if len(empty) == 2:
        details.config(text="BOTH HD AND SD AVAILABLE")
    elif empty[0] == 0:
        details.config(text="ONLY HD AVAILABLE")
    elif empty[0] == 1:
        details.config(text="ONLY SD AVAILABLE")
    elif len(empty) == 0:
        details.config(text="NO HD AND SD VIDEO ARE AVAILABLE")

    # Set the download destination and download
    videos_url = re.search(rf'sd_src:"(.+?)"', html).group(1)
    file_size_request = requests.get(videos_url, stream=True)
    block_size = 1024
    filename = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')
    path = download_path.get()

    # Use write mode in file handling to download the video
    with open(os.path.join(path, filename) + '.mp4', 'wb') as f:
        for data in file_size_request.iter_content(block_size):
            f.write(data)
    messagebox.showinfo("HD: Downloaded Successfully", "Successfully downloaded in " + str(path))


# BROWSE
def browse():
    download_dir = filedialog.askdirectory(initialdir="YOUR DIR PATH")
    download_path.set(download_dir)


# Label, Entry and buttons for url
Label(root, text="Facebook Video Downloader", font='Helvetica 20 bold', bg="steel blue4", fg="white", relief="flat", pady=3).place(x=10, y=10)
Label(root, text="Enter url :", font='Helvetica 15', bg='steel blue4', fg='white').place(x=20, y=120)
input_url = StringVar()
video_url = Entry(root, textvariable=input_url, width=40, font="Helvetica 15")
video_url.place(x=120, y=120)

# Label, Entry and Buttons for setting path
Label(root, text="Choose Browse path", font='Helvetica 15', bg='steel blue4', fg='white').place(x=20, y=165)
download_path = StringVar()
Button(root, text="Set Path", font="Helvetica 15", command=browse).place(x=240, y=160)
Entry(root, textvariable=download_path, width=40, font='Helvetica 15').place(x=80, y=220)

# Label, Entry and buttons for showing and deleting database
show = Button(root, text='Show data', font='Helvetica 15', command=show)
show.place(x=110, y=320)
identity = Label(root, text='Delete ID', font='Helvetica 15', bg='steel blue4', fg='white')
identity.place(x=160, y=380)
Id = Entry(root, font='Helvetica 15')
Id.place(x=260, y=380)
del_btn = Button(root, text='Delete data', font='Helvetica 15 ', command=delete)
del_btn.place(x=355, y=320)

# Create a button for HD and SD download
Button(root, text="Download HD", font="Helvetica 15", command=download_hd).place(x=110, y=270)
Button(root, text="Download SD", font="Helvetica 15", command=download_sd).place(x=355, y=270)

# Download details
details = Label(root, font='Helvetica 12', relief='flat', bg='steel blue4', fg='white', padx=10, pady=5)
details.place(x=120, y=430)

root.mainloop()