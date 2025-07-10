import cv2 as cv
import numpy as np
import time 
import os
import Hand_Tracking_module as htm

folderPath = r"C:\Users\kally\OneDrive\Desktop\kishan python\Advanced OpenCV\Paint_brushes"
mylist = os.listdir(folderPath) 
# print(mylist)

overlaylist = []
for impath in mylist:
    image = cv.imread(f"{folderPath}\\{impath}")
    overlaylist.append(image)
    
# print(len(overlaylist))
# print(overlaylist)

# In my case, webcam and overlay was of different sizes
header = overlaylist[0]

###############################
brushThickness = 15
eraserThickness = 100
xp, yp = 0, 0
drawColor = (255,0,255)
###########################

# Resizing the image to fit properly
header = cv.resize(header,(1280,125))


cap = cv.VideoCapture(0)
detector = htm.HandDetector(detectionCon=0.85)

imgCanvas = np.zeros((720, 1280, 3), np.uint8)

cap.set(3, 1280)
cap.set(4, 720)
ptime = 0
while True:
    # 1. Import the image
    success, img = cap.read()
    img = cv.flip(img,1)
    
    # 2. Find the landmarks
    img = detector.findHands(img)
    lmlist = detector.findposition(img, draw=False)
    
    if (len(lmlist) != 0):
        
        x1,y1 = lmlist[8][1:]
        x2,y2 = lmlist[12][1:]
        
        # if (lmlist[8][2] < lmlist[6][2]):
        #     print("Index up")
        # else:
        #     print("Index down")
            
    # 3. Check which fingers are up
        fingers = detector.fingersUp()
    
    # Will draw if only one finger is up, and will move if two fingers are up (won't draw)
    # 4. Selection mode - Two fingers are up

        # Selection mode
        if (fingers[1] and fingers[2]):
            xp, yp = 0, 0
            print("Selection mode")
            
            if (y1 < 125):      # => Means we are in the clicking zone
                
                # --------     Sizing the image played a crucial role    ----------
                
                if (250 < x1 < 450):    # => Means we are clicking the first brush
                    header = overlaylist[0]
                    header = cv.resize(header,(1280,125))
                    drawColor = (255,255,0)
                    
                elif (550 < x1 < 750):    # => Means we are clicking the second brush
                    header = overlaylist[1]
                    header = cv.resize(header,(1280,125))
                    drawColor = (0,255,0)
                    
                elif (800 < x1 < 950):    # => Means we are clicking the third brush
                    header = overlaylist[2]
                    header = cv.resize(header,(1280,125))
                    drawColor = (255,0,0)
                    
                elif (1050 < x1 < 1200):    # => Means we are clicking the fourth brush
                    header = overlaylist[3]
                    header = cv.resize(header,(1280,125))
                    drawColor = (0,0,0)
                    
            cv.rectangle(img, (x1,y1-25), (x2,y2+25), drawColor, -1)
        
        # Drawing mode
        if (fingers[1] and fingers[2] == False):
            cv.circle(img, (x1,y1), 7, drawColor, -1)
            print("drawing mode")
            
            # This condition checks, not to draw anything when it is the first frame
            # If you don't have this condition, it will draw a line directly from
            # the (0,0), which is annoying, You can check by commenting it out
            if (xp == 0) and (yp == 0):
                xp, yp = x1, y1
                
            
            if (drawColor == (0,0,0)):
                cv.line(img,(xp,yp), (x1,y1), drawColor, eraserThickness)
                cv.line(imgCanvas,(xp,yp), (x1,y1), drawColor, eraserThickness)
            
            else:
                cv.line(img,(xp,yp), (x1,y1), drawColor, brushThickness)
                cv.line(imgCanvas,(xp,yp), (x1,y1), drawColor, brushThickness)
            
            xp, yp = x1, y1
        
    # 5. Drawing mode - Only index finger is up
    
    # Another method to achieve drawing on the same image
    imgGray = cv.cvtColor(imgCanvas, cv.COLOR_BGR2GRAY)
    _, imgInv = cv.threshold(imgGray, 50, 250, cv.THRESH_BINARY_INV)
    imgInv = cv.cvtColor(imgInv, cv.COLOR_GRAY2BGR)
    
    img = cv.bitwise_and(img,imgInv)
    img = cv.bitwise_or(img, imgCanvas)
    
    
    ctime = time.time()
    fps = 1 / (ctime - ptime) if ptime else 0
    ptime = ctime
    cv.putText(img, f'fps: {int(fps)}', (10, 700), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    img[0:125, 0:1280] = header
    
    # # ___________ This is method 1  ______________
    
    # # This method blends the two images together and tries to merge them into 
    # # a single image, but it has transparency and blended effects
    # img = cv.addWeighted(img, 0.5, imgCanvas, 0.5,0)
    
    cv.imshow("Webcam", img)
    cv.imshow("ImageCanvas", imgCanvas)
    cv.waitKey(1)