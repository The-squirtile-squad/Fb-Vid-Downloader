from tkinter import*
from tkinter import messagebox
from tkinter import filedialog
fb=Tk()
# fb.iconbitmap("")
fb.title("facebook video downloader")
fb.geometry("600x500")
fb.config(bg="#3776ab")


def path():
    hello=filedialog.askdirectory()
    


clicked=StringVar()
clicked.set("monday")
name = StringVar(fb, "paste your link here")

#creating GUI
f1=Label(fb, text="Facebook Video Downloader", bg="#3776ab", fg="white", font=("Times", "28", "bold"))
f1.place(x=80, y=100)
f2=Label(fb, text="save your favorite videos from facebook", bg="#3776ab", fg="white", font=("Helvatica", "13", "bold"))
f2.place(x=130, y=150)
e1=Entry(fb, fg="black", font=("Arial"), width=38,justify=CENTER, textvariable=name)
e1.place(x=90, y=180)
b1=Button(fb, text="Download", bg="green", fg="white", font=("Times", "11" ,"bold"))
b1.place(x=450, y=176)
b2=Button(fb, text="select download path",bg="gold3", fg="white", font=("Times", "11", "bold"), command=path)
b2.place(x=100, y=210)
mb=  Menubutton ( fb, text="select video quality", bg="gold3", fg="white", font=("Times", "13", "bold"),relief=RAISED )
mb.place(x=300, y=211)
mb.menu =  Menu ( mb, tearoff = 0 )
mb["menu"] =  mb.menu

HD = IntVar()
SD = IntVar()

mb.menu.add_checkbutton ( label="HD",
                          variable=HD )
mb.menu.add_checkbutton ( label="SD",
                          variable=SD )

mb.place(x=300, y=211)



fb.mainloop()