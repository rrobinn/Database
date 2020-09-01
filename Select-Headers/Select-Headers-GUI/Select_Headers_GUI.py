from select_path_to_eyetracking_data import *
from select_headers_app import *
from tkinter import *
import sys

# GUI for selecting Tobii headers
root = Tk()
root.title('Tobii headers')
app=App(root)
root.mainloop()
print(app.ichose)

# GUI For selecting ET path
path_to_et_data = select_et_dir()
print('path: ' + path_to_et_data)  


# Call select-headers.py
script_descriptor = open('select_headers.py')
this_script = script_descriptor.read()
sys.argv = ['select_headers.py',
            '--rootdir', path_to_et_data,
            '--headers', app.ichose]

exec(this_script)

