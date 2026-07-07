from tkinter import *
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image, ImageOps
import datetime as dt
import os as OS
import subprocess



listOfPictures = []
result = subprocess.run(['mount'], stdout=subprocess.PIPE)
if "iphone" not in result.stdout.decode("utf-8"):
    try:
        result = subprocess.run(['ifuse', '../iphone'], stdout=subprocess.PIPE)
        print(result.stdout)
    except:
        print("error mounting the camera filesystem.")
        quit()
try:
    result = subprocess.run(['ls', '--full-time', '../iphone/DCIM/101APPLE/'], stdout=subprocess.PIPE)
except:
    print("error getting file list from the camera.")
files = result.stdout.decode("utf-8").split("\n")
for file in files:
    if "JPG" in file:
        file = file.replace('   ',' ')
        file = file.replace('  ',' ')
        fields = file.split(' ')
        fileDate = fields[5].split('-')
        try:
            OS.mkdir("../Pictures/" + fileDate[0])
        except FileExistsError:
            pass
        try:
            OS.mkdir("../Pictures/" + fileDate[0] + "/" + fileDate[1])
        except FileExistsError:
            pass
        try:
            OS.mkdir("../Pictures/" + fileDate[0] + "/" + fileDate[1] + "/" + fileDate[2])
        except FileExistsError:
            pass
        if not OS.path.exists("../Pictures/" + fileDate[0] + "/" + fileDate[1] + "/" + fileDate[2] + "/" + fields[8]):
            listOfPictures.append("../Pictures/" + fileDate[0] + "/" + fileDate[1] + "/" + fileDate[2] + "/" + fields[8])
            try:
                print(fields[8])
                result = subprocess.run(['cp', '../iphone/DCIM/101APPLE/' + fields[8], "../Pictures/" + fileDate[0] + "/" + fileDate[1] + "/" + fileDate[2] + "/" + fields[8]], stdout=subprocess.PIPE)
            except:
                print("error copying file from camera.")
if len(listOfPictures) == 0:
    print("no new images. Nothing to do!")
    quit()

currentPicture = 0

root = tk.Tk()
root.title("Web builder")

mainframe = ttk.Frame(root, padding=(3, 3, 12, 12))
mainframe.grid(column=0, row=0)

root.resizable(False, False)

image = ImageOps.exif_transpose(Image.open(listOfPictures[currentPicture]).resize((800, 600)))
currentImage = ImageTk.PhotoImage(image)
imageLabel = ttk.Label(mainframe, image=currentImage)
imageLabel.grid(column=0, row=0, columnspan=3, sticky=(W, E))

caption_entry = tk.Text(mainframe, width=20, height=4)
caption_entry.grid(column=0, row=1, columnspan=3, sticky=(W, E))

def nextButtonClicked(*args):
    try:
        print("next")
    except ValueError:
        pass

def skipButtonClicked(*args):
    global currentPicture
    global listOfPictures
    global imageLabel
    try:
        currentPicture = currentPicture + 1
        if currentPicture < len(listOfPictures):
            image = ImageOps.exif_transpose(Image.open(listOfPictures[currentPicture]).resize((800, 600)))
            currentImage = ImageTk.PhotoImage(image)
            imageLabel.configure(image=currentImage)
            imageLabel.image = currentImage
    except ValueError:
        pass

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
