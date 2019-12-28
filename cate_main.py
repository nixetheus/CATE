"""
    CATE (Code And Text Editor)

    Start date: 1/12/2019
    Version: 1.0.0.2019 (= current_version.year)
"""
import ctypes
import platform
from cate_class import CATE


# TASKBAR ICON (WINDOWS ONLY
if platform.system() == "Windows":
    my_app_id = 'cate.1.0.0.2019'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_app_id)

# SETTINGS
settings_file = open("Settings/settings.txt", "r")
settings = settings_file.readlines()
settings_file.close()

# Constants and settings variables
VERSION = "0.8.1.2019"

COLOR = None
OPEN_FILES = []
FIRST_FILE = None
CURRENT_PROJECT = None
LAST_ONE = int(settings[3].rstrip().split(" ")[2])

# Reading Settings...

if settings[0].split(" ")[2].rstrip().replace(" ", "") != "":
    CURRENT_PROJECT = settings[0].split(" ")[2].rstrip()
if settings[1].rstrip().replace(" ", "") != "":
    OPEN_FILES = settings[1].rstrip().split(" ")
    try:
        FIRST_FILE = OPEN_FILES[LAST_ONE]
    except FileNotFoundError:
        FIRST_FILE = None
        OPEN_FILES = []

COLOR = settings[2].rstrip()

# START
if __name__ == "__main__":
    app = CATE(VERSION, COLOR, FIRST_FILE, CURRENT_PROJECT, OPEN_FILES)
