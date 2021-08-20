from tkinter import *
from PIL import Image,ImageTk

#creating a window
root=Tk()
root.title("Facebook Video Downloader")
root.iconbitmap("fb1.ico")
root.attributes('-alpha',0.9)

#setting the maximun and minimum size of the window
root.maxsize(width=600,height=500)
root.minsize(width=600,height=500)


label_0 =Label(root,text="Login System",bg="crimson",fg="black",width=35,font=("Comic Sans MS",20))
label_0.place(x=20,y=20)




root.mainloop()
