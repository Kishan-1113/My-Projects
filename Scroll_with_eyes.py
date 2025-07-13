import cv2 as cv
import Face_Detection_Module as fdm
import time
import pyautogui as pg

cap = cv.VideoCapture(0)
detector = fdm.FaceDetector(min_det_con=0.8)

previous_time = 0
last_scroll_time = 0
scroll_cooldown = 0.7  # seconds

while True:
    success, img = cap.read()
    img = cv.flip(img, 1)
    img, bbox = detector.find_face(img, draw=False)
    img, faces = detector.faceMesh(img)

    current_time = time.time()

    # Only scroll every 0.7 seconds to avoid rapid triggers
    if current_time - last_scroll_time > scroll_cooldown and faces:
        length1 = detector.findDistance(145, 468)   # Lower eyelid and iris
        length2 = detector.findDistance(159, 468)   # Upper eyelid and iris

        if length1 > length2 + 2:  # Look up
            pg.scroll(100)
            last_scroll_time = current_time

        elif length2 > length1 + 2:  # Look down
            pg.scroll(-100)
            last_scroll_time = current_time

    # FPS display
    fps = 1 / (current_time - previous_time)
    previous_time = current_time
    cv.putText(img, str(int(fps)), (10, 70), cv.FONT_HERSHEY_COMPLEX, 3, (255, 255, 0), 2)

    cv.imshow("Webcam", img)
    cv.waitKey(1)
