import tkinter as tk
import tkinter.font as tkFont
from tkinter import *


class App:
    def __init__(self, root):
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

        ft = tkFont.Font(family='Times', size=48)

        Display1 = tk.Label(root, text="L1", font=ft)
        Display1.place(x=5, y=620, width=142, height=50)

        Display2 = tk.Label(root, text="L2", font=ft)
        Display2.place(x=5 + 142, y=620, width=142, height=50)

        Display3 = tk.Label(root, text="L3", font=ft)
        Display3.place(x=5 + 2 * 142, y=620, width=142, height=50)

        Display4 = tk.Label(root, text="L4", font=ft)
        Display4.place(x=5 + 3 * 142, y=620, width=142, height=50)

        Display5 = tk.Label(root, text="L5", font=ft)
        Display5.place(x=5 + 4 * 142, y=620, width=142, height=50)

        Display6 = tk.Label(root, text="L6", font=ft)
        Display6.place(x=5 + 5 * 142, y=620, width=142, height=50)

        Display7 = tk.Label(root, text="L7", font=ft)
        Display7.place(x=5 + 6 * 142, y=620, width=142, height=50)

        Display8 = tk.Label(root, text="L8", font=ft)
        Display8.place(x=5 + 7 * 142, y=620, width=142, height=50)

        Display9 = tk.Label(root, text="L9", font=ft)
        Display9.place(x=5 + 8 * 142, y=620, width=142, height=50)

        width = 200
        height = 70
        x = 1050

        DisplayHeight1 = tk.Label(root, text="Tab", font=ft)
        DisplayHeight1.place(x=x, y=0, width=width, height=height)

        DisplayHeight2 = tk.Label(root, text="H2", font=ft)
        DisplayHeight2.place(x=x, y=0 + height, width=width, height=height)

        DisplayHeight3 = tk.Label(root, text="H3", font=ft)
        DisplayHeight3.place(x=x, y=0 + 2 * height, width=width, height=height)

        DisplayHeight4 = tk.Label(root, text="H4", font=ft)
        DisplayHeight4.place(x=x, y=0 + 3 * height, width=width, height=height)

        DisplayHeight5 = tk.Label(root, text="H5", font=ft)
        DisplayHeight5.place(x=x, y=0 + 4 * height, width=width, height=height)

        DisplayHeight6 = tk.Label(root, text="Black", font=ft)
        DisplayHeight6.place(x=x, y=0 + 5 * height, width=width, height=height)

        DisplayHeight7 = tk.Label(root, text="White", font=ft)
        DisplayHeight7.place(x=x, y=0 + 6 * height, width=width, height=height)

        DisplayHeight8 = tk.Label(root, text="Strobe", font=ft)
        DisplayHeight8.place(x=x, y=0 + 7 * height, width=width, height=height)

        w = Scale(root, from_=100, to=0, width=50, )
        w.place(x=10, y=100, width=120, height=400)
        # print(w.get())


def start():
    root = tk.Tk()
    app = App(root)
    root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
