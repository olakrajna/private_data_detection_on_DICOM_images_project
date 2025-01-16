

import matplotlib.pyplot as plt 
import pydicom 
import pydicom.data 
  
# Full path of the DICOM file is passed in base 
base = r"case2"
pass_dicom = "97_r5_56082495.dcm"  # file name is 1-12.dcm 
  
# enter DICOM image name for pattern 
# result is a list of 1 element 
filename = pydicom.data.data_manager.get_files(base, pass_dicom)[0] 
  
ds = pydicom.dcmread(filename) 
  
