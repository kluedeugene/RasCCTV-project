import glob, os
import boto3
from botocore.exceptions import ClientError
import logging
s3= boto3.client('s3')

#s3= boto3.client('s3')
def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = 'public/'+file_name

    # Upload the file
    try:
        s3.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


files = dict(video=[],_10KB=[],_1MB=[],_10MB=[])
bucket_name= 'rascctvfcc104c288914011a034d2bb441de7b742257-staging'

os.chdir("./video")
for file in glob.glob("*.txt"):
    files["_10MB"].append(file)

for key,value in files.items():
    for filename in value:
       upload_file(filename,bucket_name)
