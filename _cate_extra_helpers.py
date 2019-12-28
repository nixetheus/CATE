from ctypes import windll, byref, create_unicode_buffer, create_string_buffer
FR_PRIVATE = 0x10
FR_NOT_ENUM = 0x20


# DONE
# Custom fonts
def loadfont(fontpath, private=True, enumerable=False):

    """

    Makes fonts located in file `fontpath` available to the font system.
    `private`     if True, other processes cannot see this font, and this
                  font will be unloaded when the process dies
    `enumerable`  if True, this font will appear when enumerating fonts
    """

    # This function was taken from
    # https://github.com/ifwe/digsby/blob/f5fe00244744aa131e07f09348d10563f3d8fa99/digsby/src/gui/native/win/winfonts.py#L15
    # This function is written for Python 2.x. For 3.x, you
    # have to convert the isinstance checks to bytes and str

    if isinstance(fontpath, bytes):
        pathbuf = create_string_buffer(fontpath)
        AddFontResourceEx = windll.gdi32.AddFontResourceExA
    elif isinstance(fontpath, str):
        pathbuf = create_unicode_buffer(fontpath)
        AddFontResourceEx = windll.gdi32.AddFontResourceExW
    else:
        raise TypeError('fontpath must be of type str or unicode')

    flags = (FR_PRIVATE if private else 0) | (FR_NOT_ENUM if not enumerable else 0)
    numFontsAdded = AddFontResourceEx(byref(pathbuf), flags, 0)
    return bool(numFontsAdded)


# DONE
# Show right_click menu
def right_click_menu_show(self, event):

    if True or self.current_file is not None:
        self.current_file_right_m.tk_popup(event.x_root, event.y_root, 0)


# DONE
# Load project dictionary
def load_dict(self):
    # file taken from: https://github.com/dwyl/english-words
    dictionary_file = open("Dictionary/words.txt", "r")

    for word in dictionary_file.readlines():
        self.dictionary[word.rstrip()] = True
