import numpy as np
import time 
import Pose_Estimation_Module as pm
import cv2 as cv

cap = cv.VideoCapture(r"C:\Users\kally\OneDrive\Desktop\kishan python\Advanced OpenCV\gym video.mp4")
#cap = cv.imread(r"C:\Users\kally\OneDrive\Desktop\kishan python\Advanced OpenCV\gym_photo.jpg")

detector = pm.PoseDetector()

count = 0
dir = 0
ptime = 0

while True:
    success, img = cap.read()
    img = cv.resize(img, (500,720))
    #img = cv.imread(r"C:\Users\kally\OneDrive\Desktop\kishan python\Advanced OpenCV\gym3.jpg")
    #img = cv.resize(img,(700,720))
    img = detector.findpose(img,draw=False)
    lmlist = detector.getPoints(img,draw=False)
    angle = detector.findangle(img,24,26,28)
    
    per = np.interp(angle,(196,280),(0,100))
    
    if per == 100:
        if (dir == 0):
            count += 0.5
            dir = 1
    
    if per == 0:
        if (dir == 1):
            count += 0.5
            dir = 0
            
    print(count)
    cv.rectangle(img,(30,610),(90,670),(0,255,0),2)
    cv.putText(img,f"{int(count)}",(50,650),cv.FONT_HERSHEY_COMPLEX,
                       1,(0,0,255),2)
    
    #print(int(angle), int(per))
    #print(lmlist[11],lmlist[13],lmlist[15])
    ctime = time.time()
    fps = 1 / (ctime - ptime) if ptime else 0
    ptime = ctime
    cv.putText(img, f'FPS: {int(fps)}', (10, 40), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    cv.imshow("Video",img)
    cv.waitKey(2)