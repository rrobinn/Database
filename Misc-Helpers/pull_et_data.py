import argparse
import shutil
import os
from pathlib import Path

'''configuration: pull_et_data.py --rootdir
/Users/sifre002/Box/Elab_ET_Data/BCP_BSLERP/AUDIT_PASSED/
--destination
/Users/sifre002/Desktop/data/
--tasks
Calibration_Verification,EU-AIMS_counter_1 '''

'''  
def getListOfSubDirs(dirname):
    # create list of subdirs
    file_list = os.listdir(dirname)
    all_subdirs = list()
    for entry in file_list:
        full_path = os.path.join(dirname, entry)
        if os.path.isdir(full_path): # If full_path is a directory
            all_subdirs.append(os.path.relpath(full_path, dirname)) # append to list of directories
            all_subdirs=all_subdirs + getListOfSubDirs(full_path) # Recursively check if there is a sub-dir
    return all_subdirs '''

def main(rootdir, destination, tasks):
    # Copy specific eye-tracking tasks

    # Create the destination directory for all ET files if it does not exist
    if not os.path.exists(destination):
        os.mkdir(destination)

    tasks=tasks.split(',')

    # Go thru participant files & look for tasks
    for p in os.listdir(rootdir): # For each participant directory
        partic_dir=os.path.join(rootdir, p)
        for dirs in os.listdir(partic_dir): # For each visit-directories,select the task directories to copy
            task_dirs = os.listdir(os.path.join(partic_dir,dirs))
            task_dirs[:] = [x for x in task_dirs if x in tasks]
            for t in task_dirs:
                file_to_copy = os.path.join(partic_dir, dirs, t)
                path = Path(file_to_copy) # Get the visit folder ID
                visit_dir = os.path.basename(path.parent)
                shutil.copytree(src=file_to_copy, dst=os.path.join(destination, p, visit_dir, t))



if __name__ == '__main__':
    ap=argparse.ArgumentParser(
        description="Pull data from Elab box for specific eye-tracking tasks")
    ap.add_argument("-d", "--rootdir", required=True, type=str, # Can use -d or --rootdir flag
                    help="path to parent directory for project containing eye tracking files")
    ap.add_argument("--destination", required=False, type=str,
                    help="Where data should be copied to")

    ap.add_argument("--tasks", required=False, type=str,
                    help="e.g. Calibration_Verification, EU-AIMS_counter_1, EU-AIMS_counter_2")

    args=ap.parse_args()
    main(args.rootdir, args.destination, args.tasks)
