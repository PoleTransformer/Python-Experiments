from tkinter import *

from PIL import Image, ImageTk

root = Tk()
root.title("Periodic Table of Elements")
root.geometry("1920x1080")

class Periodic_Table:
    def __init__(self,master):
        self.image = Image.open("Periodic.png")
        self.image_copy = self.image.copy()
        self.background_image = ImageTk.PhotoImage(self.image)
        self.background = Label(master,image = self.background_image)
        self.background.pack(fill=BOTH,expand=YES)
        self.background.bind("<Configure>",self.resize_image)

    def resize_image(self, event):
        new_width = event.width
        new_height = event.height
        self.image = self.image_copy.resize((new_width,new_height),Image.LANCZOS)
        self.background_image = ImageTk.PhotoImage(self.image)
        self.background.configure(image = self.background_image)

e = Periodic_Table(root)
root.mainloop()
