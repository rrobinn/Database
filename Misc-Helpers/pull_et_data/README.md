`pull_et_data.py`  

Script pulls specific eye-tracking tasks, maintaining the folder structure (`Individual/Visit/Task/my_file.tsv`)  


The script expects the following arguments:  
- <b>--rootdir</b>: Directory where ET data are (e.g. `Box/Elab_ET_Data/BCP_BSLERP/AUDIT_PASSED/`)  
- <b> --destination</b>: Destination directory where data will be moved. 
- <b>--tasks</b>:  Task(s) list. Comma separated. (e.g. `Calibration_Verification,EU-AIMS_counter_1,EU-AIMS_counter_2`  
- <b>-keepBIDS</b>: Optional flag. If included, directories will be kept in BIDS-style organization. Otherwise, they will be organized into a directory for each session/visit.  



## Example of command line execution
`python3 pull_et_data.py --rootdir ~/Box/Elab_ET_Data/BCP_BSLERP/AUDIT_PASSED --destination ~/Box/sifre002/7_MatFiles/01_Complexity/Individual_Data/20201112data/Session --tasks Calibration_Verification,EU-AIMS_counter_1,EU-AIMS_counter_2 -keepBIDS False`
