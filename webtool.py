from tkinter import *
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image, ImageOps
import datetime as dt
import os as OS
import subprocess



listOfPictures = []
directoriesToIgnore = [
".trellix",
"7VJZWPaTXqhtCV8sWoZ7zkKveJjDvIRDwzK7WVyx4TYr5mIx9Fj1hJcwiAQIWZrpyegBglz6ieFy3f",
"arduino",
"blog_archive",
"cgi-bin",
"chM2lQFWjXlKc82FBGFYreyJ6TCcHX3kla6gNh6HvRxKsvaHrbwjru5VDJZZhAdFvVjsB",
"cones",
"crane",
"dhiAKrrnombUyXIQoevTdT9f16yBcE6W5NamOVH3kXIBS5L7sufWs5w5AEm5",
"files",
"Friends",
"gallery",
"GfRenejRbJy",
"HNiGuPwM66sfNj",
"holga",
"images",
"intensifier",
"labels",
"lego",
"logging",
"logs",
"moah",
"nqkz4z2qW2pT2JrIJhggXQBpE49fCjhVaMj6UEbt8uLgU3kHBmwvpiWq0vW",
"oodle",
"Oppopls",
"plans",
"projects",
"restoreBair",
"reverser",
"roadster",
"stats",
"tav",
"trains",
"uploads",
"V04jHhedD5ce1zGJ59uAUVmrmvaSjyDzFUIuGiJYi5pJybUy8wmdHplIUDlchGbg5zB7h4qALnhoWHCWLL",
"vero",
"Vero40",
"vero_mike",
"v-web"
]

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

dirList = OS.listdir('../website/public_html')
dirsOnly = []
for d in dirList:
    if not OS.path.isfile("../website/public_html"+'/' + d):
        if d not in directoriesToIgnore:
            dirsOnly.append(d)
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


def skipButtonClicked():
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

SkipButton = ttk.Button(mainframe, text="Skip", command=skipButtonClicked).grid(column=1, row=2)

currentDir = StringVar()
cmb = ttk.Combobox(mainframe, values=dirsOnly, width=80, textvariable=currentDir).grid(column=2, row=2, sticky=W, columnspan=2)
directoryCaption_entry = tk.Text(mainframe, height=4)
directoryCaption_entry.grid(column=0, row=3, columnspan=3, sticky=(W, E))

def nextButtonClicked():
    currentCaption = caption_entry.get("1.0",END)
    if currentCaption[-1] == '\n':
        currentCaption = currentCaption[0:-1]
    print("caption = ", currentCaption, " len = ", len(currentCaption))
    if len(currentCaption) > 1:
        if len(currentDir.get()):
            print("folder = ", currentDir.get())
            if not currentDir.get() in dirsOnly:
                print("new directory")
                try:
                    OS.mkdir("../website/public_html/" + currentDir.get())
                except:
                    print("failed to make " "../website/public_html/" + currentDir.get())
                    quit()
                currentNewIndexEntry = directoryCaption_entry.get("1.0",END)
                if currentNewIndexEntry[-1] == '\n':
                    currentNewIndexEntry = currentNewIndexEntry[0:-1]
                if len(currentNewIndexEntry) > 1:
                    print("new index entry: ", currentNewIndexEntry)
                    with open("../website/public_html/index.html", "r") as inFile:
                        lines = inFile.readlines()
                        print(lines)
                        lineNumber = 0
                        for line in lines:
                            if "<!-- webtool insert point -->" in line:
                                print("marker line found")
                                lines.insert(lineNumber + 1, '<tr><td align="right"><a href=' + currentDir.get() + "/index.html><img src=" + currentDir.get() + "/" + "thumb_" + OS.path.basename(listOfPictures[currentPicture]).split('/')[-1] + "></td><td>" + currentNewIndexEntry + "</td></tr>\n")
                                break
                            lineNumber = lineNumber + 1
                    outFile = open("../website/public_html/index.html", "w")
                    outFile.writelines(lines)
                    outFile.close()
                    with open("../website/public_html/" + currentDir.get() + "/index.html", "w") as indexFile:
                        indexFile.write("<html>\n<head>\n<title>" + currentDir.get() + "</title>\n</head>\n<body>\n<p>" + currentNewIndexEntry + "\n</p>\n")
                        indexFile.write('\n<table>\n<!-- webtool insert point -->\n<tr><td><a href="' + OS.path.basename(listOfPictures[currentPicture]).split('/')[-1])
                        indexFile.write('"><img src=' + "thumb_" + OS.path.basename(listOfPictures[currentPicture]).split('/')[-1] + '></td><td>')
                        indexFile.write(currentCaption + '</td></tr></table></div></body></html>')
                else:
                    print("Must have an index entry")
        else:
            print("must select a directory")
    else:
        print("must have a caption")
    image.save("../website/public_html/" + currentDir.get() + "/thumb_" + OS.path.basename(listOfPictures[currentPicture]).split('/')[-1])
    try:
        result = subprocess.run(['cp', listOfPictures[currentPicture], "../website/public_html/" + currentDir.get() + "/" + OS.path.basename(listOfPictures[currentPicture]).split('/')[-1]], stdout=subprocess.PIPE)
        print(result.stdout, listOfPictures[currentPicture], "../website/public_html/" + currentDir.get() + "/" + OS.path.basename(listOfPictures[currentPicture]).split('/')[-1])
    except:
        print(result.stdout, "error copying the full size image to website directory.")
        quit()

NextButton = ttk.Button(mainframe, text="Next", command=nextButtonClicked).grid(column=0, row=2, sticky=E)


root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
mainframe.columnconfigure(2, weight=1)
for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

caption_entry.focus()


root.mainloop()
