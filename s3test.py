import boto3
import glob
import os.path

s3= boto3.client('s3')

# for bucket in s3.buckets.all():
#     print(bucket.name)

filename= "test.avi"
newfilename="outputnew.avi"
bucket_name= 'yujinbucket01'

key= 'video/test.avi'
# 첫 번째 매개변수 : 로컬에서 올릴 파일이름
# 두 번째 매개변수 : S3 버킷 이름
# 세 번째 매개변수 : 버킷에 저장될 파일 이름.
s3.upload_file(filename, bucket_name, key)

#s3.download_file(bucket_name,key,newfilename)



