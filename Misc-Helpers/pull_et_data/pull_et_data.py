import argparse
import shutil
import os
from pathlib import Path
from datetime import datetime
import re

'''configuration: pull_et_data.py --rootdir
/Users/sifre002/Box/Elab_ET_Data/BCP_BSLERP/AUDIT_PASSED/
--destination
/Users/sifre002/Desktop/data/
--tasks
Calibration_Verification,EU-AIMS_counter_1 '''

'''  def getListOfFiles(dirname):
    # create list of files
    file_list = os.listdir(dirname)
    all_files = list()
    #all_subdirs = list()
    for entry in file_list:
        full_path = os.path.join(dirname, entry)
        if os.path.isdir(full_path): # If full_path is a directory
            all_files=all_files + getListOfFiles(full_path) # get file list from directory
        else:
            all_files.append( os.path.relpath(full_path, dirname) )
    return all_files

'''


def main(rootdir, destination, tasks, keepBIDS):
    # Copy specific eye-tracking tasks from rootdir to destination
    # Create the destination directory for all ET files if it does not exist

    # Create sub-directory with label if it is in BIDS format
    if keepBIDS is True:
        destination += "BIDS"
    else:
        destination += 'Session'

    if not os.path.exists(destination):
        os.mkdir(destination)

    # start log of files with issues
    log_name = "log" + datetime.now().strftime('%Y-%m-%d-%H%M%S') + ".txt"
    file_log = open(os.path.join(destination, log_name), 'a+')
    print("---------------- " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " ----------------",
          file=file_log)
    print('Tasks queried: ' + tasks, file=file_log)

    tasks = tasks.split(',')
    tasks = [t.replace(' ', '') for t in tasks]  # Remove white space
    # Go thru participant files in ROOTDIR & look for tasks
    for p in os.listdir(rootdir):  # For each participant directory:
        partic_dir = os.path.join(rootdir, p)
        for dirs in os.listdir(partic_dir):  # For each visit-directories:
            # select the task directories to copy
            task_dirs = os.listdir(os.path.join(partic_dir, dirs))  # List task directories
            task_dirs[:] = [x for x in task_dirs if x in tasks]  # Reduce TASK_DIRS to include TASKS that user queries
            if not task_dirs:  # If the list is empty
                print(os.path.relpath(partic_dir, rootdir) + ",Does not have tasks in subdirectories", file=file_log)
            else:
                for t in task_dirs:  # For each task sub-directory
                    dir_to_copy = os.path.join(partic_dir, dirs, t)
                    visit_path = Path(dir_to_copy)  # Get the visit folder ID
                    visit_dir = os.path.basename(visit_path.parent)
                    if keepBIDS is True:
                        dest_dir = os.path.join(destination, p, visit_dir, t)
                        # Copy the task directory, if it does not exist
                        if not os.path.exists(dest_dir):
                            shutil.copytree(src=dir_to_copy, dst=dest_dir)
                            print(os.path.relpath(dir_to_copy, rootdir) + ",Copied", file=file_log)
                        else:
                            print(os.path.relpath(dir_to_copy, rootdir) + ",Skipped", file=file_log)
                    else:  # Re-organize so each session is its own directory
                        # Create destination directory for this visit
                        visit_num = re.sub("[^0-9]", "", visit_dir)
                        dest_dir = os.path.join(destination, p + "_" + visit_num)
                        # Create folder for visit if it does not exist
                        if not os.path.exists(dest_dir):
                            os.mkdir(dest_dir)
                        files_to_copy = os.listdir(dir_to_copy)
                        for f in files_to_copy:
                            task_file = dir_to_copy + "/" + f
                            # Copy .tsv if not already there
                            if not os.path.exists(os.path.join(dest_dir, f)):
                                shutil.copy(src=dir_to_copy + "/" + f, dst=dest_dir)
                                print(os.path.relpath(task_file, rootdir) + ",Copied", file=file_log)
                            else:
                                print(os.path.relpath(task_file, rootdir) + ",Skipped", file=file_log)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description="Pull data from Elab box for specific eye-tracking tasks")

    ap.add_argument("-rootdir", required=True, type=str,  # Can use -d or --rootdir flag
                    help="path to parent directory for project containing eye tracking files")
    ap.add_argument("-destination", required=True, type=str,
                    help="Where data should be copied to")
    ap.add_argument("-tasks", required=True, type=str,
                    help="e.g. Calibration_Verification, EU-AIMS_counter_1, EU-AIMS_counter_2")
    ap.add_argument("-keepBIDS", required=False, type=int, default=0,
                    help="Keep BIDS format?")

    args = ap.parse_args()
    main(args.rootdir, args.destination, args.tasks, args.keepBIDS)


