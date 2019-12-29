import random
import webbrowser
import tkinter as tk
import _cate_extra_helpers as ceh
import _cate_gui_main_helpers as gmh

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
numbered_lines = True

""" SETTINGS """


def load_extra_fonts():
    ceh.loadfont("/Fonts/Hack-Regular.tff")


# DONE
def set_colors(self):

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
    if self.current_color == "DARK":
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
    elif self.current_color == "BLUE":
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
    elif self.current_color == "ICEY":
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
    elif self.current_color == "WHITE":
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
    elif self.current_color == "RANDOM":
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


""" MAIN """


# DONE
def gui_main(self):

    set_colors(self)
    load_extra_fonts()

    # VARIABLES
    screen_width = self.root.winfo_screenwidth()
    screen_height = self.root.winfo_screenheight()
    gmh.set_values(self, screen_width - (screen_width // 10), True)

    menu_creation(self, text_color, text_editor_color)

    # Create and position main canvas in root
    main_canvas = tk.Canvas(self.root)
    self.main_canvas = main_canvas
    main_canvas.grid()

    # TOP CANVAS
    top = top_canvas_creation(main_canvas, 25, screen_width, text_editor_color, top_bottom_color)

    self.top_canvas = top

    # For GUI updates
    try:
        self.all_elements_bg[12].append(self.top_canvas)
    except KeyError:
        self.all_elements_bg[12] = [self.top_canvas]

    # TOP CANVAS METHODS
    gmh.display_file_path(self)

    # AUTOCOMPLETE TOP LEVEL
    autocomplete = autocomplete_creation(self, project_color)
    self.autocomplete_tl = autocomplete

    # RIGHT MENUS
    current_file_right_m = current_file_right_menu(self, text_color, text_editor_color)
    self.current_file_right_m = current_file_right_m

    right_project_view_file_m = gmh.project_view_file_right_menu(self, text_color, text_editor_color)
    self.right_project_view_file_m = right_project_view_file_m

    # FILE BAR CANVAS
    file_bar = file_bar_creation(main_canvas, 25, screen_width - (screen_width // 10), files_color)

    self.file_bar_canvas = file_bar

    # For GUI updates
    try:
        self.all_elements_bg[3].append(self.file_bar_canvas)
    except KeyError:
        self.all_elements_bg[3] = [self.file_bar_canvas]

    main_height = int(screen_height * (87/100))

    # FILE BAR CANVAS METHODS
    gmh.display_file_names(self)

    # PROJECT VIEW CANVAS  (W = 10%)
    project_view = project_view_creation(self, main_canvas, main_height + 25, (screen_width // 10), project_color)

    self.project_view = project_view

    # For GUI updates
    try:
        self.all_elements_bg[6].append(self.project_view)
    except KeyError:
        self.all_elements_bg[6] = [self.project_view]

    # PROJECT VIEW CANVAS METHODS
    gmh.show_project_view(self, text_color, project_color)
    gmh.update_project_view(self)

    # CURRENT_FILE VIEW CANVAS  (W = 90%)
    right_side_canvas_width = int((screen_width / 75))

    current_file_canvas, content, right_side_view_canvas = \
        current_file_view_creation(self, main_canvas, main_height, screen_width - int((screen_width / 10)),
                                   text_color, text_editor_color, line_number_hb,
                                   main_height, right_side_canvas_width, text_editor_color)

    self.file_content = content
    self.current_file_canvas = current_file_canvas

    # For GUI updates
    try:
        self.all_elements_bg[13].append(self.file_content)
    except KeyError:
        self.all_elements_bg[13] = [self.file_content]
    try:
        self.all_elements_fg[2].append(self.file_content)
    except KeyError:
        self.all_elements_fg[2] = [self.file_content]

    # For GUI updates
    try:
        self.all_elements_bg[13].append(self.current_file_canvas)
    except KeyError:
        self.all_elements_bg[13] = [self.current_file_canvas]

    # CURRENT_FILE VIEW CANVAS METHODS
    gmh.change_text_content(self)

    # AUTOCOMPLETE CANVAS
    self.autocomplete_win = autocomplete_creation(self, project_color)

    # BOTTOM VIEW CANVAS  (W = 100%)
    bottom_view = bottom_creation(main_canvas, screen_height - main_height, screen_width, 
                                  top_bottom_color, main_file_color)

    self.bottom_canvas = bottom_view

    # For GUI updates
    try:
        self.all_elements_bg[12].append(self.bottom_canvas)
    except KeyError:
        self.all_elements_bg[12] = [self.bottom_canvas]


""" MENU """


# DONE
def menu_creation(self, tc, tec):

    # MAIN MENU
    menu = tk.Menu(tearoff=0)

    # Add menu
    file_menu = file_menu_creation(self, menu, tc, tec)
    menu.add_cascade(label="File", menu=file_menu)

    edit_menu = edit_menu_creation(self, menu, tc, tec)
    menu.add_cascade(label="Edit", menu=edit_menu)

    run_menu = run_menu_creation(self, menu, tc, tec)
    menu.add_cascade(label="Run", menu=run_menu)

    view_menu = view_menu_creation(self, menu, tc, tec)
    menu.add_cascade(label="View", menu=view_menu)

    help_menu = help_menu_creation(menu, tc, tec)
    menu.add_cascade(label="Help", menu=help_menu)

    menu_gui_elements = [file_menu, edit_menu, run_menu, view_menu, help_menu]

    # For GUI updates
    try:
        self.all_elements_bg[13].extend(menu_gui_elements)
    except KeyError:
        self.all_elements_bg[13] = menu_gui_elements
    try:
        self.all_elements_fg[2].extend(menu_gui_elements)
    except KeyError:
        self.all_elements_fg[2] = menu_gui_elements

    tk.Tk.config(self.root, menu=menu)


# DONE
def file_menu_creation(self, menu, tc, tec):

    # File menu
    file_menu = tk.Menu(menu, tearoff=0, fg=tc, bg=tec)

    # File menu entries
    file_menu.add_command(label="New Project        ", accelerator="Ctrl+N",
                          command=lambda: gmh.set_project(self))
    file_menu.add_separator()

    file_menu.add_command(label="New Folder         ",
                          command=lambda: gmh.new_folder(self))
    file_menu.add_separator()

    file_menu.add_command(label="New File           ", accelerator="Ctrl+n",
                          command=lambda: gmh.new_file(self))
    file_menu.add_command(label="Open...            ", accelerator="Ctrl+o",
                          command=lambda: gmh.open_file(self))
    file_menu.add_command(label="Save               ", accelerator="Ctrl+s",
                          command=lambda: gmh.save_file(self))
    file_menu.add_command(label="Save as...         ", accelerator="Ctrl+S",
                          command=lambda: gmh.save_file_as(self))
    file_menu.add_command(label="Close File         ", accelerator="Ctrl+w",
                          command=lambda: gmh.close_current_file(self))
    file_menu.add_separator()

    file_menu.add_command(label="Print              ", accelerator="Ctrl+p",
                          command=lambda: gmh.printer(self))
    file_menu.add_separator()

    file_menu.add_command(label="Exit               ", accelerator="Ctrl+X",
                          command=lambda: gmh.on_closing(self))

    return file_menu


# DONE
def edit_menu_creation(self, menu, tc, tec):

    # Edit menu
    edit_menu = tk.Menu(menu, tearoff=0, fg=tc, bg=tec)

    # Edit menu entries
    edit_menu.add_command(label="Find               ", accelerator="Ctrl+f",
                          command=lambda: gmh.find_in_file(self))
    edit_menu.add_command(label="Find and Replace   ", accelerator="Ctrl+r",
                          command=lambda: gmh.find_and_replace(self))
    edit_menu.add_separator()

    edit_menu.add_command(label="Copy               ", accelerator="Ctrl+c",
                          command=lambda: self.right_menu.focus_get().event_generate('<<Copy>>'))
    edit_menu.add_command(label="Paste              ", accelerator="Ctrl+v",
                          command=lambda: self.right_menu.focus_get().event_generate('<<Paste>>'))
    edit_menu.add_command(label="Cut                ", accelerator="Ctrl+x",
                          command=lambda: self.right_menu.focus_get().event_generate('<<Cut>>'))

    return edit_menu


# DONE
def run_menu_creation(self, menu, tc, tec):

    # Run menu
    run_menu = tk.Menu(menu, tearoff=0, fg=tc, bg=tec)

    # Run menu entries
    run_menu.add_command(label="Run                 ", accelerator="(Python) Ctrl+R",
                         command=lambda: gmh.run_python(self), compound="left")
    run_menu.add_command(label="Open in Browser     ", accelerator="(HTML)",
                         command=lambda: gmh.open_in_web(self), compound="left")

    return run_menu


# DONE
def view_menu_creation(self, menu, tc, tec):

    # View menu
    view_menu = tk.Menu(menu, tearoff=0, fg=tc, bg=tec,
                        postcommand=lambda: view_menu.entryconfig(1, accelerator=str(self.spelling_text)))

    # View menu entries
    view_menu.add_command(label="Line Number        ", command=lambda: gmh.write_n_lines(self))
    view_menu.add_command(label="Spelling           ", accelerator=self.spelling_text,
                          command=lambda: gmh.change_spelling(self))

    # Themes sub-menu
    themes_menu = tk.Menu(view_menu, tearoff=0, fg=tc, bg=tec)

    # Themes menu entries
    themes_menu.add_command(label="Ice              ", command=lambda: gmh.set_colors(self, "ICEY"))
    themes_menu.add_command(label="Dark             ", command=lambda: gmh.set_colors(self, "DARK"))
    themes_menu.add_command(label="Blue             ", command=lambda: gmh.set_colors(self, "BLUE"))
    themes_menu.add_command(label="White            ", command=lambda: gmh.set_colors(self, "WHITE"))
    themes_menu.add_separator()
    themes_menu.add_command(label="RANDOM", command=lambda: gmh.set_colors(self, "RANDOM"))

    view_menu.add_cascade(label="Edit Theme", menu=themes_menu)

    # For GUI updates
    try:
        self.all_elements_bg[13].append(themes_menu)
    except KeyError:
        self.all_elements_bg[13] = [themes_menu]
    try:
        self.all_elements_fg[2].append(themes_menu)
    except KeyError:
        self.all_elements_fg[2] = [themes_menu]

    return view_menu


# DONE
def help_menu_creation(menu, tc, tec):

    # Help menu
    help_menu = tk.Menu(menu, tearoff=0, fg=tc, bg=tec)

    # Help menu entries
    site = "https://github.com/nixetheus/CATE"
    help_menu.add_command(label="On GitHub          ", command=lambda w=site: webbrowser.open(w))

    return help_menu


""" AUTOCOMPLETE """


# DONE
def autocomplete_creation(self, pc):

    autocomplete_win = tk.Toplevel(self.root, bg=pc, relief=tk.RAISED)
    autocomplete_win.grid()
    autocomplete_win.grid_propagate(False)

    autocomplete_win.withdraw()
    autocomplete_win.overrideredirect(True)

    return autocomplete_win


""" MAIN GUI """


# DONE
def top_canvas_creation(main_canvas, h, w, tec, top_btm_color):

    # Top canvas
    top = tk.Canvas(main_canvas, bg=top_btm_color, height=h, width=w,
                    borderwidth=0,  highlightthickness=0, relief=tk.RIDGE)

    # Top canvas proprieties
    top.config(highlightbackground=tec)
    top.grid(row=0, column=0, columnspan=3, sticky=tk.W)

    top.grid_propagate(False)

    return top


# DONE
def file_bar_creation(main_canvas, h, w, fc):

    # File bar canvas
    file_can = tk.Canvas(main_canvas, height=h, width=w, bg=fc, highlightthickness=0, relief=tk.FLAT)

    # File bar canvas proprieties
    file_can.grid(row=1, column=1, columnspan=2, sticky=tk.W)
    file_can.grid_propagate(False)

    return file_can


# DONE
def project_view_creation(self, main_canvas, h, w, project_view_color):

    # File bar canvas
    project_view = tk.Canvas(main_canvas, height=h, width=w, bg=project_view_color,
                             highlightthickness=0, relief=tk.FLAT, borderwidth=0)

    # File bar canvas proprieties
    project_view.grid(rowspan=2, row=1, column=0, sticky=tk.W)
    project_view.grid_propagate(False)

    # Right project view canvas
    right_side_view = tk.Canvas(project_view, height=h, width=w // 10, bg=files_color,
                                borderwidth=0, highlightthickness=0)
    right_side_view.grid(row=0, column=0, rowspan=2, sticky=tk.N)
    right_side_view.grid_propagate(False)

    # For GUI updates
    try:
        self.all_elements_bg[3].append(right_side_view)
    except KeyError:
        self.all_elements_bg[3] = [right_side_view]

    # Project view menu
    project_view_menu_canvas = tk.Canvas(project_view, width=w, bg=proj_view_men_col, height=25, highlightthickness=0)
    project_view_menu_canvas.grid(row=0, column=1, sticky=tk.W)
    project_view_menu_canvas.grid_propagate(False)

    # For GUI updates
    try:
        self.all_elements_bg[14].append(project_view_menu_canvas)
    except KeyError:
        self.all_elements_bg[14] = [project_view_menu_canvas]

    project_text = tk.Label(project_view_menu_canvas, fg=text_color, bg=proj_view_men_col, text="Project View",
                            borderwidth=2, relief=tk.FLAT, anchor=tk.W, compound="left")
    project_text.grid(row=0, column=0, sticky=tk.W, ipady=0, pady=(2, 2), padx=(5, 0))

    # For GUI updates
    try:
        self.all_elements_bg[14].append(project_text)
    except KeyError:
        self.all_elements_bg[14] = [project_text]
    try:
        self.all_elements_fg[2].append(project_text)
    except KeyError:
        self.all_elements_fg[2] = [project_text]

    # Project view inside
    project_view_inside = tk.Canvas(project_view, width=w, bg=project_color, height=h - 23, highlightthickness=0)
    project_view_inside.grid(row=1, column=1, sticky=tk.W, pady=0)
    project_view_inside.grid_propagate(False)

    return project_view_inside


# DONE
def current_file_view_creation(self, main_canvas, h, w, tc, tec, ln_hb, rsh, rsw, rsc):

    # Current file canvas
    current_file_view = tk.Canvas(main_canvas, height=h, width=w, bg=tec, highlightthickness=0)

    current_file_view.config(highlightbackground=ln_hb)
    current_file_view.grid(row=2, column=1, sticky=tk.W)

    current_file_view.grid_propagate(False)

    # File content
    file_content = tk.Text(current_file_view, height=50, width=161, fg=tc, bg=tec,
                           borderwidth=0, highlightthickness=0, tabs='1c')
    file_content.insert(tk.INSERT, "No file selected.")
    file_content.configure(font=("helvetica", 12, "bold"))

    file_content.config(insertbackground=tc)
    file_content.grid(column=1, row=1, padx=5, pady=7, sticky=tk.N+tk.S+tk.W+tk.E)

    file_content.bind("<Tab>", lambda e: gmh.insert_tab(self))

    # Scrollbar
    scrollbar = tk.Scrollbar(current_file_view, width=rsw - int(rsw / 2.5), borderwidth=0,
                             highlightthickness=0, relief=tk.FLAT)

    scrollbar.config(command=file_content.yview)
    current_file_view.grid_rowconfigure(1, weight=1)
    file_content.config(yscrollcommand=scrollbar.set)

    scrollbar.grid(row=1, column=3, sticky=tk.N+tk.S+tk.W)

    # Right View file canvas
    right_side_view = tk.Canvas(current_file_view, height=rsh, width=int(rsw/2.5), bg=rsc,
                                borderwidth=0, highlightthickness=0)
    right_side_view.grid(row=1, column=2, sticky=tk.N)
    right_side_view.grid_propagate(False)

    try:
        self.all_elements_bg[13].append(right_side_view)
    except KeyError:
        self.all_elements_bg[13] = [right_side_view]

    # No writing if no file
    file_content.config(state=tk.DISABLED)

    return current_file_view, file_content, right_side_view


# DONE
def bottom_creation(main_canvas, h, w, tbc, hl_bg):

    # Bottom
    bottom = tk.Canvas(main_canvas, height=h, width=w, bg=tbc, highlightthickness=0)

    bottom.config(highlightbackground=hl_bg)
    bottom.grid(row=3, column=0, columnspan=3, sticky=tk.NW)

    bottom.grid_propagate(False)

    return bottom


""" RIGHT CLICK MENUS """


# DONE
def current_file_right_menu(self, tc, tec):

    right_menu = tk.Menu(self.root, tearoff=0, fg=tc, bg=tec)
    # For GUI updates
    try:
        self.all_elements_bg[13].append(right_menu)
    except KeyError:
        self.all_elements_bg[13] = [right_menu]
    try:
        self.all_elements_fg[2].append(right_menu)
    except KeyError:
        self.all_elements_fg[2] = [right_menu]

    right_menu.add_command(label="Copy              ", accelerator="Ctrl+c",
                           command=lambda: right_menu.focus_get().event_generate('<<Copy>>'))
    right_menu.add_command(label="Paste             ", accelerator="Ctrl+v",
                           command=lambda: right_menu.focus_get().event_generate('<<Paste>>'))
    right_menu.add_command(label="Cut               ", accelerator="Ctrl+x",
                           command=lambda: right_menu.focus_get().event_generate('<<Cut>>'))
    right_menu.add_separator()

    right_menu.add_command(label="Save              ", accelerator="Ctrl+s",
                           command=lambda: gmh.save_file(self))
    right_menu.add_separator()

    right_menu.add_command(label="Run...            ", accelerator="Ctrl+R", compound="left",
                           command=lambda: gmh.run_python(self))

    return right_menu
