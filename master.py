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
import os
import sys
import shutil
import glob
import ntpath

## define configurations
with open ( "C:\Scripts\Bucket_role_info.json") as data_file:
  data=json.load(data_file)
data_file.close()

bucket_name=data["Para"][0]["BUCKET"]
current_process_folder_s3=" s3://"+bucket_name+"/folder/current_process/raw/"
Tran_File="C:/SrcFiles/TRANSACTIONS.txt"
Manifest_file_path="C:/Scripts/manifest_creation.py"

s3 = boto3.resource('s3')
bucket=s3.Bucket(bucket_name)

File_name_s3="C:/SrcFiles/S3.txt"
File_name_ec2="C:/SrcFiles/ec2.txt"
File_name_diff="C:/SrcFiles/Diff_S3_ec2.txt"
s3_File=open (File_name_s3,'w')

with open(Tran_File,"r") as Tran:
 for line1 in Tran:
  line=line1.strip()
  line_folder=line.split('/')[0]
  line_file=line.split('/')[1]
  print("######## Processing started for "+line+"#########")

 
  Bucket_Prefix=line_folder+"/raw/"+line_file
  print(Bucket_Prefix)

##End Configuration


  
  for file in bucket.objects.filter(Prefix=Bucket_Prefix):
     s3_File.write(bucket.name+'/'+file.key)
     print(file)
    #s3_File.write(file)
     s3_File.write("\n")
s3_File.close()
with open(File_name_s3, 'r') as t1, open(File_name_ec2, 'r') as t2:
    fileone = t1.readlines()
    filetwo = t2.readlines()
    
########## COMPARE S3 AND EC2 FILE AND COPY S3 FILE 

with open(File_name_diff, 'w') as outFile:
     for line_one in fileone:
      if line_one not in filetwo:
        outFile.write(line_one)



########## UPDATE LOCAL EC2 COPY WITH LATEST S3 FILE NAMES

with open(File_name_s3, 'r') as s3_file:
    with open(File_name_ec2, 'w') as ec2_file:
      for line in s3_file:
        ec2_file.write(line)
ec2_file.close()
#print ("Step 5: Local ec2 copy has been updated")
#print("******************************************")


########################Calling Manifest file creation python###############
print("Manifest file creating process started!!")
os.system ("python "+Manifest_file_path)
print("Manifest file creating and copying to S3 proces done!!")
