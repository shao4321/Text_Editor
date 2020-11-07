from tkinter import *


def about_app():
    info = Tk()
    info.title('Simple Text Editor - About')
    info.iconbitmap('TextIco.ico')
    info.after(1, lambda: info.focus_force())

    lbl1 = Label(info, text='This is a simple text editor.\nMain Developer: Lee Shao Wee')
    lbl1.pack(padx=5, pady=5)

    info.mainloop()
