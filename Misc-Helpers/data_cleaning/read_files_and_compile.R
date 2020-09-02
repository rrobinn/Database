# first time you run:
install.packages('tidyverse')

library(tidyverse)

###########################
# FILL THIS PART IN 
###########################
my_dir = '/Users/sifre002/Box/sifre002/9_ExcelSpreadsheets/03_EyeBlink_ValidationStudy/Adults/BlinkTimes_Hand/' # Directory with your files
my_ext = '.csv' # file extension (.csv, .xlsx, etc)


# list of everyone's blinks files
files = list.files(my_dir, pattern =my_ext)

# Loop thru the files and read them in 
out = list() # make list to store data in 
for (f in files) {
  if (my_ext == '.csv') {
    dat = read.csv( file = paste(my_dir,f,sep='') )
  } else{
    dat = read_xlsx(path = paste(my_dir,f,sep='') )
  }
  out[[f]] = dat
}



my_df = do.call(rbind, out) # convert list to data.frame
