"""
Script under development by Robin Sifre <robinsifre@gmail.com>.

"""

# import pywinauto
from tkinter import Tk
import tkinter.filedialog
import sys
#sys.coinit_flags = 2

def select_et_dir():
    # Make sure the TK() window doesn't appear, and doesn't keep the askdirectory up
    directory_root = Tk()
    directory_root.withdraw()
    directory_root.call('wm', 'attributes', '.', '-topmost', True) # solution to stop from crashing
    # Get dir name
    dirname = tkinter.filedialog.askdirectory()

    return dirname



