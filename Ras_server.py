import numpy as np
import cv2
import time
import autoupload
import glob, os
import boto3
from botocore.exceptions import ClientError
import logging
s3= boto3.client('s3')
# haar_face_cascade = cv2.CascadeClassifier('/home/pi/project/opencvlb/data/haarcascades/haarcascade_frontalface_default.xml')
haar_face_cascade = cv2.CascadeClassifier('/home/pi/project/opencvlb/data/haarcascades/haarcascade_upperbody.xml')

video = cv2.VideoCapture(0)  

fps =10 #video.get(cv2.CAP_PROP_FPS)
#코덱 정의 및 videoWriter 개체 생성
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
DetectCount=0
FrameCount=0
delay =round(1000/fps)
recordtime= fps *5


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


def upload_main():

    files = dict(video=[],_10KB=[],_1MB=[],_10MB=[])
    bucket_name= 'rascctvfcc104c288914011a034d2bb441de7b742257-staging'

    os.chdir("./video")
    for file in glob.glob("*.mp4"):
        files["_10MB"].append(file)

    for key,value in files.items():
        for filename in value:
            upload_file(filename,bucket_name)
    os.chdir("..")


while True:

    check, frame = video.read()
    #frame= cv2.flip(frame,-1) # flip camera vertically
    #print(frame)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    body = haar_face_cascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5, minSize=(70, 70));
    for (x, y, w, h) in body:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 3)
        DetectCount+=1
        FrameCount =0
        
    if DetectCount == 1:
        save_name = time.strftime("video/%Y-%m-%d-%H시%M분%S초.mp4");
        out = cv2.VideoWriter(save_name ,fourcc, fps, (640,480),True);
        out.write(frame)
        print(save_name+' frame write start')
        DetectCount+=1
        
    elif DetectCount>=1 and FrameCount<recordtime:
        out.write(frame)

    elif DetectCount>=1 and FrameCount>=recordtime:
        out.release()
        print(save_name+"is released")
        upload_main()
        print("file uploaded")
        FrameCount=-1
        DetectCount=0
        

    FrameCount+=1
    # cv2.imshow("Face Detector", frame)

    # key = cv2.waitKey(delay)    
    # if key == ord('q') or key == ord('Q'):
    #     print("종료키 입력받음 -upload file")
      
    #     upload_main()
    #     break


video.release()
cv2.destroyAllWindows()


