from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import requests
import re
from datetime import datetime
import os

# windows
root = Tk()
root.geometry('900x600')
root.resizable(0, 0)
root.title("Video Downloader")
root.iconbitmap('fb.ico')
root.config(bg="royalblue4")

photo2 = Image.open('fbwp.jpg')
resized = photo2.resize((900, 600), Image.ANTIALIAS)
converted = ImageTk.PhotoImage(resized)
label = Label(root, image=converted, width=900, height=600)
label.pack()

# download hd
def download_hd():
    url = input_url.get()
    if "www.facebook.com" in url:
        url = url
    else:
        try:
            url = requests.head(url).headers['location']
        except:
            details.config(text="Something error error")
    x = re.match(r'^(https:|)[/][/]www.([^/]+[.])*facebook.com', url)
    if x:
        html = requests.get(url).content.decode('utf-8')
    else:
        details.config("cannot fetch the video url")
    hd = re.search('hd_src:"https', html)
    sd = re.search('sd_src:"https', html)
    list = []
    thelist = [hd, sd]
    for id, val in enumerate(thelist):
        if val != None:
            list.append(id)
    print(list)
    if len(list) == 2:
        details.config(text="BOTH HD AND SD AVAILABLE")
    elif list[0] == 0:
        details.config(text="ONLY HD AVAILABLE")
    elif list[0] == 1:
        details.config(text="ONLY SD AVAILABLE")
    elif len(list) == 0:
        details.config(text="NO HD AND SD VIDEO ARE AVAILABLE")
    video_url = re.search(rf'hd_src:"(.+?)"', html).group(1)
    file_size_request = requests.get(video_url, stream=True)
    block_size = 1024
    filename = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')
    path = download_path.get()
    with open(os.path.join(path, filename) + '.mp4', 'wb') as f:
        for data in file_size_request.iter_content(block_size):
            f.write(data)
    messagebox.showinfo("HD: Downloaded", "Successfully downloade in " + str(path))


def download_sd():
    url = input_url.get()
    if "www.facebook.com" in url:
        url = url
    else:
        try:
            url = requests.head(url).headers['location']
        except:
            details.config(text="Something error error")
    x = re.match(r'^(https:|)[/][/]www.([^/]+[.])*facebook.com', url)
    if x:
        html = requests.get(url).content.decode('utf-8')
    else:
        details.config("cannot fetch the video url")
    hd = re.search('hd_src:"https', html)
    sd = re.search('sd_src:"https', html)
    list = []
    thelist = [hd, sd]
    for id, val in enumerate(thelist):
        if val != None:
            list.append(id)
    print(list)
    if len(list) == 2:
        details.config(text="BOTH HD AND SD AVAILABLE")
    elif list[0] == 0:
        details.config(text="ONLY HD AVAILABLE")
    elif list[0] == 1:
        details.config(text="ONLY SD AVAILABLE")
    elif len(list) == 0:
        details.config(text="NO HD AND SD VIDEO ARE AVAILABLE")
    video_url = re.search(rf'sd_src:"(.+?)"', html).group(1)
    file_size_request = requests.get(video_url, stream=True)
    block_size = 1024
    filename = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')
    path = download_path.get()
    with open(os.path.join(path, filename) + '.mp4', 'wb') as f:
        for data in file_size_request.iter_content(block_size):
            f.write(data)
    messagebox.showinfo("HD: Downloaded", "Successfully downloade in " + str(path))


# BROWSE

def Browse():
    download_dir = filedialog.askdirectory(initialdir="YOUR DIR PATH")
    download_path.set(download_dir)


##
Label(root, text="Facebook Video Downloader", font='Helvetica 20 bold', bg="royalblue4", fg="white", relief="flat", pady=3).place(x=10, y=10)
Label(root, text="Enter url :", font='Helvetica 15 bold', bg='royalblue4', fg='white').place(x=20, y=120)
input_url = StringVar()
video_url = Entry(root, textvariable=input_url, width=40, font="Helvetica 15")
video_url.place(x=125, y=120)

Label(root, text="Choose Browse path", font='Helvetica 15 bold', bg='royalblue4', fg='white').place(x=20, y=165)
download_path = StringVar()
Button(root, text="Browse Path", font="Helvetica 15", command=Browse).place(x=240, y=160)
Entry(root, textvariable=download_path, width=40, font='Helvetica 15 bold').place(x=80, y=220)

# crete a button for HD and Sd  download
Button(root, text="Download HD", font="Helvetica 15 ", command=download_hd).place(x=110, y=270)
Button(root, text="Download SD", font="Helvetica 15 ", command=download_sd).place(x=355, y=270)


# Download details
details = Label(root, font='Helvetica 15 bold', relief="solid", padx=5, pady=5)
details.place(x=260, y=350)

root.mainloop()
