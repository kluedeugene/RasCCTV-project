import numpy as np
import cv2
import time

haar_face_cascade = cv2.CascadeClassifier('/home/pi/project/opencvlb/data/haarcascades/haarcascade_frontalface_default.xml')
video = cv2.VideoCapture(0)  
a = 0
fps = video.get(cv2.CAP_PROP_FPS)
#코덱 정의 및 videoWriter 개체 생성
fourcc = cv2.VideoWriter_fourcc(*'DIVX')

save_name = time.strftime("video/%Y-%m-%d-%H시%M분%S초.mp4");
out = cv2.VideoWriter(save_name ,fourcc, 3, (640,480),False);

#out = cv2.VideoWriter('output.avi',fourcc, 3, (640,480))

detectcount=0
while True:


    a = a + 1    
    check, frame = video.read()
    frame= cv2.flip(frame,-1) # flip camera vertically

    print(frame)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = haar_face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5);
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
        detectcount+=1
        
    if detectcount >= 1:
        out.write(frame)
    
    cv2.imshow("Face Detector", frame)


    key = cv2.waitKey(1)    
    if key == ord('q'):
        break

print(a)

video.release()
out.release()
cv2.destroyAllWindows()