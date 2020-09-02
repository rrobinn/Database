Robin Sifre, robinsifre@gmail.com.  

# About  
Tobii's raw data file output contains up to 85 fields. This script creates filtered versions of those data files based on user input.  

# To execute  
## Option 1: Specify headers in .csv
0. Create <b>headers.csv</b>. This file should contain the list of columns that you would like in your final files.
An example file can be found in this repo.    
1. Save <b>headers.csv</b> in the same directory as your tobii files.  
2. Open terminal. Navigate to directory where `select-headers.py` is located.  
3. Type `python3 select-headers.py --rootdir  <path/to/your/files>`.  
e.g. `python3 select-headers.py --rootdir /Users/sifre002/select-headers/`  

## Option 2: Enter headers into command line
1. Open terminal. Navigate to directory where `select-headers.py` is located.
2. Type `python3 select-headers.py --rootdir <path/to/your/files> --headers <your,comma,separated,headers>`  
e.g. `python3 select-headers.py --rootdir /Users/sifre002/select-headers/ --headers ExportDate,DistanceRight,DistanceLeft`  

## Option 3: Use the point-and-click GUI  
<img src="https://github.com/rrobinn/Database/blob/master/img/Menu.png" align="right"
     alt="Screengrab of select-headers menu" width="144" height="240">  
     
1. Open terminal. Navigate to directory where `select-headers.py` is located.  
2. Type `python3 Select_Headers_GUI.py`.  
3. A window will pop up with a list of tobii headers. Click to select/deselect the headers you want exported.  


     
4. Then a Finder window will pop up. Navigate to the directory where your .tsv files, and select that directory.  

  
    
  

# Headers
For a complete list of headers you can export, see [Tobii Studio User Manual](https://www.tobiipro.com/siteassets/tobii-pro/user-manuals/tobii-pro-studio-user-manual.pdf)

<b>Some commonly exported headers</b>:  
-DistanceLeft  
-DistanceRight  
-EyeTrackerTimestamp  
-FixationFilter  
-FixationIndex  
-FixationPointX (MCSpx)  
-FixationPointY (MCSpx)  
-GazeEventDuration  
-GazeEventType  
-GazePointLeftX (ADCSpx)  
-GazePointLeftY (ADCSpx)  
-GazePointRightX (ADCSpx)  
-GazePointRightY (ADCSpx)  
-GazePointX (ADCSpx)  
-GazePointY (ADCSpx)  
-MediaName  
-ParticipantName  
-PupilLeft  
-PupilRight  
-RecordingDate  
-RecordingDuration  
-RecordingName  
-RecordingResolution  
-ValidityLeft  
-ValidityRight  
