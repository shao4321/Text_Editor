from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter import colorchooser
from tkinter import messagebox
from tkinter import font
from tkinter import ttk
import TE_about
import font2
import sqlite3

# Global variables
opened_filepath = None
txt_font_style = 'normal'
txt_font_fam = 'Helvetica'
txt_font_size = 15
txt_bg = 'white'
txt_fg = 'black'
txt_bg_changed = False
txt_fg_changed = False
txt_fs_changed = False
txt_fam_changed = False
txt_fstyle_changed = False

# Create database table for fonts and background color
connect = sqlite3.connect('text.db')
c = connect.cursor()
# c.execute("DROP TABLE attributes")
# c.execute("""CREATE TABLE attributes (
#     file_name TEXT,
#     bg TEXT,
#     font_fam TEXT,
#     font_style TEXT,
#     fg TEXT,
#     f_size INT);
#     """)
# connect.commit()
# connect.close()


# Functions available in TextEditor
def new():
    global opened_filepath
    global txt_font_size
    global txt_bg
    global txt_fg
    global txt_font_fam
    global txt_font_style

    # Set all attributes back to default
    opened_filepath = None
    txt_font_style = 'normal'
    txt_font_fam = 'Helvetica'
    txt_font_size = 15
    txt_bg = 'white'
    txt_fg = 'black'

    txt_edit.delete("1.0", END)
    txt_edit.config(state='normal')
    txt_edit.config(bg=txt_bg)
    txt_edit.config(fg=txt_fg)
    txt_edit.config(font=(txt_font_fam, txt_font_size, txt_font_style))
    btn_save.config(state='normal')
    btn_save_as.config(state='normal')

    fileMenu.entryconfig('Save', state='normal')
    fileMenu.entryconfig('Save as', state='normal')
    edit_menu.entryconfig('Change text background color', state='normal')
    edit_menu.entryconfig('Change font color', state='normal')
    edit_menu.entryconfig('Change font type', state='normal')

    root.title(f'Simple Text Editor')


def open_file():
    """Open a file for editing."""

    # Declaring global variable to edit opened file path and text variables
    global opened_filepath
    global txt_font_style
    global txt_font_fam
    global txt_font_size
    global txt_bg
    global txt_fg

    # Retrieving the file path of the text file to be opened
    opened_filepath = askopenfilename(initialdir="/C:/",
                                      title="Select file",
                                      filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

    # Cancel command if no file path is retrieved
    if not opened_filepath:
        return

    # Enable the text field
    txt_edit.config(state='normal')
    txt_edit.delete("1.0", END)

    # Set the attributes back to default first
    txt_bg = 'white'
    txt_fg = 'black'
    txt_font_size = 15
    txt_font_fam = 'Helvetica'
    txt_font_style = 'normal'
    txt_edit.config(bg=txt_bg)
    txt_edit.config(fg=txt_fg)
    txt_edit.config(font=(txt_font_fam, txt_font_size, txt_font_style))

    # Retrieving the attributes data for this file
    c.execute("SELECT * FROM attributes WHERE file_name=:filename", {'filename': opened_filepath})
    records = c.fetchone()

    # Apply the attributes if any
    bg = records[1]
    f_fam = records[2]
    f_style = records[3]
    fg = records[4]
    f_size = records[5]
    if bg:
        txt_bg = bg
        txt_edit.config(bg=txt_bg)
    if fg:
        txt_fg = fg
        txt_edit.config(fg=txt_fg)
    if f_fam:
        txt_font_fam = f_fam
    if f_size:
        txt_font_size = f_size
    if f_style:
        txt_font_style = f_style
    txt_edit.config(font=(txt_font_fam, txt_font_size, txt_font_style))

    # Read the contents from the file to text editor
    with open(opened_filepath, 'r') as input_file:
        opened_text = input_file.read().strip('\n')
        txt_edit.insert(END, opened_text)

    # Save and save_as button is enabled
    btn_save.config(state='normal')
    btn_save_as.config(state='normal')
    fileMenu.entryconfig('Save', state='normal')
    fileMenu.entryconfig('Save as', state='normal')
    edit_menu.entryconfig('Change text background color', state='normal')
    edit_menu.entryconfig('Change font color', state='normal')
    edit_menu.entryconfig('Change font type', state='normal')

    root.title(f'Simple Text Editor - {opened_filepath}')


def save_file(filepath):
    """Save the current opened file"""

    global txt_bg_changed
    global txt_fg_changed
    global txt_fs_changed
    global txt_fam_changed
    global txt_fstyle_changed

    # File already exists
    if filepath:
        # Overwrite the existing file
        ans = messagebox.askyesno('Warning', 'Do you want to overwrite existing file?')
        if ans:
            with open(filepath, "w") as output_file:
                text = txt_edit.get("1.0", END)
                output_file.write(text)

            # Update attributes into database if modified
            with connect:
                if txt_bg_changed:
                    c.execute("UPDATE attributes SET bg=:bg WHERE file_name=:filename;",
                              {'bg': txt_bg, 'filename': filepath})
                    txt_bg_changed = False
                if txt_fg_changed:
                    c.execute("UPDATE attributes SET fg=:fg WHERE file_name=:filename;",
                              {'fg': txt_fg, 'filename': filepath})
                    txt_fg_changed = False
                if txt_fs_changed:
                    c.execute("UPDATE attributes SET f_size=:f_size WHERE file_name=:filename;",
                              {'f_size': txt_font_size, 'filename': filepath})
                    txt_fs_changed = False
                if txt_fam_changed:
                    c.execute("UPDATE attributes SET font_fam=:f_fam WHERE file_name=:filename;",
                              {'f_fam': txt_font_fam, 'filename': filepath})
                    txt_fam_changed = False
                if txt_fstyle_changed:
                    c.execute("UPDATE attributes SET font_style=:f_style WHERE file_name=:filename;",
                              {'f_style': txt_font_style, 'filename': filepath})
                    txt_fstyle_changed = False
        else:
            return
    else:
        # File don't exist
        save_as_file()


def save_as_file():
    """Save the current file as a new file."""

    global opened_filepath
    global txt_bg_changed
    global txt_fg_changed
    global txt_fs_changed
    global txt_fam_changed
    global txt_fstyle_changed

    text = txt_edit.get("1.0", END).strip('\n')
    # Retrieving the file path to save the text file
    filepath = asksaveasfilename(
        initialfile=text,
        defaultextension="txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])

    if not filepath:
        return

    with open(filepath, "w") as output_file:
        output_file.write(text)

    # Set current opened file
    opened_filepath = filepath
    root.title(f"Simple Text Editor - {opened_filepath}")

    # Record new file into database and it's attributes
    with connect:
        c.execute("INSERT INTO attributes('file_name') VALUES(:filename)",
                  {'filename': opened_filepath})

        # Update attributes into database if modified from default
        if txt_bg_changed:
            c.execute("UPDATE attributes SET bg=:bg WHERE file_name=:filename;",
                      {'bg': txt_bg, 'filename': opened_filepath})
            txt_bg_changed = False
        if txt_fg_changed:
            c.execute("UPDATE attributes SET fg=:fg WHERE file_name=:filename;",
                      {'fg': txt_fg, 'filename': opened_filepath})
            txt_fg_changed = False
        if txt_fs_changed:
            c.execute("UPDATE attributes SET f_size=:f_size WHERE file_name=:filename;",
                      {'f_size': txt_font_size, 'filename': opened_filepath})
            txt_fs_changed = False
        if txt_fam_changed:
            c.execute("UPDATE attributes SET font_fam=:f_fam WHERE file_name=:filename;",
                      {'f_fam': txt_font_fam, 'filename': opened_filepath})
            txt_fam_changed = False
        if txt_fstyle_changed:
            c.execute("UPDATE attributes SET font_style=:f_style WHERE file_name=:filename;",
                      {'f_style': txt_font_style, 'filename': opened_filepath})
            txt_fstyle_changed = False


def run_save_alert(filepath):
    # Retrieving the text from textbox
    txtEdit = txt_edit.get("1.0", END)
    txtEdit = txtEdit.strip('\n')

    with open(filepath, 'r') as input_file:
        open_text = input_file.read().strip('\n')

    if open_text != txtEdit or txt_bg_changed or txt_fg_changed or txt_fs_changed:
        alert = messagebox.askyesnocancel("Save", "File edited, do you want to save before quitting?")
        if alert:
            save_file(filepath)
            connect.close()
            root.destroy()
        elif alert is False:
            connect.close()
            root.destroy()
        else:
            return
    else:
        connect.close()
        root.destroy()


def on_closing():
    """Remind user to save when file is edited"""
    if not opened_filepath:
        if txt_edit['state'] == 'disabled':
            connect.close()
            root.destroy()
            return
        if txt_edit.get("1.0", END):
            alert = messagebox.askyesnocancel("Save", "Do you want to save as new file before quitting?")
            if alert:
                save_as_file()
            elif alert is None:
                return
        connect.close()
        root.destroy()
    run_save_alert(opened_filepath)


def change_bg_color():
    global txt_bg
    global txt_bg_changed
    txt_bg = colorchooser.askcolor()[-1]
    txt_edit.config(bg=txt_bg)
    txt_bg_changed = True


def change_font_color():
    global txt_fg
    global txt_fg_changed
    txt_fg = colorchooser.askcolor()[-1]
    txt_edit.config(fg=txt_fg)
    txt_fg_changed = True


def change_font_type():
    global txt_font_fam
    global txt_font_size
    global txt_font_style
    prev_font_fam = txt_font_fam

    # Create new window for font
    fontRoot = Tk()
    fontRoot.title('Font Types')
    fontRoot.iconbitmap('TextIco.ico')

    fontRoot.after(1, lambda: fontRoot.focus_force())

    app_width2 = 600
    app_height2 = 500

    screen_width2 = fontRoot.winfo_screenwidth()
    screen_height2 = fontRoot.winfo_screenheight()

    x2 = (screen_width2 / 2) - (app_width2 / 2)
    y2 = (screen_height2 / 2) - (app_height2 / 2)
    fontRoot.geometry(f"{app_width2}x{app_height2}+{int(x2)}+{int(y2)}")

    fontRoot.rowconfigure([i for i in range(7)], minsize=60, weight=1)
    fontRoot.columnconfigure([i for i in range(3)], minsize=50, weight=1)
    fontRoot.minsize(600, 500)

    # Retrieving all font types data
    available_fonts = font.families()

    # Function to change font on txt edit page
    def changeFont():
        global txt_font_fam
        global txt_fam_changed
        global txt_font_size
        global txt_fs_changed
        global txt_font_style
        global txt_fstyle_changed

        # Error checking
        if not cb_FontSize.get().strip() or not cb_FontSize.get().isnumeric():
            messagebox.showerror('Error', 'Please enter an integer value for Font Size')
            fontRoot.after(1, lambda: fontRoot.focus_force())
            return "break"

        # Retrieving font type/size chosen
        selection = temp_selected.get()
        if selection:
            txt_font_fam = selection
            txt_fam_changed = True
        if txt_font_size != cb_FontSize.get():
            txt_font_size = cb_FontSize.get()
            txt_fs_changed = True
        prev_txt_font_style = txt_font_style
        if style1.get():
            if style2.get() and style3.get():
                txt_font_style = 'bold italic underline'
            elif style2.get() and not style3.get():
                txt_font_style = 'bold italic'
            elif not style2.get() and style3.get():
                txt_font_style = 'bold underline'
            else:
                txt_font_style = 'bold'
        elif style2.get():
            if not style1.get() and style3.get():
                txt_font_style = 'italic underline'
            else:
                txt_font_style = 'italic'
        elif style3.get():
            txt_font_style = 'underline'
        if prev_txt_font_style != txt_font_style:
            txt_fstyle_changed = True
        txt_edit.config(font=(txt_font_fam, txt_font_size, txt_font_style))
        fontRoot.destroy()

    # Widgets for font types
    lb1 = Label(fontRoot, text='Pick a font family', font=('Helvetica', 15, 'underline'), justify=LEFT)
    current_font = Label(fontRoot, text=f'Current font:\n{prev_font_fam}',
                         font=(prev_font_fam, 10), wraplength=130, justify=RIGHT)
    lb2 = Label(fontRoot, text='Font not selected', font=15)
    lbFonts = Listbox(fontRoot)
    lb3 = Label(fontRoot, text='Search font:', font=('Helvetica', 15))
    font_query = Entry(fontRoot, font=('Helvetica', 20))

    # Widgets for font sizes
    lb_FontSize = Label(fontRoot, text='Pick a font size', font=('Helvetica', 12, 'underline'))
    fontSizes = [i for i in range(1, 100)]
    cb_FontSize = ttk.Combobox(fontRoot, font=('Helvetica', 15, 'bold'), width=5, value=fontSizes)
    cb_FontSize.set(txt_font_size)

    # Widgets for font styles
    lb_FontStyle = Label(fontRoot, text='Pick a font style', font=('Helvetica', 15, 'underline'))
    if 'bold' in txt_font_style:
        style1 = IntVar(fontRoot, value=1)
    else:
        style1 = IntVar(fontRoot)
    if 'italic' in txt_font_style:
        style2 = IntVar(fontRoot, value=1)
    else:
        style2 = IntVar(fontRoot)
    if 'underline' in txt_font_style:
        style3 = IntVar(fontRoot, value=1)
    else:
        style3 = IntVar(fontRoot)
    chk1_FS = Checkbutton(fontRoot, text='bold', font=('Helvetica', 15, 'bold'),
                          variable=style1, onvalue=1, offvalue=0)
    chk2_FS = Checkbutton(fontRoot, text='italic', font=('Helvetica', 15, 'italic'),
                          variable=style2, onvalue=1, offvalue=0)
    chk3_FS = Checkbutton(fontRoot, text='underline', font=('Helvetica', 15, 'underline'),
                          variable=style3,  onvalue=1, offvalue=0)

    # Button to apply the chosen font and update changes
    font_btn = Button(fontRoot, text="Choose Font", font=('Helvetica', 15))
    font_btn.bind("<1>", lambda e: changeFont())

    # Filtering the list based on search and preview
    font_query.bind('<KeyRelease>', lambda e: font2.on_keyrelease(e, available_fonts, lbFonts))
    font2.lbFonts_update(available_fonts, lbFonts)
    lbFonts.bind('<Double-Button-1>', lambda e: changeFont())
    lbFonts.bind('<Return>', lambda e: changeFont())
    temp_selected = StringVar()
    lbFonts.bind('<<ListboxSelect>>', lambda e: font2.on_select(e, lb2, temp_selected))
    cb_FontSize.bind('<Return>', lambda e: changeFont())

    # Grid up the font types widgets
    row = 0
    lb1.grid(row=row, column=0, sticky='w', pady=5, padx=5)
    current_font.grid(row=row, column=1, sticky='e', pady=5, padx=5)
    row += 1
    lb2.grid(row=row, column=0, columnspan=2, sticky='ew', pady=5)
    row += 1
    lbFonts.grid(row=row, column=0, rowspan=2, columnspan=2, sticky='ew', pady=5)
    row += 2
    lb3.grid(row=row, column=0, columnspan=2, sticky='w', pady=5)
    row += 1
    font_query.grid(row=row, column=0, columnspan=2, sticky='ew')
    row += 1
    font_btn.grid(row=row, column=0, columnspan=2, sticky='nsew', pady=5)

    # Grid up the font sizes widgets
    lb_FontSize.grid(row=0, column=2, sticky='n', pady=5, padx=5)
    cb_FontSize.grid(row=1, column=2, rowspan=1, sticky='n', pady=5, padx=5)

    # Grid up the font styles widgets
    lb_FontStyle.grid(row=3, column=2, sticky='n', pady=5, padx=5)
    chk1_FS.grid(row=4, column=2, sticky='n', pady=5, padx=5)
    chk2_FS.grid(row=5, column=2, sticky='n', pady=5, padx=5)
    chk3_FS.grid(row=6, column=2, sticky='n', pady=5, padx=5)


def about_app():
    TE_about.about_app()


root = Tk()
root.title('Simple Text Editor')
root.iconbitmap('TextIco.ico')

app_width = 700
app_height = 700

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width / 2) - (app_width / 2)
y = (screen_height / 2) - (app_height / 2)
root.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")

root.rowconfigure(0, minsize=500, weight=1)
root.columnconfigure(1, minsize=500, weight=1)
root.minsize(500, 500)

txt_edit = Text(root, font=(txt_font_fam, txt_font_size), bg=txt_bg, fg=txt_fg, state='disabled')
txt_edit.bind('<Control-n>', lambda e: new())
txt_edit.bind('<Control-o>', lambda e: open_file())
txt_edit.bind('<Control-s>', lambda e: save_file(opened_filepath))
txt_edit.bind('<Control-Shift-S>', lambda e: save_as_file())
txt_edit.bind('<Escape>', lambda e: on_closing())

btn_frame = Frame(root)
btn_new = Button(btn_frame, text='New', cursor='hand2', command=new)
btn_open = Button(btn_frame, text='Open', cursor='hand2', command=open_file)
btn_save = Button(btn_frame, text='Save', state='disabled', cursor='hand2', command=lambda: save_file(opened_filepath))
btn_save_as = Button(btn_frame, text='Save as..', state='disabled', cursor='hand2', command=save_as_file)

# Create Menu Bar
menuBar = Menu(root)
root.config(menu=menuBar)

fileMenu = Menu(menuBar, tearoff=0, font=('Times', 10))
fileMenu.add_command(label="New", accelerator='Ctrl-n', command=new)
fileMenu.add_command(label="Open", accelerator='Ctrl-o', command=open_file)
fileMenu.add_command(label="Save", accelerator='Ctrl-s', state='disabled', command=lambda: save_file(opened_filepath))
fileMenu.add_command(label="Save as", accelerator='Ctrl-Shift-s', state='disabled', command=save_as_file)
fileMenu.add_separator()
fileMenu.add_command(label='Exit (Esc)', command=on_closing)
menuBar.add_cascade(label="File", menu=fileMenu)

edit_menu = Menu(menuBar, tearoff=0, font=('Times', 10))
edit_menu.add_command(label='Change text background color', state='disabled', command=change_bg_color)
edit_menu.add_command(label='Change font color', state='disabled', command=change_font_color)
edit_menu.add_command(label='Change font type', state='disabled', command=change_font_type)
menuBar.add_cascade(label='Edit', menu=edit_menu)

about = Menu(menuBar, tearoff=0, font=('Times', 10))
about.add_command(label='About app', command=about_app)
menuBar.add_cascade(label='Information', menu=about)

row_counter = 0
btn_new.grid(row=row_counter, column=0, sticky='ew', padx=5, pady=5)
row_counter += 1
btn_open.grid(row=row_counter, column=0, sticky='ew', padx=5, pady=5)
row_counter += 1
btn_save.grid(row=row_counter, column=0, sticky='ew', padx=5, pady=5)
row_counter += 1
btn_save_as.grid(row=row_counter, column=0, stick='ew', padx=5, pady=5)

btn_frame.grid(row=0, column=0, stick='ns')
txt_edit.grid(row=0, column=1, sticky='nsew')

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
