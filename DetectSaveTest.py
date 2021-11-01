import numpy as np
import cv2
import time

haar_face_cascade = cv2.CascadeClassifier('/home/pi/project/opencvlb/data/haarcascades/haarcascade_frontalface_default.xml')
video = cv2.VideoCapture(0)  

fps =video.get(cv2.CAP_PROP_FPS)
#코덱 정의 및 videoWriter 개체 생성
fourcc = cv2.VideoWriter_fourcc(*'XVID')

#save_name = time.strftime("video/%Y-%m-%d-%H시%M분%S초.mp4");
#out = cv2.VideoWriter(save_name ,fourcc, 3, (640,480),False);

#out = cv2.VideoWriter('output.avi',fourcc, 3, (640,480))

DetectCount=0
FrameCount=0
while True:


     
    check, frame = video.read()
    #frame= cv2.flip(frame,-1) # flip camera vertically

    print(frame)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = haar_face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5);
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
        DetectCount+=1
        FrameCount =0
        
    if DetectCount == 1:
        save_name = time.strftime("video/%Y-%m-%d-%H시%M분%S초.mp4");
        out = cv2.VideoWriter(save_name ,fourcc, 50, (640,480),True);
        out.write(frame)
        print('frame write')
        
    elif DetectCount>=1 and FrameCount<100:
        out.write(frame)

    elif DetectCount>=1 and FrameCount==100:
        out.release()
        FrameCount=0
        DetectCount=0
        
   
    
    FrameCount+=1
    cv2.imshow("Face Detector", frame)

    key = cv2.waitKey(1)    
    if key == ord('q') or key == ord('Q'):
        break

video.release()
cv2.destroyAllWindows()
