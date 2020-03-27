####################################################################
##########   Script name: Manifest_File_Creation.py
##########   Created on : 8th Aug 2019
##########   Created by : sandeep kumar
##########   Version: 1.0
####################################################################



import boto3
import awscli
import os
import glob
from awscli.clidriver import create_clidriver
import json
import subprocess
import datetime

## define configurations
with open ( "C:\Scripts\Bucket_role_info.json") as data_file:
  data=json.load(data_file)
data_file.close()

bucket_name=data["Para"][0]["BUCKET"]
current_process_folder_s3=" s3://"+bucket_name+"/folder/current_process/raw/"
Src_File="C:/SrcFiles/file_prefix.txt"
diff_file="C:/SrcFiles/Diff_S3_ec2.txt"
Manifest_Files_Loc="C:/SrcFiles/Manifest_Folder/"

######Remove manifest files of last load#############
os.system (" aws s3 rm "+current_process_folder_s3+" --recursive --exclude * --include *.manifest")


diff_list=open(diff_file,'r',newline='\r\n')
diff_list_1=list(open(diff_file,'r',newline='\r\n'))
size = len(diff_list_1)
print(size)


with open(Src_File,"r",newline='\n') as Src:
 for file_raw in Src:
  file=file_raw.strip()
  
  print(file)
  File_name_s3=Manifest_Files_Loc+file+".manifest"   
  with open (File_name_s3,'w') as s3_File:
     s3_File.write("{\n\"entries\":[\n")
     
     i=0
     for file_ec2  in diff_list_1:
       
       print(file_ec2)
      #print (file)
      #print(file)
       if file in file_ec2:
         if i>0:
          s3_File.write(",")
          s3_File.write("\n")
        #s3_File.write(file_ec2)
         s3_File.write("{\"url\":\"s3://"+file_ec2.strip('\r\n')+"\"}")
         i=i+1
         
     
#####Finish adding comma##   
     s3_File.write(" \n]\n}")
s3_File.close()
  

   
   
####Move Manifest files from Ec2 to S3 bucket##############
os.system('aws s3 cp '+Manifest_Files_Loc+' '+ current_process_folder_s3 +' --recursive')
