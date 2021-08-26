from tkinter import *
from tkinter import filedialog, messagebox
import requests
import re
from datetime import datetime
import os

# windows
root = Tk()
root.geometry('600x600')
root.resizable(0, 0)
root.title("Facebook Video Downloader")
root.config(bg="royalblue3")


# download hd
def download_hd():
    url = input_url.get()
    if "www.facebook.com" in url:
        url = url
    else:
        try:
            url = requests.head(url).headers['location']
        except:
            details.config(text="Error : Not a facebook link")
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
    messagebox.showinfo("HD: Downloaded", "Successfully downloaded in " + str(path))


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
Label(root, text="FACEBOOK VIDEO DOWNLOADER", font='arial 20 bold', bg="white", fg="black", relief="solid", pady=3).pack(pady=20)
Label(root, text="Enter the video url :", font='arial 15 bold', bg='white', fg='black').pack(pady=2)
input_url = StringVar()
video_url = Entry(root, textvariable=input_url, width=50, font="20")
video_url.pack(pady=10)

Label(root, text="Choose Browse path", font='arial 15 bold', bg='white', fg='black').pack(pady=3)
download_path = StringVar()
Button(root, text="Browse Path", font="Helvetica 15 bold", command=Browse).pack(pady=2)
Entry(root, textvariable=download_path, width=40, font='Helvetica 15 bold').pack(pady=5)

# crete a button for HD and Sd  download
Button(root, text="DOWNLOAD HD", font="Helvetica 15 bold", command=download_hd).pack(pady=2)
Button(root, text="DOWNLOAD SD", font="Helvetica 15 bold", command=download_sd).pack(pady=2)

#
details = Label(root, font='arial 15 bold', relief="solid", padx=5, pady=5)
details.pack(pady=10)

root.mainloop()
