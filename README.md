# create_manifest
 This script will create a manifest file for latest files uploaded into s3 for dumping data into redshift using copy command.
 
 
# Manifest file: 
This file is of json format which will have list of files to be processed into redshift.
Copy command will understand this manifest file and pic the files to be loaded.

# working of script:

1. Python will use Boto3 sdk to interact with AWS services.
2. This Master script will loop into TRANSACTIONS.txt files which is of format Folder/file_prefix
3. For each folder in that bucket it will get the files based on prefix of the file. 
4. now we have all the files which belongs to that prefix we load then to s3.txt
5. and compare with ec2.txt which will have previous load.
6. s3.txt minus ec2.txt will have the latest files.
7. manifest_creation.py will create manifest file for all prefics
