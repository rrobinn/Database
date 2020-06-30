Robin Sifre, robinsifre@gmail.com.  

# About  
Tobii's raw data file output contains up to 85 fields. This script creates filtered versions of those data files based on user input.  

# To execute  
## Using headers.csv
0. Create <b>headers.csv</b>. This file should contain the list of columns that you would like in your final files.
An example file can be found in this repo.    
1. Save <b>headers.csv</b> in the same directory as your tobii files.  
2. Open terminal.  
3. Type `python3 select-headers.py --rootdir  <path/to/your/files>`.  
e.g. `python3 select-headers.py --rootdir /Users/sifre002/select-headers/`  

## Entering headers into command line
1. Open terminal.  
2. Type `python3 select-headers.py --rootdir <path/to/your/files> --headers <your,comma,separated,headers>`  
e.g. `python3 select-headers.py --rootdir /Users/sifre002/select-headers/ --headers ExportDate,DistanceRight,DistanceLeft`
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
