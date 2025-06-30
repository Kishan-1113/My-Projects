import cv2 as cv
import mediapipe as mp
import time

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
        lmlist = []

        if (self.result.multi_hand_landmarks):
            if len(self.result.multi_hand_landmarks) > handNo:
                myhand = self.result.multi_hand_landmarks[handNo]
                for id, lm in enumerate(myhand.landmark):
                    # print(id,lm)
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                   # print(id, cx, cy)
                    lmlist.append([id,cx,cy])

                    #if (id == 0 or id == 4 or id == 8 or id == 12):
                    if (draw):
                        cv.circle(img, (cx, cy), 15, (250, 250, 0), -1)
        return lmlist   # Returns all those values or coordinates of landmarks

def main():
    current_Time = 0
    previous_Time = 0
    detector = HandDetector()
    capture = cv.VideoCapture(0)
    while True:
        success, img = capture.read()
        img = detector.findHands(img)
        lmlist = detector.findposition(img)
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