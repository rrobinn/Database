"""""
Script under development by Robin Sifre <robinsifre@gmail.com>.

This program creates a module that allows users to select which tobii headers they want to export.
It passes the selected headers as input arguments to <select-headers.py>.
"""

from tkinter import *
from tkinter.filedialog import askdirectory


#https://stackoverflow.com/questions/13828531/problems-in-python-getting-multiple-selections-from-tkinter-listbox
class App(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.master=master
        self.grid()
        self.ichose = [] # Empty list to collect all of the options that were selected

        self.l = Listbox(self, height=10, selectmode=MULTIPLE) # List where user can select multiple options
        self.l.grid(column=0, row=0, sticky=(N,W,E,S))

        s = Scrollbar(self, orient=VERTICAL, command=self.l.yview) # adding scrollbar
        s.grid(column=0, row=0, sticky=(N,S,E))
        self.l['yscrollcommand'] = s.set


        # Set up listbox
        x = ["ExportDate","StudioVersionRec","StudioProjectName","StudioTestName","ParticipantName",
                "RecordingName","RecordingDate","RecordingDuration","RecordingResolution",
                "PresentationSequence","FixationFilter","MediaName","MediaPosX (ADCSpx)","MediaPosY (ADCSpx)",
                "MediaWidth","MediaHeight","SegmentName","SegmentStart","SegmentEnd","SegmentDuration",
                "SceneName","SceneSegmentStart","SceneSegmentEnd","SceneSegmentDuration","RecordingTimestamp",
                "LocalTimeStamp","EyeTrackerTimestamp","MouseEventIndex","MouseEvent","MouseEventX (ADCSpx)",
                "MouseEventY (ADCSpx)","MouseEventX (MCSpx)","MouseEventY (MCSpx)","KeyPressEventIndex",
                "KeyPressEvent","StudioEventIndex","StudioEvent","StudioEventData","ExternalEventIndex",
                "ExternalEvent","ExternalEventValue","EventMarkerValue","FixationIndex","SaccadeIndex",
                "GazeEventType","GazeEventDuration","FixationPointX (MCSpx)","FixationPointY (MCSpx)",
                "SaccadicAmplitude","AbsoluteSaccadicDirection","RelativeSaccadicDirection",
                "GazePointIndex","GazePointLeftX (ADCSpx)","GazePointLeftY (ADCSpx)",
                "GazePointRightX (ADCSpx)","GazePointRightY (ADCSpx)","GazePointX (ADCSpx)",
                "GazePointY (ADCSpx)","GazePointX (MCSpx)","GazePointY (MCSpx)","GazePointLeftX (ADCSmm)",
                "GazePointLeftY (ADCSmm)","GazePointRightX (ADCSmm)","GazePointRightY (ADCSmm)",
                "StrictAverageGazePointX (ADCSmm)","StrictAverageGazePointY (ADCSmm)",
                "EyePosLeftX (ADCSmm)","EyePosLeftY (ADCSmm)","EyePosLeftZ (ADCSmm)",
                "EyePosRightX (ADCSmm)","EyePosRightY (ADCSmm)","EyePosRightZ (ADCSmm)","CamLeftX",
                "CamLeftY","CamRightX","CamRightY","DistanceLeft","DistanceRight","PupilLeft","PupilRight",
                "ValidityLeft","ValidityRight","IRMarkerCount","IRMarkerID","PupilGlassesRight"]

        for each_item in range(len(x)):
            self.l.insert(END, x[each_item])

        # Add button for closing the app
        button = Button(text = 'I''m done selecting!', command=master.quit)
        button.grid(column=0, row=1)

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


## TODO write code that allows user select path from finder
#root2=Tk()
#root2.withdraw()
#root2.update()
#dirname = askdirectory()
#print(dirname)


root = Tk()
root.title('Tobii headers')
app=App(root)
root.mainloop()

print(app.ichose)


## TODO pass arguments to select-headers.py