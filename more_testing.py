from tkinter import ttk
from tkinter import *
from tkinter.ttk import *

root = Tk()
root.geometry('1920x1080')
ttk.Style().configure('TLabelframe',background='black')
l = ttk.Labelframe(root,text="bob",width='50',height='50')
l.place(x=5,y=5)
root.mainloop()