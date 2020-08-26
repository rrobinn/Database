from tkinter import *
#https://stackoverflow.com/questions/13828531/problems-in-python-getting-multiple-selections-from-tkinter-listbox
class App(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.master=master
        self.grid()
        self.ichose = [] # Empty list to collect all of the options that were selected

        self.l = Listbox(self, height=10, selectmode=MULTIPLE)
        # Selectmode can be SINGLE, BROWSE, MULTIPLE or EXTENDED. Default BROWSE
        self.l.grid(column=0, row=0, sticky=(N,W,E,S))

        s = Scrollbar(self, orient=VERTICAL, command=self.l.yview)
        s.grid(column=0, row=0, sticky=(N,S,E))
        self.l['yscrollcommand'] = s.set

        # Set up listbox
        x = ["X", "Y", "Media", "ID", "a", "b", "c", "D"]
        for each_item in range(len(x)):
            self.l.insert(END, x[each_item])
            #self.l.itemconfig(each_item, bg="lime")
        #self.box.pack()

        # Create textbox that will display selected items from the list
        self.selected_list = Text(self, width=20, height=10,wrap=WORD)
        self.selected_list.grid(row=12, column=0, sticky=W)

        # Execute poll() function
        #self.ichose = self.poll()
        self.ichose = self.poll()


    def poll(self):
        items = []
        self.ichose=[]
        self.selected_list.after(200, self.poll) # recurring event every 200ms
        items = map(int, self.l.curselection())
        items = self.l.curselection()
        for i in range(len(items)):
            self.ichose.append(self.l.get(items[i]))


        return self.ichose

""""
    def update_list(self):
        self.selected_list.delete(0.0, END)
        self.selected_list.insert(0.0, self.ichose) """

root = Tk()
root.title('test')
app=App(root)
root.mainloop()

print(app.ichose)
