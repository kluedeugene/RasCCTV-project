import numpy as np
import cv2
import time
import autoupload
import glob, os
import boto3
from botocore.exceptions import ClientError
import logging
from pyfcm import FCMNotification

APIKEY = 
 
TOKEN = 
 
s3= boto3.client('s3')
# haar_face_cascade = cv2.CascadeClassifier('/home/pi/project/opencvlb/data/haarcascades/haarcascade_frontalface_default.xml')
haar_face_cascade = cv2.CascadeClassifier('/home/pi/project/opencvlb/data/haarcascades/haarcascade_upperbody.xml')

video = cv2.VideoCapture(0)  

fps =10       #video.get(cv2.CAP_PROP_FPS)
#코덱 정의 및 videoWriter 개체 생성
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
DetectCount=0
FrameCount=0
delay =round(1000/fps)
recordtime= fps *10
thresh= 25
max_diff= 5
a,b,c,=None,None,None

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

    print(os.getcwd())
    os.chdir("/home/pi/project/fdcam/video")
    print(os.getcwd())

    for file in glob.glob("*.mp4"):
        
        files["_10MB"].append(file)

    for key,value in files.items():
        for filename in value:
            upload_file(filename,bucket_name)
    os.chdir("..")
    print(os.getcwd())


#Fcm 푸시알림
push_service = FCMNotification(APIKEY)
def FcmPushNotification(body,title):
    # 메시지 (data 타입)
    data_message = {
        "body": body, 
        "title": title
    }
 
    # 토큰값을 이용해 1명에게 푸시알림을 전송함
    #message_body is notification part
    result = push_service.notify_multiple_devices(registration_ids=TOKEN,message_body=body, data_message=data_message)
 
    # 전송 결과 출력
    print(result)





check, a=video.read()
check, b=video.read()

while True:

    check, c = video.read()
    draw= c.copy()
    a_gray = cv2.cvtColor(a, cv2.COLOR_BGR2GRAY)
    b_gray = cv2.cvtColor(b, cv2.COLOR_BGR2GRAY)
    c_gray = cv2.cvtColor(c, cv2.COLOR_BGR2GRAY)

    diff1 = cv2.absdiff(a_gray, b_gray)
    diff2 = cv2.absdiff(b_gray, c_gray)

    ret, diff1_t = cv2.threshold(diff1, thresh, 255, cv2.THRESH_BINARY)
    ret, diff2_t = cv2.threshold(diff2, thresh, 255, cv2.THRESH_BINARY)

    diff = cv2.bitwise_and(diff1_t, diff2_t)

    k = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    diff = cv2.morphologyEx(diff, cv2.MORPH_OPEN, k)

    diff_cnt = cv2.countNonZero(diff)
    if diff_cnt > max_diff:
        nzero = np.nonzero(diff)
        cv2.rectangle(draw, (min(nzero[1]), min(nzero[0])),
                      (max(nzero[1]), max(nzero[0])), (0, 255, 0), 2)
        DetectCount+=1
        FrameCount =0

        '''
        rectangle: pt1, pt2 기준으로 사각형 프레임을 만들어줌.
        nzero: diff는 카메라 영상과 사이즈가 같으며, a, b프레임의 차이 어레이를 의미함.
        (min(nzero[1]), min(nzero[0]): diff에서 0이 아닌 값 중 행, 열이 가장 작은 포인트
        (max(nzero[1]), max(nzero[0]): diff에서 0이 아닌 값 중 행, 열이 가장 큰 포인트
        (0, 255, 0): 사각형을 그릴 색상 값
        2 : thickness
        '''

        cv2.putText(draw, "Motion detected!!", (10, 30),
                    cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255))
 
    stacked = np.hstack((draw, cv2.cvtColor(diff, cv2.COLOR_GRAY2BGR)))
  #  cv2.imshow('motion', stacked)
 
    a = b
    b = c
 
    if cv2.waitKey(1) & 0xFF == 27:
        break


        
    if DetectCount == 1:
        save_name = time.strftime("/home/pi/project/fdcam/video/%Y-%m-%d-%H시%M분%S초.mp4");
        out = cv2.VideoWriter(save_name ,fourcc, fps, (640,480),True);
        out.write(draw)
        print(save_name+' frame write start')
        DetectCount+=1
        
    elif DetectCount>=1 and FrameCount<recordtime:
        out.write(draw)

    elif DetectCount>=1 and FrameCount>=recordtime:
        out.release()
        print(save_name+"is released")
        upload_main()
        print("file uploaded")
        FcmPushNotification("RasCCTV detect Motion" , "RasCCTV detect Motion" )
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


