# Script takes directory that has a file called "headers.csv" and tobii files. It creates another
# directory for "clean" files that only contains the headers the user wants

import os
import re
import pandas as pd
import argparse
from datetime import datetime



def select_headers(mydir):
    # Set vars
    tobii_out_cols = ["ExportDate","StudioVersionRec","StudioProjectName","StudioTestName","ParticipantName",
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
    # Check if directory exists
    if not os.path.isdir(mydir):
        print('Directory does not exist. Exiting')
        return
    # Check that the .csv is in the dir
    if not os.path.exists(str(mydir + 'headers.csv')):
        print('headers.csv does not exist. Please create .csv file with your desired headers. Exiting')
        return
    # Read in file with headers
    header_file=str(mydir+'headers.csv')
    df=pd.read_csv(header_file, header=None)
    # Make data long if wide
    if df.shape[0] < df.shape[1]:
        df=df.transpose()
    # Check that user's headers are tobii headers
    header_check=df.isin(tobii_out_cols)
    if header_check.sum()[0] - header_check.shape[0] != 0:
        bad_headers=df[header_check[0]==False]
        print("The following headers are invalid: " + bad_headers)
    return df[0]


def main(rootdir, filtered_data_name='Filtered_Data'):
    # Look at all files in rootdir.
    # Go through all .csv and .tsv files & try to filter them.
    # Save log of 'failed' files

    headers = select_headers(rootdir)
    headers = headers.tolist()
    # Check if files exist to filter
    file_ext_list=[x.split('.')[-1] for x in os.listdir(rootdir) if '.' in x]
    accepted_file_ext=['tsv','csv']
    if not any(item in accepted_file_ext for item in file_ext_list):
        return Exception("No .tsv or .csv files found in {}".format(rootdir))

    # Create Filtered_Data directory if it doesn't exist
    dir_filtered=os.path.join(rootdir, filtered_data_name)
    if not os.path.exists(dir_filtered):
        os.mkdir(dir_filtered)

    # start log of files with issues
    failed_files=open(os.path.join(dir_filtered, "error_log.txt"), 'a+')
    print("---------------- " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " ----------------",
          file=failed_files)

    # iterate through files
    for f in os.listdir(rootdir):
        file_ext=f.split('.')[-1]

        if file_ext in accepted_file_ext:
            # Read file
            print("Reading file " + f)
            if file_ext == 'tsv':
                df = pd.read_csv(f, header=0, delimiter='\t')
            else:
                df = pd.read_csv(f, header=0, delimiter='\t')

            # Filter columns & save new output
            df_filtered = df.loc[:, df.columns.isin(headers)]
            # If original tobii file is missing expected column, log it
            if len(df_filtered.columns) < len(headers):
                missing_col=[i for i in headers if i not in df_filtered.columns.tolist()]
                print(f + " is missing columns" + str(missing_col),
                    file=failed_files)
            # Write output
            file_name = os.path.relpath(f, rootdir)  # Extract file name by removing root_dir from full path
            df_filtered.to_csv(path_or_buf=os.path.join(dir_filtered, file_name), index=False)
        else:
            # If not a .csv or .tsv, log in failed_files
            print(f, file=files_files)



if __name__ == '__main__':
    ap=argparse.ArgumentParser(
        description="Filter tobii files using headers")
    ap.add_argument("-d", "--rootdir", required=True, type=str,
                    help="path to parent directory for project containing eye tracking files")
    args=ap.parse_args()
    main(args.rootdir)
