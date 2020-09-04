# Script takes directory that has a file called "headers.csv" and tobii files. It creates another
# directory for "clean" files that only contains the headers the user wants

import os
import re
import pandas as pd
import argparse
from datetime import datetime
import shutil


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
        bad_headers=bad_headers[0].tolist()
        print("The following headers are invalid and will be skipped: " + str(bad_headers))
        df=df[header_check[0]]
    return df[0]

def is_BIDS_struct(dirname):
    # TODO: More explicit checks of BIDS formating
    # Function returns TRUE if data are organized using BIDS structure (Person/Visit/Task)
    is_subdir = [os.path.isdir(os.path.join(dirname, f)) for f in os.listdir(dirname)]

    # If the only sub-directory is "filtered_data", then not in BIDS format
    if sum(is_subdir) == 1 and 'Filtered_Data' in os.listdir(dirname):
        return False
    # Otherwise, if there are any subdirs, potentially BIDS
    return(sum(is_subdir)  > 0)

def getListOfFiles(dirname):
    #For a given path, recursively get the list of files in the directory truee
    list_of_files = os.listdir(dirname)
    all_files = list()
    # Iterate over entries
    for x in list_of_files:
        fullpath = os.path.join(dirname, x)
        # If x is a directory, get list of files
        if os.path.isdir(fullpath):
            all_files += getListOfFiles(fullpath)
        else: # otherwise, append the file to all_files
            all_files.append(fullpath)

    return all_files

def filter_headers(full_path_to_file, failed_log, headers):
    print("Reading file " + os.path.basename(full_path_to_file))
    if os.path.splitext(full_path_to_file)[1] == '.tsv':
        df = pd.read_csv(full_path_to_file, header=0, delimiter='\t', low_memory=False)
    else:
        df = pd.read_csv(full_path_to_file, header=0, delimiter=',', low_memory=False)
    # Filter columns & save new output
    df_filtered = df.loc[:, df.columns.isin(headers)]

    # # # # # # # # # # # # #
    # Error checking
    # # # # # # # # # # # # #
    # If original tobii file is missing expected column, log it
    if len(df_filtered.columns) < len(headers):
        missing_col = [i for i in headers if i not in df_filtered.columns.tolist()]
        print(full_path_to_file + " is missing columns" + str(missing_col),
              file=failed_log)
    return(df_filtered)



def main(rootdir, headers, filtered_data_name='Filtered_Data'):
    # Look at all files in rootdir.
    # Go through all .csv and .tsv files & try to filter them.
    # Save log of 'failed' files

    if headers is None: # If user did not add headers to command line, read headers from .csv
        headers = select_headers(rootdir)
        headers = headers.tolist()
    else:
        headers=headers.split(',')

    # Check if files exist to filter
    all_files = getListOfFiles(rootdir)
    file_ext_list=[x.split('.')[-1] for x in all_files if '.' in x]
    # file_ext_list=[x.split('.')[-1] for x in os.listdir(rootdir) if '.' in x]
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
    if is_BIDS_struct(rootdir): # preserve file structure
        for root, dirs, files in os.walk(rootdir):
            #
            dirs[:] = [d for d in dirs if d!= 'Filtered_Data']
            if len(files) > 0:
                for f in files:
                    if f.split('.')[-1] in ['tsv', 'csv']:
                        # Filter headers
                        full_path_to_file = os.path.join(root, f)
                        df_filtered = filter_headers(full_path_to_file, headers)
                        # Save in same file structure
                        temp_relative_path = os.path.relpath(root, start = rootdir)
                        # Create dirs if needed
                        if not os.path.exists(os.path.join(dir_filtered, temp_relative_path)):
                            os.makedirs(os.path.join(dir_filtered, temp_relative_path))
                        df_filtered.to_csv(path_or_buf=os.path.join(dir_filtered, temp_relative_path, f), index=False)
    else:
        for f in os.listdir(rootdir):
            if f=='headers.csv': continue
            file_ext=f.split('.')[-1]

            list_of_files = os.listdir(rootdir)
            # Iterate over entries

            for x in list_of_files:
                fullpath = os.path.join(dirname, x)
                # If x is a directory, get list of files
                if os.path.isdir(fullpath):
                    all_files += getListOfFiles(fullpath)
                else:  # otherwise, append the file to all_files
                    all_files.append(fullpath)

            if file_ext in accepted_file_ext: # If it is a .tsv or .csv, read the file
                #print("Reading file " + f)
                #if file_ext == 'tsv':
                #    df = pd.read_csv(os.path.join(rootdir,f), header=0, delimiter='\t',  low_memory=False)
                #else:
                #    df = pd.read_csv(os.path.join(rootdir,f), header=0, delimiter=',', low_memory=False)
                # Filter columns & save new output

                df_filtered = filter_headers(os.path.join(rootdir,f), headers)

                # Write output
                #file_name = os.path.relpath(f, rootdir)  # Extract file name by removing root_dir from full path
                df_filtered.to_csv(path_or_buf=os.path.join(dir_filtered, f), index=False)
            else: # If not a .csv or .tsv, skip
                print(f + " is not a .csv or .tsv. Skipping!")
                continue





if __name__ == '__main__':
    ap=argparse.ArgumentParser(
        description="Filter tobii files using headers")
    ap.add_argument("-d", "--rootdir", required=True, type=str, # Can use -d or --rootdir flag
                    help="path to parent directory for project containing eye tracking files")
    ap.add_argument("--headers", required=False, type=str,
                    help="Comma separated headers (e.g. <ExportDate,StudioVersion>)")
    args=ap.parse_args()
    main(args.rootdir, args.headers)
