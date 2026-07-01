from tkinter import *
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image, ImageOps

def nextButtonClicked(*args):
    try:
        print("next")
    except ValueError:
        pass

def skipButtonClicked(*args):
    try:
        print("skip")
    except ValueError:
        pass


root = tk.Tk()
root.title("Web builder")

mainframe = ttk.Frame(root, padding=(3, 3, 12, 12))
mainframe.grid(column=0, row=0)

root.resizable(False, False)

image = ImageOps.exif_transpose(Image.open('./testimage.jpg').resize((800, 600)))
currentImage = ImageTk.PhotoImage(image)
imageLabel = ttk.Label(mainframe, image=currentImage).grid(column=0, row=0, columnspan=3, sticky=(W, E))


caption_entry = tk.Text(mainframe, width=20, height=4)
caption_entry.grid(column=0, row=1, columnspan=3, sticky=(W, E))

NextButton = ttk.Button(mainframe, text="Next", command=nextButtonClicked).grid(column=0, row=2, sticky=E)
SkipButton = ttk.Button(mainframe, text="Skip", command=skipButtonClicked).grid(column=1, row=2)
dirvar = StringVar()
directory = ttk.Combobox(mainframe, textvariable=dirvar).grid(column=2, row=2, sticky=W)

directoryCaption_entry = tk.Text(mainframe, height=4)
directoryCaption_entry.grid(column=0, row=3, columnspan=3, sticky=(W, E))


meters = StringVar()



root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
mainframe.columnconfigure(2, weight=1)
for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

caption_entry.focus()

root.mainloop()
