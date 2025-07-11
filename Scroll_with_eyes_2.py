import cv2 as cv
import Face_detection_module as fdm
import time
import pyautogui as pg

cap = cv.VideoCapture(0)
detector = fdm.FaceDetector(min_det_con=0.8)

previous_time = 0

while True:
    success, img = cap.read()
    img = cv.flip(img, 1)
    img, bbox = detector.find_face(img, draw=False)
    img, faces = detector.faceMesh(img)
    
    length1 = detector.findDistance(145, 468)   # lower eyelid and iris
    length2 = detector.findDistance(159, 468)   # Upper eyelid and iris
    
    if (length1 > length2):     # User watching upwards
        # Scroll up
        time.sleep(2)
        while True:
            pg.scroll(100)
            
    if (length2 > length1):     # User watching downwards 
        # Scroll down
        time.sleep(2)
        while True:
            pg.scroll(-100)
            
    current_time = time.time()
    fps = 1 / (current_time - previous_time)
    previous_time = current_time
    cv.putText(img, str(int(fps)), (10, 70), cv.FONT_HERSHEY_COMPLEX, 3, (255, 255, 0), 2)
    
    cv.imshow("Webcam", img)
    cv.waitKey(2)