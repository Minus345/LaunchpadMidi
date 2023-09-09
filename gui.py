import tkinter as tk
import tkinter.font as tkFont
import yaml
from time import strftime
from tkinter import *

global root, TimeLable


def time():
    global TimeLable
    string = strftime('%H:%M:%S')
    TimeLable.config(text=string)
    TimeLable.after(1000, time)


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

    Display1 = tk.Label(root, text=configFile['fader']['a'], font=ft)
    Display1.place(x=5, y=620, width=142, height=50)

    Display2 = tk.Label(root, text=configFile['fader']['b'], font=ft)
    Display2.place(x=5 + 142, y=620, width=142, height=50)

    Display3 = tk.Label(root, text=configFile['fader']['c'], font=ft)
    Display3.place(x=5 + 2 * 142, y=620, width=142, height=50)

    Display4 = tk.Label(root, text=configFile['fader']['d'], font=ft)
    Display4.place(x=5 + 3 * 142, y=620, width=142, height=50)

    Display5 = tk.Label(root, text=configFile['fader']['e'], font=ft)
    Display5.place(x=5 + 4 * 142, y=620, width=142, height=50)

    Display6 = tk.Label(root, text=configFile['fader']['f'], font=ft)
    Display6.place(x=5 + 5 * 142, y=620, width=142, height=50)

    Display7 = tk.Label(root, text=configFile['fader']['g'], font=ft)
    Display7.place(x=5 + 6 * 142, y=620, width=142, height=50)

    Display8 = tk.Label(root, text=configFile['fader']['h'], font=ft)
    Display8.place(x=5 + 7 * 142, y=620, width=142, height=50)

    width = 200
    height = 70
    x = 1050

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

    # w = Scale(root, from_=100, to=0, width=50, )
    # w.place(x=10, y=100, width=120, height=400)

    Button1 = tk.Button(root, text=configFile['button']['a'], borderwidth=10)
    Button1.place(x=20, y=50, width=150, height=150)

    Button2 = tk.Button(root, text=configFile['button']['b'], borderwidth=10)
    Button2.place(x=20 + 180, y=50, width=150, height=150)

    Button3 = tk.Button(root, text=configFile['button']['c'], borderwidth=10)
    Button3.place(x=20 + 2 * 180, y=50, width=150, height=150)

    Button4 = tk.Button(root, text=configFile['button']['d'], borderwidth=10)
    Button4.place(x=20 + 3 * 180, y=50, width=150, height=150)

    Button5 = tk.Button(root, text=configFile['button']['e'], borderwidth=10)
    Button5.place(x=20 + 4 * 180, y=50, width=150, height=150)

    Button6 = tk.Button(root, text=configFile['button']['f'], borderwidth=10)
    Button6.place(x=20 + 5 * 180, y=50, width=150, height=150)

    global TimeLable
    TimeLable = Label(root, font=('calibri', 70, 'bold'),
                      foreground='black')

    TimeLable.place(x=20, y=450)
    time()


def start():
    init()
    root.mainloop()


if __name__ == "__main__":
    init()
    root.mainloop()
