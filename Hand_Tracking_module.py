import cv2 as cv
import mediapipe as mp
import time
import math

class HandDetector():

    def __init__(self,mode = False, maxhands = 2, detectionCon = 0.5, trackCon = 0.5):
        self.mode = mode
        self.maxhands = maxhands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=self.mode,max_num_hands=self.maxhands,
                                        min_detection_confidence=self.detectionCon,
                                        min_tracking_confidence=self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        
        self.tipIds = [4,8,12,16,20]


    def findHands(self,img, draw = True):
        imgRBG = cv.cvtColor(img,cv.COLOR_BGR2RGB)
        self.result = self.hands.process(imgRBG)
        #  print(result.multi_hand_landmarks)

        if (self.result.multi_hand_landmarks):
            for handlms in self.result.multi_hand_landmarks:
                if (draw):
                    self.mpDraw.draw_landmarks(img,handlms,self.mpHands.HAND_CONNECTIONS)

        return img


    def findposition(self,img,handNo = 0, draw = True):
        
        xlist = []
        ylist = []
        bbox = []
        
        self.lmlist = []

        if (self.result.multi_hand_landmarks):
            if len(self.result.multi_hand_landmarks) > handNo:
                myhand = self.result.multi_hand_landmarks[handNo]
                for id, lm in enumerate(myhand.landmark):
                    # print(id,lm)
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    
                    xlist.append(cx)
                    ylist.append(cy)
                   # print(id, cx, cy)
                    self.lmlist.append([id,cx,cy])

                    #if (id == 0 or id == 4 or id == 8 or id == 12):
                    if (draw):
                        cv.circle(img, (cx, cy), 8, (250, 250, 0), -1)
                        
                xmin, xmax = min(xlist), max(xlist)
                ymin, ymax = min(ylist), max(ylist)
                bbox = xmin, ymin, xmax, ymax
                
                if draw:
                    cv.rectangle(img, (xmin-20, ymin-20), (xmax+20, ymax+20), (0, 255, 0), 2)
                        
        return self.lmlist, bbox   # Returns all those values or coordinates of landmarks


    def fingersUp(self):
        if not hasattr(self, 'lmlist') or len(self.lmlist) == 0:
            return [0, 0, 0, 0, 0]  # All fingers down (safe default)
        
        fingerId = []
        
        # Checks for thumb finger (checks the x-coordinates)
        if (self.lmlist[self.tipIds[0]][1] < self.lmlist[self.tipIds[0]-1][1]): 
            fingerId.append(1)
        else: 
            fingerId.append(0)
        
        # Checks the other fingers (checks the y-coordinates)
        for id in range(1,5):
            if (self.lmlist[self.tipIds[id]][2] < self.lmlist[self.tipIds[id]-2][2]): # If it is greater 
            
            # => finger is closed!
                fingerId.append(1)
            else: 
                fingerId.append(0)
        
        return fingerId
    
    
    def findDistance(self, img, p1, p2, draw=True, r=15, thickness=3):
        
        # Safety check, when there is no hands
        if len(self.lmlist) <= max(p1, p2):
            return img, 0, []
        
        x1, y1 = self.lmlist[p1][1:]
        x2, y2 = self.lmlist[p2][1:]
        
        cx, cy = (x1 + x2)//2, (y1 + y2)//2
        
        if draw:
            cv.line(img, (x1,y1), (x2,y2), (255, 0, 255), thickness)
            cv.circle(img, (x1, y1), r, (255, 0, 255), -1)
            cv.circle(img, (x2, y2), r, (255, 0, 255), -1)
            cv.circle(img, (cx, cy), r, (0, 0, 255), -1)
            
        length = math.hypot(x2-x1, y2-y1)
        
        return img, length, [x1, y1, x2, y2, cx, cy]
            

def main():
    current_Time = 0
    previous_Time = 0
    detector = HandDetector()
    capture = cv.VideoCapture(0)
    while True:
        success, img = capture.read()
        img = cv.flip(img,1)
        img = detector.findHands(img)
        lmlist, bbox = detector.findposition(img,draw=True)
        
        img, lnt, lst = detector.findDistance(img, 8, 12)

        if (len(lmlist) != 0):
            print(lmlist)

        current_Time = time.time()
        fps = 1 / (current_Time - previous_Time)
        previous_Time = current_Time
        cv.putText(img, str(int(fps)), (10, 70), cv.FONT_HERSHEY_COMPLEX, 3, (255, 255, 0), 2)
        cv.imshow("WebCam", img)
        cv.waitKey(1)

if __name__ == "__main__":
    main()