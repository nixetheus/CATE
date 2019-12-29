import os
import sys
import string
import random
import subprocess
import webbrowser
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog
from tkinter import messagebox

# COLORS
white = "#FFF"
ln_color = None
for_color = None
text_color = None
files_color = None
emb_ter_col1 = None
emb_ter_col2 = None
project_color = None
replace_butt_c = None
line_number_hb = None
file_bar_color = None
main_file_color = None
condition_color = None
top_bottom_color = None
text_editor_color = None
proj_view_men_col = None

colors_array = [ln_color, for_color, text_color, files_color, emb_ter_col1, emb_ter_col2, project_color, replace_butt_c,
                line_number_hb, file_bar_color, main_file_color, condition_color, top_bottom_color, text_editor_color,
                proj_view_men_col]

# GLOBAL VARS
W, H = 1750, 947
screen_width = 0
screen_height = 0
numbered_lines = 0
current_file_width = 0

medium_font = ("Hack", 9)
big_font = ("Hack", 10)
very_big_font = ("Hack", 20)

"""
    SETTINGS FUNCTIONS

    set_
"""


# DONE
def set_values(self, cfw, nl):
    
    global current_file_width, numbered_lines, screen_width, screen_height

    set_colors(self, self.current_color)
    numbered_lines = nl
    current_file_width = cfw
    screen_width = self.root.winfo_screenwidth()
    screen_height = self.root.winfo_screenheight()


# DONE
"""
    FILE MENU FUNCTIONS
    
    set_project:
        Set a new user-chosen folder as the new current project
        
    new_folder:
        Ask the user for the name of a new folder to be created
    
    new_folder_click:
        Using new_folder() method's new folder name, creates a new folder in current project directory
        
    new_file:
        Ask the user for the name of a new file to be created
    
    new_file_click:
        Using new_file() method's new file name, creates a new file in current project directory
        
    open_file:
        Open a user-chosen file as current open file
    
    save_file:
        Save current open file to disk
        
    save_file_as:
        Save current open file to disk as a new file
        
    close_current_file:
        Close current open file
        
    on_closing:
        Deletes every widget and closes the application
        
    printer:
        Prints current open file
"""


# DONE
def set_project(self):

    self.current_project_dir = filedialog.askdirectory()

    if self.current_project_dir:

        # Get content from settings
        settings_file = open("Settings/settings.txt", "r")
        settings = settings_file.readlines()
        settings_file.close()

        # Change current project directory in settings
        settings[0] = "current_project = " + str(self.current_project_dir) + "\n"

        # Now writing mode
        settings_file = open("Settings/settings.txt", "w")
        settings_file.writelines(settings)
        settings_file.close()

        show_project_view(self, text_color, project_color)


# DONE
def new_folder(self):

    # Choose name canvas
    choose_name = tk.Tk()
    choose_name.wm_title("New Folder")
    choose_name.attributes("-toolwindow", 1)
    choose_name.wm_attributes("-topmost", 1)
    choose_name.resizable(width=False, height=False)
    choose_name.focus_force()

    # Set root to center
    can_width = 350
    can_height = 25
    x = (screen_width // 2) - (can_width // 2)
    y = (screen_height // 2) - (can_height // 2) - 50
    choose_name.geometry('%dx%d+%d+%d' % (can_width, can_height, x, y))

    # Main choose canvas
    main_choose_canvas = tk.Frame(choose_name, height=can_height, width=can_width, bg=line_number_hb)
    main_choose_canvas.grid_propagate(False)
    main_choose_canvas.grid()

    new_fol_name = tk.Entry(main_choose_canvas, width=65, insertbackground="white", bg=line_number_hb, relief=tk.FLAT,
                            fg="white", borderwidth=0)
    new_fol_name.grid(row=0, ipady=5, padx=(5, 5))

    choose_name.bind("<FocusOut>", lambda event: choose_name.destroy())
    choose_name.bind('<Return>', lambda event, r=choose_name: new_folder_click(self, r, new_fol_name.get()))

    choose_name.mainloop()


# DONE
def new_folder_click(self, choose_root, folder_name):

    # Destroy name choosing root.
    choose_root.destroy()

    # Error handling
    if folder_name.replace(" ", "") == "":
        messagebox.showerror("Invalid Name", "The name you inserted is not valid")
        return 1

    # Create and set file.
    try:
        os.mkdir(self.current_project_dir + "/" + folder_name)
        show_project_view(self, text_color, project_color)
    except ValueError:
        messagebox.showwarning("Folder Exists", "Cannot overwrite already existing folder")


# DONE
def new_file(self):

    # Choose name canvas
    choose_name = tk.Tk()
    choose_name.wm_title("New File")
    choose_name.attributes("-toolwindow", 1)
    choose_name.wm_attributes("-topmost", 1)
    choose_name.resizable(width=False, height=False)
    choose_name.focus_force()

    # Set root to center
    can_width = 350
    can_height = 25
    x = (screen_width // 2) - (can_width // 2)
    y = (screen_height // 2) - (can_height // 2) - 50
    choose_name.geometry('%dx%d+%d+%d' % (can_width, can_height, x, y))

    # Main choose canvas
    main_choose_canvas = tk.Frame(choose_name, height=can_height, width=can_width, bg=line_number_hb)
    main_choose_canvas.grid_propagate(False)
    main_choose_canvas.grid()

    new_file_name = tk.Entry(main_choose_canvas, width=65, insertbackground="white", bg=line_number_hb, relief=tk.FLAT,
                             fg="white", borderwidth=0)
    new_file_name.grid(row=0, ipady=5, padx=(5, 5))

    choose_name.bind("<FocusOut>", lambda event: choose_name.destroy())
    choose_name.bind('<Return>', lambda event, r=choose_name: new_file_click(self, r, new_file_name.get()))

    choose_name.mainloop()


# DONE
def new_file_click(self, choose_root, filename):

    # Destroy name choosing root.
    choose_root.destroy()

    # Error handling
    if filename.replace(" ", "") == "":
        messagebox.showerror("Invalid Name", "The name you inserted is not valid")
        return 1

    if os.path.splitext(filename)[1] != "" or os.path.splitext(filename)[0] != "":

        if os.path.splitext(filename)[1] not in [".txt", ".py", ".cs", ".c", ".cpp", ".html", ".css", ".js", ".rs"]:

            messagebox.showerror("Invalid Extension", "The file extension you provided is invalid")
            return 1

    else:

        messagebox.showerror("Invalid Name", "The name you inserted is not valid")
        return 1

    # Create and set file.
    try:

        new_f = open(self.current_project_dir + "/" + filename, "w+")
        new_f.close()

        self.current_file = self.current_project_dir + "/" + filename
        self.all_open_files.append(self.current_project_dir + "/" + filename)

        show_project_view(self, text_color, project_color)
        change_text_content(self)

    except FileExistsError:

        messagebox.showwarning("File Exists", "Cannot overwrite already existing file")


# DONE
def open_file(self):

    try:

        filename = filedialog.askopenfilename(
            filetypes=[("All files", ".*"), ("Text files", "*.txt"), ("Python files",  "*.py"),
                       ("C files",  "*.c"),  ("C Sharp files", "*.cs"), ("C++ files",  "*.cpp"),
                       ("HTML files", "*.html"), ("CSS files", "*.css"), ("JavaScript files", "*.js"),
                       ("Rust files", "*.rs"), ("PNG image", ".png"), ("JPEG image", ".jpeg"), ("JPG image", ".jpg")])

        if filename == "":
            messagebox.showerror("404: File not found", "The file you were trying to open can't be found")
        else:

            # Check it's not already opened
            if filename not in self.all_open_files:

                self.current_file = filename
                self.all_open_files.append(filename)

                change_text_content(self)
                show_project_view(self, text_color, project_color)

            else:
                messagebox.showinfo("File already open", "The file you selected is already open")

    except FileNotFoundError:
        messagebox.showerror("404: File not found", "The file you were trying to open can't be found")


# DONE
def save_file(self):

    if self.current_file is not None and os.path.splitext(self.current_file)[1] not in [".png", ".jpeg", ".jpg"]:

        try:

            file = open(self.current_file, "w+")
            lines = self.file_content.get("1.0", 'end-1c')
            file.writelines(lines)
            file.close()

        except FileNotFoundError:
            messagebox.showerror("404: File not found", "The file you were trying to open can't be found")

        except TypeError:
            messagebox.showerror("Error", "Some error occurred. No worries though")

    # Save file each second
    self.root.after(1000, lambda: save_file(self))


# DONE
def save_file_as(self):

    try:

        f = open(filedialog.asksaveasfilename(), "w")
        f.writelines(self.file_content.get(1.0, 'end-1c'))
        f.close()

    except FileNotFoundError:
        pass


# DONE
def close_current_file(self):

    if self.current_file is not None:

        save_file(self)
        self.all_open_files.remove(self.current_file)

        try:
            self.current_file = self.all_open_files[0]
        except IndexError:
            self.current_file = None

        display_file_names(self)
        change_text_content(self)


# DONE
def on_closing(self):

    settings_file = open("Settings/settings.txt", "r")
    settings = settings_file.readlines()
    settings_file.close()

    settings[1] = " ".join(self.all_open_files) + "\n"
    settings[2] = self.current_color + "\n"
    if self.current_file is not None:
        settings[3] = "last_one = " + str(self.all_open_files.index(self.current_file))
    else:
        settings[3] = "last_one = -1"

    settings_file = open("Settings/settings.txt", "w")
    settings_file.writelines(settings)
    settings_file.close()

    for root in self.roots_to_close:

        try:
            root.destroy()
        except tk.TclError:
            pass

    self.root.destroy()


# DONE
def printer(self):

    if self.current_file is not None:

        # On windows
        if "nt" in os.name:
            os.startfile(self.current_file, "print")

        # On Linux
        elif sys.platform.startswith('linux'):
            lpr = subprocess.Popen("/usr/bin/lpr", stdin=subprocess.PIPE)
            lpr.stdin.write(self.file_content.get(0.0, 'end-1c'))


# DONE
"""
    EDIT MENU FUNCTIONS

    find_in_file:
        Ask user for word to find in file
        
    find_and_replace:
        Ask user for word to find in file and for word to replace it with
    
    replace:
        Replace found instances of the word in a file with a new word
    
    highlight_find:
        highlights user-searched words with find or find and replace
"""


# DONE
def find_in_file(self):

    self.file_content.tag_delete("search")
    if not self.find_in_file_canvas:

        if self.current_file is not None:
            find_in_file_canvas = tk.Canvas(self.current_file_canvas, height=25, bg=project_color, borderwidth=0,
                                            highlightthickness=0.5, width=screen_width - int((screen_width / 10)) - 1)
            find_in_file_canvas.grid_propagate(False)
            find_in_file_canvas.grid(row=0, column=0, columnspan=4)

            find_in_file_canvas.config(highlightbackground=line_number_hb)
            self.find_in_file_canvas = find_in_file_canvas

            # Mini Search Canvas
            search_canvas = tk.Canvas(find_in_file_canvas, height=20, bg=project_color, highlightthickness=0)
            search_canvas.grid(row=0, column=1, padx=(10, 0), pady=(2, 2))
            search_canvas.config(highlightbackground=line_number_hb)

            # Find Image
            search_image = tk.Button(search_canvas, anchor=tk.W, borderwidth=0, width=25, height=15,
                                     bg=line_number_hb, justify=tk.LEFT, relief=tk.FLAT)

            folder_icon = ImageTk.PhotoImage(file=os.getcwd() + "\\Images\\search.png")
            search_image.config(image=folder_icon)
            search_image.image = folder_icon

            search_image.grid(row=0, column=0, padx=0, pady=(3, 3))

            # Entry to search
            entry_find = tk.Entry(search_canvas, name="entry_find", width=40, insertbackground="white",
                                  bg=line_number_hb, relief=tk.FLAT, fg="white", borderwidth=0)
            entry_find.bindtags(('Entry', '.entry_find', '.', 'all'))
            entry_find.grid(row=0, column=1, padx=0, pady=(3, 3))
            entry_find.focus_set()

            # Number of matches
            match_case_var = tk.IntVar()
            match_case_var.set(1)
            match_case_check = tk.Checkbutton(find_in_file_canvas,
                                              variable=match_case_var, offrelief=tk.FLAT, height=1, offvalue=0,
                                              fg=project_color, bg=project_color, anchor=tk.CENTER, width=1, onvalue=1,
                                              selectcolor="white", activebackground=project_color, state=tk.ACTIVE)
            match_case_check.grid(row=0, column=2, padx=(20, 0), pady=(0, 0))

            match_case_l = tk.Label(find_in_file_canvas, width=10, text="Match Case", fg=text_color, bg=project_color)
            match_case_l.grid(row=0, column=3, padx=0, pady=(2, 2))

            # Number of matches
            entry_label = tk.Label(find_in_file_canvas, width=10, text="Matches: 0", fg=text_color, bg=project_color)
            entry_label.grid(row=0, column=4, padx=0, pady=(2, 2))

            # Highlight function
            self.root.bind("<Key>", lambda event, l=entry_label:
                           highlight_find(self, event, l, entry_find, match_case_var.get()))

            # Close Button:
            close_button = tk.Button(find_in_file_canvas, anchor=tk.NE, borderwidth=0, height=16, bg=project_color,
                                     text="WTF", fg=text_color, activebackground=project_color, relief=tk.FLAT,
                                     command=lambda: find_in_file(self))

            close_icon = ImageTk.PhotoImage(file=os.getcwd() + "\\Images\\close.png")
            close_button.config(image=close_icon)
            close_button.image = close_icon

            close_button.grid(row=0, column=0, pady=(3, 3), padx=(5, 0))

    else:

        self.find_in_file_canvas.grid_forget()
        self.file_content.tag_delete("search")
        self.find_in_file_canvas = None


# DONE
def find_and_replace(self):

    self.file_content.tag_delete("search")
    if not self.find_in_file_canvas:

        if self.current_file is not None:
            find_in_file_canvas = tk.Canvas(self.current_file_canvas, height=50, bg=project_color, borderwidth=0,
                                            highlightthickness=0.5, width=screen_width - int((screen_width / 10)) - 1)
            find_in_file_canvas.grid_propagate(False)
            find_in_file_canvas.grid(row=0, column=0, columnspan=4)

            find_in_file_canvas.config(highlightbackground=line_number_hb)
            self.find_in_file_canvas = find_in_file_canvas

            # FIND
            find_canvas = tk.Canvas(find_in_file_canvas, height=25, bg=project_color, borderwidth=0,
                                    highlightthickness=0, width=screen_width - int((screen_width / 10)) - 1)
            find_canvas.grid_propagate(False)
            find_canvas.grid(row=0)

            # Mini Search Canvas
            search_canvas = tk.Canvas(find_canvas, height=20, bg=project_color, highlightthickness=0)
            search_canvas.grid(row=0, column=1, padx=(5, 0), pady=(2, 2))
            search_canvas.config(highlightbackground=line_number_hb)

            # Find Image
            search_image = tk.Button(search_canvas, anchor=tk.W, borderwidth=0, width=25, height=15,
                                     bg=line_number_hb, justify=tk.LEFT, relief=tk.FLAT)

            folder_icon = ImageTk.PhotoImage(file=os.getcwd() + "\\Images\\search.png")
            search_image.config(image=folder_icon)
            search_image.image = folder_icon

            search_image.grid(row=0, column=0, padx=0, pady=(3, 3))

            # Entry to search
            entry_find = tk.Entry(search_canvas, name="entry_find", width=40, insertbackground="white",
                                  bg=line_number_hb, relief=tk.FLAT, fg="white", borderwidth=0)
            entry_find.bindtags(('Entry', '.entry_find', '.', 'all'))
            entry_find.grid(row=0, column=1, padx=0, pady=(3, 3))
            entry_find.focus_set()

            # Match Case
            match_case_var = tk.IntVar()
            match_case_var.set(1)
            match_case_check = tk.Checkbutton(find_canvas,
                                              variable=match_case_var, offrelief=tk.FLAT, height=1, offvalue=0,
                                              fg=project_color, bg=project_color, anchor=tk.CENTER, width=1, onvalue=1,
                                              selectcolor="white", activebackground=project_color, state=tk.ACTIVE)
            match_case_check.grid(row=0, column=2, padx=(20, 0), pady=(0, 0))

            match_case_l = tk.Label(find_canvas, width=10, text="Match Case", fg=text_color, bg=project_color)
            match_case_l.grid(row=0, column=3, padx=0, pady=(2, 2))

            # Number of matches
            entry_label = tk.Label(find_canvas, width=10, text="Matches: 0", fg=text_color, bg=project_color)
            entry_label.grid(row=0, column=4, padx=0, pady=(2, 2))

            # REPLACE
            replace_canvas = tk.Canvas(find_in_file_canvas, height=25, bg=project_color, borderwidth=0,
                                       highlightthickness=0, width=screen_width - int((screen_width / 10)) - 1)
            replace_canvas.grid_propagate(False)
            replace_canvas.grid(row=1)

            # Mini Search Canvas
            replace_word_canvas = tk.Canvas(replace_canvas, height=20, bg=project_color, highlightthickness=0)
            replace_word_canvas.grid(row=0, column=0, padx=(20, 0), pady=(0, 2))
            replace_word_canvas.config(highlightbackground=line_number_hb)

            # Find Image
            replace_image = tk.Button(replace_word_canvas, anchor=tk.W, borderwidth=0, width=25, height=15,
                                      bg=line_number_hb, justify=tk.LEFT, relief=tk.FLAT)

            folder_icon = ImageTk.PhotoImage(file=os.getcwd() + "\\Images\\search.png")
            replace_image.config(image=folder_icon)
            replace_image.image = folder_icon

            replace_image.grid(row=0, column=0, padx=0, pady=(3, 3))

            # Entry to replace
            entry_replace = tk.Entry(replace_word_canvas, name="entry_replace", width=40, insertbackground="white",
                                     bg=line_number_hb, relief=tk.FLAT, fg="white", borderwidth=0)
            entry_replace.bindtags(('Entry', '.entry_replace', '.', 'all'))
            entry_replace.grid(row=0, column=1, padx=0, pady=(3, 3))

            # replace button
            replace_b = tk.Button(replace_canvas, text="Replace all", bg=replace_butt_c, fg=text_color, relief=tk.FLAT,
                                  command=lambda bef=entry_find, aft=entry_replace: replace(self, bef, aft))
            replace_b.grid(row=0, column=1, padx=10)

            # Highlight function
            self.root.bind("<Key>", lambda event, l=entry_label:
                           highlight_find(self, event, l, entry_find, match_case_var.get()))

            # Close Button:
            close_button = tk.Button(find_canvas,
                                     anchor=tk.NE, borderwidth=0, height=16, bg=project_color, text="WTF",
                                     fg=text_color, activebackground=project_color,
                                     relief=tk.FLAT, command=lambda: find_and_replace(self))

            close_icon = ImageTk.PhotoImage(file=os.getcwd() + "\\Images\\close.png")
            close_button.config(image=close_icon)
            close_button.image = close_icon

            close_button.grid(row=0, column=0, pady=(3, 3), padx=(5, 0))

    else:

        self.find_in_file_canvas.grid_forget()
        self.file_content.tag_delete("search")
        self.find_in_file_canvas = None


# DONE
def replace(self, before, after):
    if before.get() != "":
        text = str(self.file_content.get(0.0, 'end-1c'))
        text = text.replace(str(before.get()), str(after.get()))

        self.file_content.delete(0.0, tk.END)
        self.file_content.insert(tk.INSERT, text)


# DONE
def highlight_find(self, event, label, find_entry, match_case):

    # Has to work only when using the find_entry widget
    if event.widget == find_entry and (self.find_in_file_canvas or self.find_in_file_canvas):

        self.file_content.tag_delete("search")

        try:

            # If word to search is not empty
            if event.widget.get() != "":

                if match_case:
                    wp = search_index_list(self, [event.widget.get()])
                else:
                    wp = search_index_list(self, [event.widget.get().upper(), event.widget.get().lower()])

                matches = sum(len(wp[key]) for key in wp.keys())
                label.config(text='Matches: ' + str(matches))  # Update matches

                for word in wp.keys():

                    sp = wp[word]
                    fp = []

                    for x in sp:
                        fp.append(x.split('.')[0] + "." + str(int(x.split('.')[1]) + len(word)))
                    for i in range(len(sp)):
                        self.file_content.tag_add("search", sp[i], fp[i])

                self.file_content.tag_configure("search", background="yellow", foreground="black")

            else:
                label.config(text='Matches: 0')
        except TypeError:
            pass


# DONE
"""
    RUN MENU FUNCTIONS

    run_python:
        Runs a python file (current file or right clicked project view file)
    open_in_web:
        Opens current file in default browser if .html
"""


def build_terminal_window(self, current_app, file=None):

    if not self.embedded_terminal_canvas:

        if self.current_file or file:

            embedded_terminal_canvas = tk.Canvas(self.current_file_canvas, height=201, bg=project_color, borderwidth=0,
                                                 highlightthickness=0, width=screen_width-int((screen_width / 10))-1)
            embedded_terminal_canvas.grid_propagate(False)
            embedded_terminal_canvas.grid(row=2, column=0, columnspan=4)

            embedded_terminal_canvas.config(highlightbackground=line_number_hb)
            self.embedded_terminal_canvas = embedded_terminal_canvas

            # TOP
            top_terminal_canvas = tk.Canvas(embedded_terminal_canvas, height=25, bg=line_number_hb, borderwidth=0,
                                            highlightthickness=0, width=screen_width - int((screen_width / 10)) - 1)
            top_terminal_canvas.grid_propagate(False)
            top_terminal_canvas.grid(row=0, column=0, columnspan=3)

            # Close Button:
            close_button = tk.Button(top_terminal_canvas, anchor=tk.E, borderwidth=0, height=16, bg=line_number_hb,
                                     fg=text_color, activebackground=line_number_hb, relief=tk.FLAT,
                                     command=lambda: self.embedded_terminal_canvas.grid_forget())

            close_icon = ImageTk.PhotoImage(file=os.getcwd() + "\\Images\\close.png")
            close_button.config(image=close_icon)
            close_button.image = close_icon

            close_button.grid(row=0, column=0, pady=(3, 3), padx=(5, 1), sticky=tk.E)

            # LEFT 1
            left_1_terminal_canvas = tk.Canvas(embedded_terminal_canvas, width=25, bg=emb_ter_col1, borderwidth=0,
                                               highlightthickness=0, height=176)
            left_1_terminal_canvas.grid_propagate(False)
            left_1_terminal_canvas.grid(row=1, column=0, rowspan=2)

            # LEFT 2
            left_2_terminal_canvas = tk.Canvas(embedded_terminal_canvas, width=25, bg=emb_ter_col2, borderwidth=0,
                                               highlightthickness=0, height=176)
            left_2_terminal_canvas.grid_propagate(False)
            left_2_terminal_canvas.grid(row=1, column=1, rowspan=2)

            # CENTER
            center_width = screen_width - int((screen_width / 10)) - 51
            center_terminal_canvas = tk.Canvas(embedded_terminal_canvas, bg=text_editor_color, borderwidth=0,
                                               highlightthickness=0, height=155, width=center_width)
            center_terminal_canvas.grid_propagate(False)
            center_terminal_canvas.grid(row=1, column=2)

            self.terminal_win = center_terminal_canvas

            # BOTTOM
            bottom_terminal_canvas = tk.Canvas(embedded_terminal_canvas, height=21, bg=line_number_hb, borderwidth=0,
                                               highlightthickness=0, width=center_width)
            bottom_terminal_canvas.grid_propagate(False)
            bottom_terminal_canvas.grid(row=2, column=2)

            # BOTTOM BUTTONS
            terminal_apps = ["PYTHON"]
            for app_n in range(len(terminal_apps)):

                app = terminal_apps[app_n]

                # CURRENT APP
                if app == current_app:

                    button_app = tk.Button(bottom_terminal_canvas, text=" " + app, width=15,
                                           fg=text_color, bg=text_editor_color, anchor=tk.NW, bd=0,
                                           highlightcolor=text_editor_color, highlightthickness=0)
                    button_app.grid(row=0, column=app_n, padx=(0, 0.5), ipadx=5, pady=(0, 1))

                    button_app.configure(activebackground=main_file_color, activeforeground=text_color,
                                         relief=tk.FLAT, compound="left")

                    # For GUI updates
                    try:
                        self.all_elements_bg[13].append(button_app)
                    except KeyError:
                        self.all_elements_bg[13] = [button_app]
                    try:
                        self.all_elements_fg[2].append(button_app)
                    except KeyError:
                        self.all_elements_fg[2] = [button_app]

                else:

                    button_app = tk.Button(bottom_terminal_canvas, text=" " + app, width=15,
                                           fg=text_color, bg=files_color, anchor=tk.NW, bd=0,
                                           highlightcolor=text_editor_color, highlightthickness=0)
                    button_app.grid(row=0, column=app_n, padx=(0, 0), ipadx=5, pady=(0, 1))

                    button_app.configure(activebackground=main_file_color, activeforeground=text_color,
                                         relief=tk.FLAT, compound="left")

                    # For GUI updates
                    try:
                        self.all_elements_bg[3].append(button_app)
                    except KeyError:
                        self.all_elements_bg[3] = [button_app]
                    try:
                        self.all_elements_fg[2].append(button_app)
                    except KeyError:
                        self.all_elements_fg[2] = [button_app]

                if app == "PYTHON":
                    button_app.config(command=lambda: run_python(self, file))

    else:

        self.embedded_terminal_canvas.grid_forget()

        self.terminal_win = None
        self.embedded_terminal_canvas = None
        build_terminal_window(self, current_app, file)


# DONE
def run_python(self, file=None):

    if not self.embedded_terminal_canvas:

        if (self.current_file and os.path.splitext(self.current_file)[1] == ".py") or \
                (file and os.path.splitext(file)[1] == ".py"):

            build_terminal_window(self, "PYTHON", file)
            center_terminal_canvas = self.terminal_win

            # RUN PYTHON FILE
            if file:
                file_to_run = self.current_project_dir + file
            else:
                file_to_run = self.current_file

            run_script = subprocess.Popen('python ' + file_to_run, stdout=subprocess.PIPE)
            output = run_script.stdout.read().decode(encoding='UTF-8')
            return_code = str(run_script.returncode)

            text = sys.executable + " " + file_to_run + "\n" \
                                  + output + "\n\n" \
                                  + "Process finished with exit code " + return_code

            otw = int((screen_width - int((screen_width / 10)) - 51) / 7)
            output_text = tk.Text(center_terminal_canvas, bg=text_editor_color, fg=text_color, width=otw, bd=0,
                                  font=medium_font)
            output_text.insert(0.0, text)
            output_text.grid(padx=5, pady=5)
            output_text.config(state=tk.DISABLED)

    else:

        self.embedded_terminal_canvas.grid_forget()
        self.embedded_terminal_canvas = None
        run_python(self, file)


# DONE
def open_in_web(self):

    if self.current_file is not None:
        if os.path.splitext(self.current_file)[1] == ".html":
            webbrowser.open("file://" + self.current_file)


# DONE
"""
    VIEW MENU FUNCTIONS

    write_n_lines:
        ???
        
    change_spelling:
        ???
        
    update_spelling_menu:
        ???
        
    set_colors:
        Changes application theme
"""


# DONE
def write_n_lines(self):
    self.write_line_n = not self.write_line_n
    change_text_content(self)


# DONE
def change_spelling(self):

    self.dict_yes_no = not self.dict_yes_no
    if self.dict_yes_no:
        self.spelling_text = "On"
    else:
        self.spelling_text = "Off"
    speller(self)


# DONE
def update_spelling_menu(self, menu):
    menu.entryconfig(2, accelerator=str(self.spelling_text))


# DONE
def set_colors(self, color):

    global ln_color
    global for_color
    global text_color
    global files_color
    global emb_ter_col1
    global emb_ter_col2
    global project_color
    global replace_butt_c
    global line_number_hb
    global file_bar_color
    global main_file_color
    global condition_color
    global top_bottom_color
    global text_editor_color
    global proj_view_men_col

    n_colors = 15
    if color == "DARK":
        colors = {
            0: "#191919",  # ln_color
            1: "#55FBF7",  # for_color
            2: "#DEDEDE",  # text_color
            3: "#242424",  # files_color
            4: "#494949",  # emb_ter_col1
            5: "#5A5A5A",  # emb ter_col2
            6: "#111111",  # project_color
            7: "#484848",  # replace_butt_c
            8: "#383838",  # line_number_hb
            9: "#3E3E3E",  # file_bar_color
            10: "#585858",  # main_file_color
            11: "#6CF970",  # condition_color
            12: "#484848",  # top_bottom_color
            13: "#151515",  # text_editor_color
            14: "#333333"  # proj_view_men_color
        }
    elif color == "BLUE":
        colors = {
            0: "#130061",
            1: "#000",
            2: "#FFFFFF",
            3: "#1B00B3",
            4: "#301399",
            5: "#306199",
            6: "#070B2C",
            7: "#004799",
            8: "#482E9B",
            9: "#000",
            10: "#130080",
            11: "#000",
            12: "#139CCB",
            13: "#130080",
            14: "#306199"
        }
    elif color == "ICEY":
        colors = {
            0: "#D3E5E8",
            1: "#000",
            2: "#000000",
            3: "#7DB5BA",
            4: "#A2E8E8",
            5: "#CEE8E8",
            6: "#E2E9F0",
            7: "#94C0CE",
            8: "#B8F3F6",
            9: "#000",
            10: "#B9E1EB",
            11: "#000",
            12: "#FFFFFF",
            13: "#B9E1EB",
            14: "#94C0CE"
        }
    elif color == "WHITE":
        colors = {
            0: "#FFFFFF",  # ln_color
            1: "#FFFFFF",  # for_color
            2: "#000000",  # text_color
            3: "#EFEFEF",  # files_color
            4: "#EEEEEE",  # emb_ter_col1
            5: "#DDDDDD",  # emb ter_col2
            6: "#CCCCCC",  # project_color
            7: "#EEEEEE",  # replace_butt_c
            8: "#FFFFFF",  # line_number_hb
            9: "#FFFFFF",  # file_bar_color
            10: "#EEEEEE",  # main_file_color
            11: "#FFFFFF",  # condition_color
            12: "#DDDDDD",  # top_bottom_color
            13: "#FFFFFF",  # text_editor_color
            14: "#AAAAAA"  # proj_view_men_color
        }
    elif color == "RANDOM":
        rand255 = lambda: random.randint(0, 255)
        colors = ['#%02X%02X%02X' % (rand255(), rand255(), rand255()) for _ in range(n_colors)]
    else:
        rand255 = lambda: random.randint(0, 255)
        colors = ['#%02X%02X%02X' % (rand255(), rand255(), rand255()) for _ in range(n_colors)]

    ln_color = colors[0]
    for_color = colors[1]
    text_color = colors[2]
    files_color = colors[3]
    emb_ter_col1 = colors[4]
    emb_ter_col2 = colors[5]
    project_color = colors[6]
    replace_butt_c = colors[7]
    line_number_hb = colors[8]
    file_bar_color = colors[9]
    main_file_color = colors[10]
    condition_color = colors[11]
    top_bottom_color = colors[12]
    text_editor_color = colors[13]
    proj_view_men_col = colors[14]

    self.current_color = color
    change_color_ide(self)


# DONE
def change_color_ide(self):

    global ln_color
    global for_color
    global text_color
    global files_color
    global emb_ter_col1
    global emb_ter_col2
    global project_color
    global replace_butt_c
    global line_number_hb
    global file_bar_color
    global main_file_color
    global condition_color
    global top_bottom_color
    global text_editor_color
    global proj_view_men_col

    colors = [ln_color, for_color, text_color, files_color, emb_ter_col1, emb_ter_col2, project_color,
              replace_butt_c, line_number_hb, file_bar_color, main_file_color, condition_color, top_bottom_color,
              text_editor_color, proj_view_men_col]

    # Background
    for key in self.all_elements_bg.keys():
        for widget in self.all_elements_bg[key]:
            try:
                widget.config(bg=colors[key])
            except tk.TclError:
                pass

    # Foreground
    for key in self.all_elements_fg.keys():
        for widget in self.all_elements_fg[key]:
            try:
                widget.config(fg=colors[key])
            except tk.TclError:
                pass

    # Auto modify everything else only if colors change:
    display_file_path(self)
    display_file_names(self)
    show_project_view(self, text_color, project_color)


# DONE
"""
    AUTOCOMPLETE FUNCTIONS

    on_key_pressing:
        Activates the autocomplete menu and functions every time a key is pressed
        
    get_file_keywords:
        Gets keywords (like variables) from a file
        
    autocomplete_word:
        If user clicks on word to autocomplete it automatically completes the word in the file
        
    empty_current_word:
        Removes the autocomplete menu
"""


# DONE
def on_key_pressing(self, key):

    # Remove Autocomplete Menu
    self.autocomplete_win.withdraw()

    # Forget everything
    for widget in self.autocomplete_win.grid_slaves():
        widget.grid_forget()

    get_file_keywords(self)
    if type(key.char) == str:

        if key.char == " ":

            self.current_word = ""
            self.auto_buttons = {}
            self.auto_n_button = 0

        elif key.char.isalnum() or key.char == "_":

            self.current_word += key.char

        elif key.keycode != 8:

            self.current_word = ""
            self.auto_buttons = {}
            self.auto_n_button = 0

    if key.keycode == 8:

        word_len = len(self.current_word)
        self.current_word = self.current_word[:word_len - 1]

    elif key.keycode == 13:

        self.current_word = ""
        self.auto_n_button = 0
        self.auto_buttons = {}

    autocomplete = False
    autocomplete_options = []
    curr_word_len = len(self.current_word)

    if self.current_word.replace(" ", "") != "":
        for word in self.key_words:
            if self.current_word == word[0][:curr_word_len]:
                autocomplete = True
                autocomplete_options.append(word)

    # autocomplete
    if autocomplete:

        self.autocomplete_win.deiconify()
        self.autocomplete_win.config(border=2)
        self.autocomplete_win.config(relief=tk.RIDGE)
        autocomplete_options.sort(key=lambda s: len(s))

        length = len(autocomplete_options)

        # Set position at cursor
        cursor_y, cursor_x = map(int, self.file_content.index(tk.INSERT).split("."))
        x = self.root.winfo_rootx()
        y = self.root.winfo_rooty()
        self.autocomplete_win.geometry("%dx%d+%d+%d" %
                                       (250, min(250, length * 25 + 2), x + 265 + cursor_x * 8, y + 62 + cursor_y * 16))

        index = 0
        for word in set(autocomplete_options):

            txt = " " * 4 + word[0]

            button_auto = tk.Button(self.autocomplete_win, width=238, text=txt, font=medium_font,
                                    relief=tk.FLAT, bg=project_color, fg=text_color,
                                    highlightbackground=white, border=2, anchor=tk.W,
                                    compound="left")

            if word[1] == "Function":
                func_icon = ImageTk.PhotoImage(file=os.getcwd()+"\\AutocompleteIcons\\function.png")
                button_auto.config(image=func_icon)
                button_auto.image = func_icon
            elif word[1] == "Variable":
                func_icon = ImageTk.PhotoImage(file=os.getcwd()+"\\AutocompleteIcons\\variable.png")
                button_auto.config(image=func_icon)
                button_auto.image = func_icon
            elif word[1] == "Class":
                class_icon = ImageTk.PhotoImage(file=os.getcwd()+"\\AutocompleteIcons\\class.png")
                button_auto.config(image=class_icon)
                button_auto.image = class_icon
            elif word[1] == "Module":
                module_icon = ImageTk.PhotoImage(file=os.getcwd()+"\\AutocompleteIcons\\module.png")
                button_auto.config(image=module_icon)
                button_auto.image = module_icon
            elif word[1] == "Standard":
                module_icon = ImageTk.PhotoImage(file=os.getcwd()+"\\AutocompleteIcons\\standard.png")
                button_auto.config(image=module_icon)
                button_auto.image = module_icon

            button_auto.grid(row=index, padx=0, sticky=tk.W)
            self.auto_buttons[index] = button_auto

            button_auto.bind("<Enter>", lambda event, h=button_auto: h.configure(bg=files_color))
            button_auto.bind("<Leave>", lambda event, h=button_auto: h.configure(bg=project_color))
            button_auto.bind('<Button-1>', lambda event, w=word: autocomplete_word(self, w[0]))

            index += 1


# DONE
def get_file_keywords(self):

    self.key_words = []

    if self.current_file is not None:

        # Python File
        if os.path.splitext(self.current_file)[1] == ".py":

            # Python initial keywords
            python_keywords = ["yield", "with ", "try", "return", "raise", "pass", "or", "not", "lambda", "is", "in",
                               "global", "finally", "exec", "except", "del", "def", "class", "assert", "as", "and",
                               "True", "False"]
            for p_keyword in python_keywords:
                self.key_words.append((p_keyword, "Standard"))

            # get lines
            file = open(self.current_file, "r")
            lines = file.readlines()
            file.close()

            for line in lines:

                split_line = ' '.join(line.split()).split(" ")

                # CASES
                if len(split_line) > 1:  # just the typing or the import or the def...

                    if split_line[0] == "def":
                        # function
                        self.key_words.append((split_line[1][:split_line[1].find("(")], "Function"))
                        # function arguments
                    elif split_line[0] == "import":
                        try:  # import ... as ...
                            self.key_words.append((split_line[3], "Module"))
                        except IndexError:
                            self.key_words.append((split_line[1], "Module"))
                    elif split_line[0] == "class":
                        self.key_words.append((split_line[1][:split_line[1].find("(")], "Class"))
                    elif split_line[1] == "=":
                        pass


# DONE
def autocomplete_word(self, word):

    word_len = len(self.current_word)
    missing = word[word_len:]
    self.current_word = ""
    self.autocomplete_win.withdraw()

    self.file_content.insert(tk.INSERT, missing)


# DONE
def empty_current_word(self):
    self.autocomplete_win.withdraw()


# DONE
"""
    TOP CANVAS FUNCTIONS

    display_file_path:
        Display the path from project directory to current file in top canvas
"""


# DONE
def display_file_path(self):

    for button in self.path_buttons:
        button.destroy()

    for col in range(self.max_cols):
        try:
            self.top_canvas.columnconfigure(col + 1, weight=0)
        except AttributeError:
            pass

    if self.current_file:

        current_file_path = self.current_file.replace(self.current_project_dir, "").split("/")

        current_file_path = [file_or_dir for file_or_dir in current_file_path if file_or_dir]

        # Creates the buttons
        for file_or_dir in range(len(current_file_path)):

            width = 30 + int(len(current_file_path[file_or_dir]) * 6)

            new_button_file = tk.Button(self.top_canvas, text="  " + current_file_path[file_or_dir],
                                        width=width, bd=1, highlightthickness=0.5, anchor=tk.W,
                                        bg=top_bottom_color, fg=text_color, highlightcolor=text_editor_color)
            new_button_file.grid(row=0, column=file_or_dir * 2, padx=(0, 0.5), pady=(1, 2), sticky=tk.W)
            try:
                self.top_canvas.columnconfigure(file_or_dir * 2, weight=0)
            except AttributeError:
                pass

            new_button_file.bind('<Button-1>', lambda e: 'break')  # No relief when pressed
            new_button_file.configure(activebackground=main_file_color, activeforeground=text_color, 
                                      relief=tk.FLAT, compound="left")

            # If it's a directory
            if file_or_dir != len(current_file_path) - 1:

                file_icon = ImageTk.PhotoImage(file=os.getcwd() + "\\Images\\folder.png")
                new_button_file.config(image=file_icon)
                new_button_file.image = file_icon

            else:

                file_icon = ImageTk.PhotoImage(file=os.getcwd() + "\\Images\\file.png")
                new_button_file.config(image=file_icon)
                new_button_file.image = file_icon

            self.path_buttons.append(new_button_file)

            # Decoration
            if file_or_dir != len(current_file_path) - 1:

                path_arrow_button = tk.Button(self.top_canvas, text="", bd=1, highlightthickness=0.5, anchor=tk.W,
                                              bg=top_bottom_color, fg=text_color, highlightcolor=text_editor_color)
                path_arrow_button.grid(row=0, column=(file_or_dir * 2) + 1, padx=(0, 0.5), pady=(2, 2), sticky=tk.W)
                try:
                    self.top_canvas.columnconfigure(file_or_dir * 2 + 1, weight=0)
                except AttributeError:
                    pass

                path_arrow_button.bind('<Button-1>', lambda e: 'break')  # No relief when pressed
                path_arrow_button.configure(activebackground=main_file_color, activeforeground=text_color,
                                            relief=tk.FLAT, compound="left")

                path_arrow_icon = ImageTk.PhotoImage(file=os.getcwd() + "\\Images\\path_arrow.png")
                path_arrow_button.config(image=path_arrow_icon)
                path_arrow_button.image = path_arrow_icon

                self.path_buttons.append(path_arrow_button)

        if os.path.splitext(self.current_file)[1] == ".py":

            file_basename = os.path.basename(self.current_file)
            run_button = tk.Button(self.top_canvas, text="  " + file_basename + "  ", bd=1, highlightthickness=0,
                                   anchor=tk.E, bg=top_bottom_color, fg=text_color, highlightcolor=text_editor_color)
            run_button.grid(row=0, column=(len(current_file_path) + 1), sticky=tk.E, padx=(0, 15))

            try:
                self.top_canvas.columnconfigure(len(current_file_path) + 1, weight=1)
            except AttributeError:
                pass

            current_file_base = self.current_file.replace(self.current_project_dir, "")
            run_button.bind('<Button-1>', lambda e: run_python(self, current_file_base))  # No relief when pressed
            run_button.configure(activebackground=main_file_color, activeforeground=text_color,
                                 relief=tk.GROOVE, compound="left")

            path_arrow_icon = ImageTk.PhotoImage(file=os.getcwd() + "\\Images\\run.png")
            run_button.config(image=path_arrow_icon)
            run_button.image = path_arrow_icon

            self.path_buttons.append(run_button)

        if len(current_file_path) + 1 > self.max_cols:
            self.max_cols = len(current_file_path) + 1


# DONE
"""
    FILE BAR CANVAS FUNCTIONS

    display_file_names:
        Display all open files with interactive buttons
"""


# DONE
def display_file_names(self):

    for button in self.file_bar_buttons:
        button.destroy()

    for file in range(len(self.all_open_files)):

        button_width = (current_file_width // len(self.all_open_files))  # Width per file
        if button_width > 100:
            button_width = 100

        filename = self.all_open_files[file].replace(self.current_project_dir + "/", "")

        if self.current_file.replace(self.current_project_dir + "/", "") == filename:

            filename = os.path.basename(self.all_open_files[file])
            # Reduce filename length if necessary
            if len(filename) > 10 and len(self.all_open_files) > current_file_width // len(self.all_open_files):
                ext = filename.index(".")
                filename = filename[:min(ext, 8)] + "..."

            button_current_file = tk.Button(self.file_bar_canvas, text=" "+filename, width=button_width, height=25,
                                            fg=text_color, bg=text_editor_color, highlightcolor=text_editor_color,
                                            bd=0, highlightthickness=0, anchor=tk.W,
                                            command=lambda f=self.all_open_files[file]: on_click_filename(self, f))
            button_current_file.grid(row=0, column=file, padx=(0, 0.5))

            button_current_file.configure(activebackground=main_file_color, activeforeground=text_color, 
                                          relief=tk.FLAT, compound="left")

            file_icon = ImageTk.PhotoImage(file=os.getcwd() + "\\Images\\file.png")
            button_current_file.config(image=file_icon)
            button_current_file.image = file_icon

            self.file_bar_buttons.append(button_current_file)

            # For GUI updates
            try:
                self.all_elements_bg[13].append(button_current_file)
            except KeyError:
                self.all_elements_bg[13] = [button_current_file]
            try:
                self.all_elements_fg[2].append(button_current_file)
            except KeyError:
                self.all_elements_fg[2] = [button_current_file]

            button_current_file.bind("<Button-2>", lambda event, f=self.all_open_files[file]: close_file_n(self, f))

        else:

            filename = os.path.basename(self.all_open_files[file])

            # Reduce filename length if necessary
            if len(filename) > 10 and len(self.all_open_files) > current_file_width // len(self.all_open_files):
                ext = filename.index(".")
                filename = filename[:min(ext, 8)] + "..."

            button_bg_file = tk.Button(self.file_bar_canvas, text=" "+filename, width=button_width, anchor=tk.W, bd=0,
                                       fg=text_color, bg=files_color, highlightbackground=top_bottom_color, height=25,
                                       highlightthickness=0,
                                       command=lambda f=self.all_open_files[file]: on_click_filename(self, f))
            button_bg_file.grid(row=0, column=file, padx=(0, 0.5))

            button_bg_file.configure(activebackground=main_file_color, activeforeground=text_color,
                                     relief=tk.FLAT, compound="left")

            file_icon = ImageTk.PhotoImage(file=os.getcwd() + "\\Images\\file.png")
            button_bg_file.config(image=file_icon)
            button_bg_file.image = file_icon

            # For GUI updates
            try:
                self.all_elements_bg[3].append(button_bg_file)
            except KeyError:
                self.all_elements_bg[3] = [button_bg_file]
            try:
                self.all_elements_fg[2].append(button_bg_file)
            except KeyError:
                self.all_elements_fg[2] = [button_bg_file]

            self.file_bar_buttons.append(button_bg_file)

            button_bg_file.bind("<Button-1>", lambda event: event.widget.config(relief=tk.FLAT))
            button_bg_file.bind("<Button-2>", lambda event, f=self.all_open_files[file]: close_file_n(self, f))


# DONE
"""
    PROJECT VIEW FUNCTIONS

    show_project_view + print_project_folder_view:
        List all current files and directories in a tree like structure in project view
    
    update_project_view:
        Keeps project view up to date
"""


# DONE
def show_project_view(self, button_fg, button_bg, curr_dir="", depth=0):

    self.current_project_dir = self.current_project_dir.rstrip()

    if self.current_project_dir:

        if not curr_dir:
            self.project_files_dirs = [(self.current_project_dir, depth)]
            curr_dir = self.current_project_dir
    
        if curr_dir not in self.closed_folders:
        
            # Tree like project graph
            depth += 1
            for directory in os.listdir(curr_dir):
                # If it's a directory
                if os.path.isdir(curr_dir + "/" + directory):
                    self.project_files_dirs += [(curr_dir + "/" + directory, depth)]
                    show_project_view(self, button_fg, button_bg, curr_dir=curr_dir + "/" + directory, depth=depth + 1)

            for file in os.listdir(curr_dir):

                # If it's a file...
                if not os.path.isdir(curr_dir + "/" + file):
                    self.project_files_dirs += [(curr_dir.replace(self.current_project_dir, "") + "/" + file, depth)]
    
        # Show the project directory
        print_project_folder_view(self, 200)


# DONE
def print_project_folder_view(self, but_w):

    for button in self.project_view_buttons:
        button.destroy()

    for button_to_be in range(len(self.project_files_dirs)):

        # If it's a directory
        if os.path.isdir(os.path.join(self.current_project_dir, self.project_files_dirs[button_to_be][0])) or \
                self.current_project_dir == self.project_files_dirs[button_to_be][0]:

            dir_button = tk.Button(self.project_view, command=None, anchor=tk.W, compound="left",
                                   width=but_w, fg=text_color, bg=project_color, justify=tk.LEFT, relief=tk.FLAT,
                                   text=self.project_files_dirs[button_to_be][0].split('/')
                                   [len(self.project_files_dirs[button_to_be][0].split('/')) - 1].rstrip())

            folder_icon = ImageTk.PhotoImage(file=os.getcwd() + "\\Images\\folder.png")
            dir_button.config(image=folder_icon)
            dir_button.image = folder_icon

            # For GUI updates
            try:
                self.all_elements_bg[6].append(dir_button)
            except KeyError:
                self.all_elements_bg[6] = [dir_button]
            try:
                self.all_elements_fg[2].append(dir_button)
            except KeyError:
                self.all_elements_fg[2] = [dir_button]

            dir_button.configure(activeforeground=text_color, activebackground=text_editor_color, overrelief=tk.FLAT)

            # Place button and bind it for left and right mouse click
            dir_button.grid(row=button_to_be + 1, padx=5 + self.project_files_dirs[button_to_be][1] * 15, sticky=tk.W)
            dir_button.bind("<Button-1>", lambda e, f=self.project_files_dirs[button_to_be][0]: close_folder(self, f))
            dir_button.bind("<Button-3>", lambda e: None)

            self.project_view_buttons.append(dir_button)

        # If it's a file...
        else:

            file_button = tk.Button(self.project_view, anchor=tk.W, compound="left",
                                    command=lambda f=self.project_files_dirs[button_to_be][0]:  open_file_n(self, f),
                                    width=but_w, fg=text_color, bg=project_color, justify=tk.LEFT, relief=tk.FLAT,
                                    text=self.project_files_dirs[button_to_be][0].split('/')
                                    [len(self.project_files_dirs[button_to_be][0].split('/')) - 1].rstrip())

            file_icon = ImageTk.PhotoImage(file=os.getcwd() + "\\Images\\file.png")
            file_button.config(image=file_icon)
            file_button.image = file_icon

            # For GUI updates
            try:
                self.all_elements_bg[6].append(file_button)
            except KeyError:
                self.all_elements_bg[6] = [file_button]
            try:
                self.all_elements_fg[2].append(file_button)
            except KeyError:
                self.all_elements_fg[2] = [file_button]

            file_button.configure(activeforeground=text_color, activebackground=text_editor_color, overrelief=tk.FLAT)

            file_button.grid(row=button_to_be + 1, padx=5 + self.project_files_dirs[button_to_be][1] * 15, sticky=tk.W)
            file_button.bind("<Enter>", lambda event, h=file_button: h.configure(bg=files_color))
            file_button.bind("<Leave>", lambda event, h=file_button: h.configure(bg=project_color))
            file_button.bind("<Button-3>", lambda event, f=self.project_files_dirs[button_to_be][0]:
                             right_click_file_menu(self, event, f))

            self.project_view_buttons.append(file_button)


# DONE
def update_project_view(self):

    if sorted(get_all_content(self.current_project_dir)) != sorted(self.all_in_dir):
        self.all_in_dir = get_all_content(self.current_project_dir)
        show_project_view(self, text_color, project_color)
    else:
        self.root.after(1000, lambda: update_project_view(self))


# DONE
"""
    CURRENT FILE CANVAS FUNCTIONS

    change_text_content:
        Shows current file content in file_content_view
        
    write_lines_number:
        Writes number for each line in current_file
        
    insert_tab:
        Inserts 4 spaces
"""


# DONE
def change_text_content(self):

    # Safety checks
    if self.current_file:

        if os.path.splitext(self.current_file)[1] in [".py", ".c", ".cpp", ".html", ".js", ".txt", ".cs", ".rs"]:

            # Clean current screen
            self.file_content.config(state=tk.NORMAL)
            self.file_content.delete(0.0, tk.END)

            try:
                self.current_image.place_forget()
            except AttributeError:
                pass

            self.file_content.configure(font=big_font)

            current_file = open(self.current_file, "r+")
            text = ''.join(current_file.readlines())
            current_file.close()

            self.file_content.insert(tk.INSERT, text)

            # Precautions
            save_file(self)
            display_file_names(self)

            if numbered_lines:
                if self.current_file is not None:
                    create_line_number_canvas(self)
                else:
                    self.line_number.config(state=tk.NORMAL)
                    self.line_number.delete(0.0, tk.END)
                    self.line_number.config(state=tk.DISABLED)

            if self.current_file is not None:
                if os.path.splitext(self.current_file)[1] == ".py":
                    python_watcher(self)
                elif os.path.splitext(self.current_file)[1] == ".txt":
                    speller(self)

        # image show, pretty much
        elif os.path.splitext(self.current_file)[1] in [".png", ".jpg", ".jpeg"]:

            self.file_content.config(state=tk.NORMAL)
            self.file_content.delete(0.0, tk.END)
            self.file_content.config(state=tk.DISABLED)
            try:
                self.current_image.place_forget()
            except AttributeError:
                pass

            try:

                load = Image.open(self.current_file)

                original_image_width, original_image_height = load.size
                global_width, global_height = screen_width - int((screen_width / 10)), int(screen_height * (87/100))

                if abs(global_width - original_image_width) > abs(global_height - original_image_height):
                    if original_image_width > (global_width - 100):
                        ratio = (original_image_width - (global_width - 100)) / original_image_width
                        original_image_width = (global_width - 100)
                        original_image_height = int(original_image_height - (original_image_height * ratio))
                    elif original_image_height > (global_height - 100):
                        ratio = (original_image_height - (global_height - 100)) / original_image_height
                        original_image_height = (global_height - 100)
                        original_image_width = original_image_width - (original_image_width * ratio)
                else:
                    if original_image_height > (global_height - 100):
                        ratio = (original_image_height - (global_height - 100)) / original_image_height
                        original_image_height = (global_height - 100)
                        original_image_width = int(original_image_width - (original_image_width * ratio))
                    elif original_image_width > (global_width - 100):
                        ratio = (original_image_width - (global_width - 100)) / original_image_width
                        original_image_width = (global_width - 100)
                        original_image_height = int(original_image_height - (original_image_height * ratio))

                res_load = load.resize((original_image_width, original_image_height), Image.ANTIALIAS)
                render = ImageTk.PhotoImage(res_load)

                height = (global_height - original_image_height - 35) // 2
                width = (global_width - original_image_width - 90) // 2

                if height < 0:
                    height = 0
                if width < 0:
                    width = 0

                # labels can be text or images
                self.current_image = tk.Label(self.file_content, image=render)
                self.current_image.image = render
                self.current_image.place(x=width, y=height, width=original_image_width, h=original_image_height)

            except OSError:
                messagebox.showerror("Can't open file", "File may bw corrupted or not exist")

            display_file_names(self)
        else:
            messagebox.showinfo("File not supported")

    else:

        self.file_content.config(state=tk.NORMAL)
        self.file_content.delete(0.0, tk.END)

        text = "\n" * 10 + " " * 35 + "NO FILE SELECTED"
        self.file_content.configure(font=very_big_font)

        self.file_content.insert(tk.INSERT, text)
        self.file_content.config(state=tk.DISABLED)

        try:
            self.line_number_canvas.config(state=tk.NORMAL)
            self.line_number_canvas.delete(0.0, tk.END)
            self.line_number_canvas.config(state=tk.DISABLED)
        except AttributeError:
            pass

        try:
            self.current_image.place_forget()
        except AttributeError:
            pass


# DONE
def create_line_number_canvas(self):

    lnh = int(screen_height * (87 / 100))
    lnw = (screen_width - int((screen_width / 9))) // (10 * 25)

    if self.write_line_n:

        # Line number canvas (container)
        ln_canvas = tk.Canvas(self.current_file_canvas, height=lnh, width=lnw,
                              bg=ln_color, borderwidth=0, highlightthickness=0)

        try:
            self.all_elements_bg[0].append(ln_canvas)
        except KeyError:
            self.all_elements_bg[0] = [ln_canvas]

        self.file_content.config(width=161)
        ln_canvas.grid(column=0, row=1, sticky=tk.NE)

        # Actual lines number
        line_number_cv = tk.Text(ln_canvas, height=49, width=lnw, font=big_font, fg=text_color, borderwidth=0,
                                 bg=ln_color, highlightthickness=0)

        line_number_cv.config(highlightbackground=line_number_hb)
        line_number_cv.grid(column=0, row=0, padx=10, pady=7, sticky=tk.NW)

        line_number_cv.insert(tk.INSERT, "\n".join([str(line) for line in range(1, 1000)]))
        line_number_cv.config(state=tk.DISABLED)

        self.line_number_canvas = ln_canvas

        # SCROLLBAR
        self.scrollbar.config(command=self.file_content.yview)
        self.file_content.config(yscrollcommand=self.scrollbar.set)

        # SCROLLBAR
        line_number_cv.yview("moveto", self.file_content.yview()[0])
        line_number_scroll_update(self, line_number_cv)

        # For GUI updates
        try:
            self.all_elements_bg[0].append(self.line_number_canvas)
        except KeyError:
            self.all_elements_bg[0] = [self.line_number_canvas]

        try:
            self.all_elements_bg[0].append(line_number_cv)
        except KeyError:
            self.all_elements_bg[0] = [line_number_cv]
        try:
            self.all_elements_fg[2].append(line_number_cv)
        except KeyError:
            self.all_elements_fg[2] = [line_number_cv]

        # Font Updates
        try:
            self.all_elements_fonts["big"].append(self.line_number_canvas)
        except KeyError:
            self.all_elements_fonts["big"] = [self.line_number_canvas]

        write_lines_number(self, line_number_cv)

    else:

        self.file_content.config(width=169)
        self.line_number_canvas.grid_forget()
        self.line_number_canvas = None

        # For GUI updates
        try:
            self.all_elements_bg[0].remove(self.line_number_canvas)
        except ValueError:
            pass


# DONE
def line_number_scroll_update(self, canvas):
    canvas.yview("moveto", self.file_content.yview()[0])
    self.root.after(10, lambda: line_number_scroll_update(self, canvas))


# DONE
def write_lines_number(self, canvas):

    if self.write_line_n:

        if self.current_file is not None and os.path.splitext(self.current_file)[1] not in [".png", ".jpg", ".jpeg"]:

            # WRITE LINES
            lines = self.file_content.get(1.0, tk.END).split("\n")
            lines_text = "\n".join([str(line) for line in range(1, len(lines))])

            canvas.config(state=tk.NORMAL)
            canvas.delete(0.0, tk.END)
            canvas.insert(tk.INSERT, lines_text)
            canvas.config(state=tk.DISABLED)

        else:

            canvas.config(state=tk.NORMAL)
            canvas.delete(0.0, tk.END)
            canvas.config(state=tk.DISABLED)

        if self.write_line_n:
            self.root.after(1000, lambda: write_lines_number(self, canvas))


# DONE
def insert_tab(self):
    # insert 4 spaces
    self.file_content.insert(tk.INSERT, " " * 4)


# DONE
"""
    FILE & FOLDERS MISC FUNCTIONS

    close_folder:
        Hides selected folder's content from project view
        
    open_file_n:
        Open selected file when button is pressed
        
    close_file_n:
        Close selected file when button is pressed with mouse wheel
        
    on_click_filename:
        Changes current file with one from file view
"""


# DONE
def close_folder(self, f):

    if f not in self.closed_folders:
        self.closed_folders.append(f)
    else:
        self.closed_folders.remove(f)

    show_project_view(self, text_color, project_color)


# DONE
def open_file_n(self, f):

    if self.current_project_dir.rstrip() + f not in self.all_open_files:

        save_file(self)
        self.current_file = self.current_project_dir.rstrip() + f
        self.all_open_files.append(self.current_project_dir.rstrip() + f)
        change_text_content(self)

    else:

        save_file(self)
        self.current_file = self.current_project_dir.rstrip() + f
        change_text_content(self)

    display_file_path(self)


# DONE
def close_file_n(self, file_to_close):

    index = self.all_open_files.index(file_to_close)
    self.all_open_files.remove(file_to_close)

    if self.current_file == file_to_close:

        try:
            self.current_file = self.all_open_files[index-1]
        except IndexError:
            self.current_file = None

    display_file_path(self)
    display_file_names(self)
    change_text_content(self)


# DONE
def on_click_filename(self, file):

    try:
        ext = os.path.splitext(file)[1]
        if ext in [".py", ".c", ".cpp", ".js", ".html", ".cs", ".png", ".jpg", ".jpeg", ".txt", ".rs"]:
            self.current_file = file

            display_file_path(self)
            change_text_content(self)
        else:
            messagebox.showinfo("File not supported", "The " + ext + " format is currently not supported")
    except FileNotFoundError:
        pass


# DONE
"""
    RIGHT CLICK MISC FUNCTIONS

    TODO
"""


# DONE
def project_view_file_right_menu(self, tc, tec):

    right_file_menu = tk.Menu(self.root, tearoff=0, fg=tc, bg=tec)

    # For GUI updates
    try:
        self.all_elements_bg[13].append(right_file_menu)
    except KeyError:
        self.all_elements_bg[13] = [right_file_menu]
    try:
        self.all_elements_fg[2].append(right_file_menu)
    except KeyError:
        self.all_elements_fg[2] = [right_file_menu]

    right_file_menu.add_command(label="Run", accelerator="Ctrl+R",
                                command=lambda: run_python(self, self.right_click_file))
    right_file_menu.add_separator()

    # Refactor sub-menu
    ref_menu = tk.Menu(self.root, tearoff=0, bg=text_editor_color, fg=text_color)

    # For GUI updates
    try:
        self.all_elements_bg[13].append(ref_menu)
    except KeyError:
        self.all_elements_bg[13] = [ref_menu]
    try:
        self.all_elements_fg[2].append(ref_menu)
    except KeyError:
        self.all_elements_fg[2] = [ref_menu]

    ref_menu.add_command(label="Rename File", command=lambda: ask_rename_file(self, self.right_click_file))
    ref_menu.add_command(label="Delete File", command=lambda: ask_delete_file(self, self.right_click_file))

    right_file_menu.add_cascade(label="Refactor", menu=ref_menu)

    return right_file_menu


# DONE
def right_click_file_menu(self, event, f):

    self.right_click_file = f
    self.right_project_view_file_m.grid_forget()
    self.right_project_view_file_m = project_view_file_right_menu(self, text_color, text_editor_color)
    self.right_project_view_file_m.tk_popup(event.x_root, event.y_root)
    return 0


# DONE
def ask_rename_file(self, f):

    rename_name = tk.Tk()
    rename_name.wm_title("Rename...")
    rename_name.attributes("-toolwindow", 1)
    rename_name.wm_attributes("-topmost", 1)
    rename_name.resizable(width=False, height=False)
    rename_name.focus_force()

    # Set root to center
    can_width = 350
    can_height = 25
    ws = rename_name.winfo_screenwidth()
    hs = rename_name.winfo_screenheight()
    x = (ws / 2) - (can_width / 2)
    y = (hs / 2) - (can_height / 2) - 50
    rename_name.geometry('%dx%d+%d+%d' % (can_width, can_height, x, y))

    # Main choose canvas
    main_choose_canvas = tk.Frame(rename_name, height=can_height, width=can_width, bg=line_number_hb)
    main_choose_canvas.grid_propagate(0)
    main_choose_canvas.grid()

    # New name for file entry
    new_name = tk.Entry(main_choose_canvas, width=100, insertbackground="white", bg=line_number_hb, relief=tk.FLAT,
                        fg="white", borderwidth=0)
    new_name.grid(row=0, ipady=5, padx=5, sticky=tk.W+tk.E+tk.N)

    rename_name.bind("<FocusOut>", lambda event: rename_name.destroy())
    rename_name.bind('<Return>', lambda event, r=rename_name: rename_file(self, f, new_name.get(), rename_name))

    rename_name.mainloop()


# DONE
def rename_file(self, file, new_name, root=None):

    self.current_project_dir = self.current_project_dir.rstrip()

    if root:
        root.destroy()

    # Error handling
    if new_name.replace(" ", "") == "":
        messagebox.showerror("Invalid Name", "The name you inserted is not valid")
        return 1

    if os.path.splitext(new_name)[1] != "" or os.path.splitext(new_name)[0] != "":

        if os.path.splitext(new_name)[1] not in [".txt", ".py", ".cs", ".c", ".cpp", ".html",  ".css", ".js"]:
            messagebox.showerror("Invalid Extension", "The file extension you provided is invalid")
    else:
        messagebox.showerror("Invalid Name", "The name you inserted is not valid")
        return 1

    # Rename File
    basename = os.path.basename(file)
    file_dir = self.current_project_dir + file.replace(self.current_project_dir, "").replace(basename, "")

    try:
        os.rename(file_dir + basename, file_dir + new_name)
    except OSError:
        print(OSError)

    show_project_view(self, text_color, project_color)
    change_text_content(self)


# DONE
def ask_delete_file(self, file):

    if messagebox.askyesno("Delete file", "Are you sure you want to delete this file?"):

        os.remove(self.current_project_dir + "/" + file)

        if self.current_project_dir + "/" + file in self.all_open_files:
            self.all_open_files.remove(self.current_project_dir + "/" + file)

        if file == self.current_file:
            self.current_file = None
            change_text_content(self)

        display_file_names(self)
        show_project_view(self, text_color, project_color)

    else:
        pass


# DONE
"""
    WATCHERS MISC FUNCTIONS

    python_watcher:
        Highlights python syntax
        
    speller:
        Performs text correction for text files
"""


# DONE
def python_watcher(self):

    for tag in self.file_content.tag_names():
        self.file_content.tag_delete(tag)

    if self.current_file is not None:

        if os.path.splitext(self.current_file)[1] == ".py":

            # everything else
            keywords = ["yield", "with ", "try", "return", "raise", "pass", "or", "not", "lambda", "is", "in", "global",
                        "finally", "exec", "except", "del", "def", "class", "assert", "as", "and", "True", "False"]
            keywords_positions = search_index_list(self, keywords)

            for keyword in keywords_positions.keys():

                positions = keywords_positions[keyword]
                fp = []

                for pos in positions:
                    fp.append(pos.split('.')[0] + "." + str(int(pos.split('.')[1]) + len(keyword)))

                for i in range(len(positions)):
                    try:
                        prev = int(positions[i].split(".")[1]) - 1
                        prev_char = positions[i].split(".")[0] + "." + str(prev)
                        next_char = fp[i].split(".")[0] + "." + str(int(fp[i].split(".")[1]))
                        if self.file_content.get(next_char) == " " and \
                                (prev < 0 or self.file_content.get(prev_char) == " "):
                            self.file_content.tag_add("keyword", positions[i], fp[i])
                    except ValueError:
                        pass

            self.file_content.tag_configure("keyword", foreground="#FF0000")

            # import
            keywords_positions = search_index_list(self, ["import", "from", "==", "!=", ">", "<", ">=", "<=", "="])
            for keyword in keywords_positions.keys():
                positions = keywords_positions[keyword]
                fp = []
                for pos in positions:
                    fp.append(pos.split('.')[0] + "." + str(int(pos.split('.')[1]) + len(keyword)))
                for i in range(len(positions)):
                    try:
                        prev = int(positions[i].split(".")[1]) - 1
                        prev_char = positions[i].split(".")[0] + "." + str(prev)
                        next_char = fp[i].split(".")[0] + "." + str(int(fp[i].split(".")[1]))
                        if self.file_content.get(next_char) == " " and \
                                (prev < 0 or self.file_content.get(prev_char) == " "):
                            self.file_content.tag_add("red", positions[i], fp[i])
                    except ValueError:
                        pass

            self.file_content.tag_configure("red", foreground="#ff595e")

            # conditions
            keywords_positions = search_index_list(self, ["else", "elif", "if"])
            for keyword in keywords_positions.keys():
                positions = keywords_positions[keyword]
                fp = []
                for pos in positions:
                    fp.append(pos.split('.')[0] + "." + str(int(pos.split('.')[1]) + len(keyword)))
                for i in range(len(positions)):
                    try:
                        prev = int(positions[i].split(".")[1]) - 1
                        prev_char = positions[i].split(".")[0] + "." + str(prev)
                        next_char = fp[i].split(".")[0] + "." + str(int(fp[i].split(".")[1]))
                        if self.file_content.get(next_char) == " " and \
                                (prev < 0 or self.file_content.get(prev_char) == " "):
                            self.file_content.tag_add("green", positions[i], fp[i])
                    except ValueError:
                        pass

            self.file_content.tag_configure("green", foreground="#FFD300")

            # loops
            keywords_positions = search_index_list(self, ["while", "return", "pass", "for", "continue"])
            for keyword in keywords_positions.keys():
                positions = keywords_positions[keyword]
                fp = []
                for pos in positions:
                    fp.append(pos.split('.')[0] + "." + str(int(pos.split('.')[1]) + len(keyword)))
                for i in range(len(positions)):
                    try:
                        prev = int(positions[i].split(".")[1]) - 1
                        prev_char = positions[i].split(".")[0] + "." + str(prev)
                        next_char = fp[i].split(".")[0] + "." + str(int(fp[i].split(".")[1]))
                        if self.file_content.get(next_char) == " " and \
                                (prev < 0 or self.file_content.get(prev_char) == " "):
                            self.file_content.tag_add("b", positions[i], fp[i])
                    except ValueError:
                        pass

            self.file_content.tag_configure("b", foreground=for_color)

            # short comments
            keywords_positions = search_index_list(self, ["#"])
            for keyword in keywords_positions.keys():
                positions = keywords_positions[keyword]
                fp = []
                for pos in positions:
                    fp.append(str(int(pos.split('.')[0])+1)+".0")
                for i in range(len(positions)):
                    try:
                        prev = int(positions[i].split(".")[1]) - 1
                        prev_char = positions[i].split(".")[0] + "." + str(prev)
                        next_char = fp[i].split(".")[0] + "." + str(int(fp[i].split(".")[1]))
                        if self.file_content.get(next_char) == " " and \
                                (prev < 0 or self.file_content.get(prev_char) == " "):
                            self.file_content.tag_add("pycomm", positions[i], fp[i]+"-1c")
                    except ValueError:
                        pass

            self.file_content.tag_configure("pycomm", foreground="#817c7d")

            # long comments
            positions = search_index_list(self, ["\"\"\""])
            fp = search_index_list(self, ["\"\"\""])
            for keyword in positions.keys():
                p = positions[keyword]
                for i in range(len(p)):
                    try:
                        self.file_content.tag_add("pyl_comm", p[i],  fp["\"\"\""][i] + "+2c")
                    except IndexError:
                        pass
            self.file_content.tag_configure("pyl_comm", foreground="#817c7d")

            # string "
            positions = search_index_list(self, ["\""])
            fp = search_index_list(self, ["\""])
            for keyword in positions.keys():
                p = positions[keyword][::2]
                f = fp["\""][1::2]
                for i in range(len(p)):
                    try:
                        self.file_content.tag_add("py_str", p[i], f[i] + "+1c")
                    except IndexError:
                        pass
            self.file_content.tag_configure("py_str", foreground="#009936")

            # string '
            positions = search_index_list(self, ["\'"])
            fp = search_index_list(self, ["\'"])
            for keyword in positions.keys():
                p = positions[keyword][::2]
                f = fp["\'"][1::2]
                for i in range(len(p)):
                    try:
                        self.file_content.tag_add("py_str", p[i], f[i] + "+1c")
                    except IndexError:
                        pass
            self.file_content.tag_configure("py_str", foreground="#009936")

            # commentsTodo
            keywords_positions = search_index_list(self, ["# TODO", "# todo", "# Todo"])
            for keyword in keywords_positions.keys():
                positions = keywords_positions[keyword]
                fp = []
                for pos in positions:
                    fp.append(pos.split('.')[0] + "." +
                              str(int(pos.split('.')[1]) + len(keyword)))
                for i in range(len(positions)):
                    try:
                        prev = int(positions[i].split(".")[1]) - 1
                        prev_char = positions[i].split(".")[0] + "." + str(prev)
                        next_char = fp[i].split(".")[0] + "." + str(int(fp[i].split(".")[1]))
                        if self.file_content.get(next_char) == " " and \
                                (prev < 0 or self.file_content.get(prev_char) == " "):
                            self.file_content.tag_add("todo_py", positions[i]+"+2c", fp[i])
                    except ValueError:
                        pass
            self.file_content.tag_configure("todo_py", foreground="#ffff00")

            self.root.after(1000, lambda: python_watcher(self))


# DONE
def speller(self):

    if self.current_file is not None:

        exclude = set(string.punctuation)  # Exclude punctuation

        if os.path.splitext(self.current_file)[1] == ".txt":

            self.file_content.tag_delete("misspelled")

            misspelled_words = []
            for line in self.file_content.get(0.0, tk.END).split("\n"):

                line = line.split(" ")

                for word in line:

                    word = ''.join(ch for ch in word.lower() if ch not in exclude)  # Remove punctuation

                    try:
                        self.dictionary[word]   # Find if they are in the dictionary
                    except KeyError:
                        if not word.isdigit():
                            misspelled_words.append(word)

            # underline misspelled words
            misspelled_word_indexes = search_index_list(self, misspelled_words)

            for misspelled_word in misspelled_word_indexes.keys():

                start_indexes = misspelled_word_indexes[misspelled_word]

                for i in range(len(start_indexes)):
                    index = start_indexes[i]
                    split_index = index.split('.')
                    self.file_content.tag_add("misspelled", index,
                                              split_index[0] + "." + str(int(split_index[1]) + len(misspelled_word)))

            # Underline misspelled content
            self.file_content.tag_configure("misspelled", underline=1)

            if self.dict_yes_no:
                self.root.after(2000, lambda: speller(self))  # Every two seconds
            else:
                self.file_content.tag_configure("misspelled", underline=0)


# DONE
"""
    OTHER MISC FUNCTIONS

    get_all_content:
        Gets everything from a given folder
        
    search_index_list:
        Returns the positions of given words inside current file
        
    change_color_ide:
        Keeps application color up to date
"""


# DONE
def get_all_content(folder):

    everything = []
    for obj in os.listdir(folder.rstrip()):
        if os.path.isdir(folder + "/" + obj):
            everything = everything + get_all_content(folder + "/" + obj)
        else:
            everything.append(obj)

    return everything


# DONE
def search_index_list(self, word_list):
    
    wp = {}
    for word in word_list:
        
        start = 0.0
        sp = []
        
        pos = True
        while pos:
            
            pos = self.file_content.search(word, start, stopindex="end-1c", exact=True)
            if pos and pos not in sp:
                sp.append(pos)
                
            start = pos + "+1c"

        if sp != ['']:
            wp[word] = sp

    return wp
