import os
import tkinter as tk
import _cate_gui_main as gm
import _cate_extra_helpers as eh
import _cate_gui_main_helpers as gmh


class CATE(object):

    """CATE Editor Class"""

    """
        ----------------------Init---------------------------------
    """

    # Import functions from other files for cleanness

    # Init method:
    def __init__(self, color, first_file, current_project, open_files):

        # ROOT
        self.root = tk.Tk()
        self.root.state('zoomed')
        self.root.wm_title(" CATE")
        self.root.configure(background="blue")
        self.root.protocol('WM_DELETE_WINDOW', lambda: gmh.on_closing(self))

        # Cate Icon
        icon = tk.PhotoImage(file=os.getcwd() + "\Images\icon.png")
        self.root.tk.call('wm', 'iconphoto', self.root.w, icon)

        # Current State Variables
        self.current_image = None
        self.current_color = color
        self.current_file = first_file
        self.current_project_dir = current_project

        # Main Canvases
        self.main_canvas = None

        self.top_canvas = None
        self.bottom_canvas = None
        self.file_bar_canvas = None
        self.autocomplete_tl = None
        self.project_view_canvas = None
        self.current_file_canvas = None

        # Right Menus
        self.right_click_file = None
        self.right_click_folder = None
        self.current_file_right_m = None
        self.right_project_view_file_m = None
        self.right_project_view_folder_m = None

        # File Path View Vars
        self.max_cols = 0
        self.path_buttons = []

        # Files Bar View Vars
        self.file_bar_buttons = []

        # Autocomplete Top Level Vars

        # Project View Vars
        self.project_view = None
        self.project_files_dirs = []
        self.project_view_buttons = []

        # Current File View Vars
        self.terminal_win = None
        self.file_content = None  # Content of current file
        self.autocomplete_win = None
        self.line_number_canvas = None
        self.find_in_file_canvas = None
        self.embedded_terminal_canvas = None

        # Autocomplete View Vars and Methods
        self.key_words = []
        self.auto_buttons = {}
        self.auto_n_button = 0
        gmh.get_file_keywords(self)

        # More Useful Variables
        self.delete = True
        self.write_line_n = True
        self.current_word = ""
        self.change_col = False
        self.dict_yes_no = True
        self.write_line_n = True
        self.spelling_text = "On"
        self.roots_to_close = []
        self.variables = {"global": []}

        # Dictionary
        self.dictionary = {}
        eh.load_dict(self)

        # All elements grouped by specs
        self.all_elements_bg = {}
        self.all_elements_fg = {}
        self.all_elements_fonts = {}
        self.all_open_files = open_files
        self.all_in_dir = gmh.get_all_content(self.current_project_dir.rstrip())

        # Closed folders
        self.closed_folders = []

        # Icons
        run_ico = "Images/run.png"
        folder_ico = "Images/folder.png"
        self.run_image = tk.PhotoImage(file=run_ico)
        self.folder_image = tk.PhotoImage(file=folder_ico)

        # BINDS
        self.root.bind('<Control-p>', lambda event: gmh.printer(self))
        self.root.bind('<Control-n>', lambda event: gmh.new_file(self))
        self.root.bind('<Control-s>', lambda event: gmh.save_file(self))
        self.root.bind('<Control-o>', lambda event: gmh.open_file(self))
        self.root.bind('<Control-X>', lambda event: gmh.on_closing(self))
        self.root.bind('<Control-R>', lambda event: gmh.run_python(self))
        self.root.bind('<Control-N>', lambda event: gmh.set_project(self))
        self.root.bind('<Control-f>', lambda event: gmh.find_in_file(self))
        self.root.bind('<Control-S>', lambda event: gmh.save_file_as(self))
        self.root.bind('<Control-r>', lambda event: gmh.find_and_replace(self))
        self.root.bind('<Control-w>', lambda event: gmh.close_current_file(self))

        # INIT METHOD CALLINGS
        self.main_canvas = gm.gui_main(self)

        # OTHER METHODS
        gmh.change_color_ide(self)
        self.file_content.bind("<Button-1>", lambda event: gmh.empty_current_word(self))
        self.file_content.bind("<KeyPress>", lambda key: gmh.on_key_pressing(self, key))
        self.file_content.bind("<Button-3>", lambda e: eh.right_click_menu_show(self, e))

        # MAINLOOP
        self.root.mainloop()
