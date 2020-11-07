import tkinter as tk


def on_keyrelease(event, available_fonts, lb_fonts):
    # get text from entry
    value = event.widget.get()
    value = value.strip().lower()

    # get font from test_list
    if value == '':
        font = available_fonts
    else:
        font = []
        for item in available_fonts:
            if value in item.lower():
                font.append(item)

    # update font in listbox
    lb_fonts_update(font, lb_fonts)


def lb_fonts_update(font, lb_fonts):
    # delete previous font
    lb_fonts.delete(0, 'end')

    # sorting font
    fonts = font

    # put new font
    for font in fonts:
        lb_fonts.insert(tk.END, font)


def on_select(event, lb2, temp_selected):
    # display element selected on list
    if event.widget.curselection():
        curr = event.widget.get(event.widget.curselection())
        temp_selected.set(curr)
        lb2.config(text=f'Selected font: {curr}', font=(f'{curr}', 15))
