from queue import Queue

import time
import tkinter as tk
import tkinter.font as tkFont
from threading import Thread
from tkinter import *
import pandas as pd
import yaml

import main
from createConfig import createConfig

global root, text, canvas, DisplayHeight1, DisplayHeight2, DisplayHeight3, DisplayHeight4, DisplayHeight5, DisplayHeight6, DisplayHeight7, DisplayHeight8, q


def init():
    global root
    root = tk.Tk()
    # setting title
    root.title("undefined")
    # setting window size
    width = 1280
    height = 697

    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    root.geometry(alignstr)

    # root.resizable(width=False, height=False)

    GLabel_572 = tk.Label(root)
    GLabel_572["anchor"] = "center"
    ft = tkFont.Font(family='Times', size=18)
    GLabel_572["font"] = ft
    GLabel_572["fg"] = "#333333"
    GLabel_572["justify"] = "center"
    GLabel_572["text"] = "DMX Joker Extenstion for Lauchpad"
    GLabel_572.place(x=0, y=0, width=1278, height=30)

    with open('config.yml', 'r') as file:
        configFile = yaml.safe_load(file)

    ft = tkFont.Font(family='Times', size=48)
    global text, canvas, DisplayHeight1, DisplayHeight2, DisplayHeight3, DisplayHeight4, DisplayHeight5, DisplayHeight6, DisplayHeight7, DisplayHeight8
    text = []
    canvas = Canvas()
    canvas.place(x=0, y=200, width=1500, height=500)
    text.append(canvas.create_text(50, 250, text="a", angle=90, font=ft))
    text.append(canvas.create_text(50 + 142, 250, text="b", angle=90, font=ft))
    text.append(canvas.create_text(50 + 2 * 142, 250, text="c", angle=90, font=ft))
    text.append(canvas.create_text(50 + 3 * 142, 250, text="d", angle=90, font=ft))
    text.append(canvas.create_text(50 + 4 * 142, 250, text="e", angle=90, font=ft))
    text.append(canvas.create_text(50 + 5 * 142, 250, text="f", angle=90, font=ft))
    text.append(canvas.create_text(50 + 6 * 142, 250, text="f", angle=90, font=ft))
    text.append(canvas.create_text(50 + 7 * 142, 250, text="h", angle=90, font=ft))

    width = 200
    height = 70
    x = 1080

    DisplayHeight1 = tk.Label(root, text=configFile['rightbuttons']['a'], font=ft)
    DisplayHeight1.place(x=x, y=0, width=width, height=height)

    DisplayHeight2 = tk.Label(root, text=configFile['rightbuttons']['b'], font=ft)
    DisplayHeight2.place(x=x, y=0 + height, width=width, height=height)

    DisplayHeight3 = tk.Label(root, text=configFile['rightbuttons']['c'], font=ft)
    DisplayHeight3.place(x=x, y=0 + 2 * height, width=width, height=height)

    DisplayHeight4 = tk.Label(root, text=configFile['rightbuttons']['d'], font=ft)
    DisplayHeight4.place(x=x, y=0 + 3 * height, width=width, height=height)

    DisplayHeight5 = tk.Label(root, text=configFile['rightbuttons']['e'], font=ft)
    DisplayHeight5.place(x=x, y=0 + 4 * height, width=width, height=height)

    DisplayHeight6 = tk.Label(root, text=configFile['rightbuttons']['f'], font=ft)
    DisplayHeight6.place(x=x, y=0 + 5 * height, width=width, height=height)

    DisplayHeight7 = tk.Label(root, text=configFile['rightbuttons']['g'], font=ft)
    DisplayHeight7.place(x=x, y=0 + 6 * height, width=width, height=height)

    DisplayHeight8 = tk.Label(root, text=configFile['rightbuttons']['h'], font=ft)
    DisplayHeight8.place(x=x, y=0 + 7 * height, width=width, height=height)

    Button1 = tk.Button(root, text=configFile['button']['a'], borderwidth=10, command=updateTextInGUI)
    Button1.place(x=20, y=50, width=150, height=150)

    Button2 = tk.Button(root, text=configFile['button']['b'], borderwidth=10, command=updateFader)
    Button2.place(x=20 + 180, y=50, width=150, height=150)

    Button3 = tk.Button(root, text=configFile['button']['c'], borderwidth=10)
    Button3.place(x=20 + 2 * 180, y=50, width=150, height=150)

    Button4 = tk.Button(root, text=configFile['button']['d'], borderwidth=10)
    Button4.place(x=20 + 3 * 180, y=50, width=150, height=150)

    Button5 = tk.Button(root, text=configFile['button']['e'], borderwidth=10)
    Button5.place(x=20 + 4 * 180, y=50, width=150, height=150)

    Button6 = tk.Button(root, text=configFile['button']['f'], borderwidth=10)
    Button6.place(x=20 + 5 * 180, y=50, width=150, height=150)
    updateTextInGUI()


def updateTextInGUI():
    with open('config.yml', 'r') as file:
        configFile = yaml.safe_load(file)
    alpha = ["a", "b", "c", "d", "e", "f", "g", "h"]
    df = pd.read_excel("data/tk-colours.xlsx")  # Path of the file.
    colours = df['Color Name'].values.tolist()
    # print(colours)
    for i in range(8):
        if configFile['fadercolourGUI'][alpha[i]] not in colours:
            print("wrong colour in row ", alpha.__getitem__(i))

    for i in range(8):
        canvas.itemconfigure(text[i], text=configFile['fader'][alpha[i]], fill=configFile['fadercolourGUI'][alpha[i]])
    DisplayHeight1.config(text=configFile['rightbuttons']['a'])
    DisplayHeight2.config(text=configFile['rightbuttons']['b'])
    DisplayHeight3.config(text=configFile['rightbuttons']['c'])
    DisplayHeight4.config(text=configFile['rightbuttons']['d'])
    DisplayHeight5.config(text=configFile['rightbuttons']['e'])
    DisplayHeight6.config(text=configFile['rightbuttons']['f'])
    DisplayHeight7.config(text=configFile['rightbuttons']['g'])
    DisplayHeight8.config(text=configFile['rightbuttons']['h'])
    root.update_idletasks()


def updateFader():
    q.put("updateFader")

def start():
    print("Starting")
    global q
    q = Queue()
    main.checkStart()
    thread1 = Thread(target=main.startMidi, daemon=True, args=(q, ))
    thread1.start()
    print("starting gui")
    init()
    root.mainloop()


if __name__ == "__main__":
    init()
    root.mainloop()
