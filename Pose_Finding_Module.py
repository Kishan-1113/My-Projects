import time
import cv2 as cv
import mediapipe as mp
import math


class PoseDetector():
    def __init__(self,mode = False, model_complx = False,smooth_land = False,enable_seg = False,
                 smooth_seg = True,mindetectCon = 0.5,trackCon = 0.5):
        self.mode = mode
        self.model_complx = model_complx
        self.smooth_land = smooth_land
        self.enable_seg = enable_seg
        self.smooth_seg = smooth_seg
        self.mindetectCon = mindetectCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode,self.model_complx,self.smooth_land,self.enable_seg,
                                     self.smooth_seg,self.mindetectCon,self.trackCon)



    def findpose(self,img,draw = True):
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.result = self.pose.process(imgRGB)
        # print(result.pose_landmarks)
        lst = []

        if (self.result.pose_landmarks):
            if draw:
                self.mpDraw.draw_landmarks(img,self.result.pose_landmarks,self.mpPose.POSE_CONNECTIONS)

        return img      # Returns an image


    def getPoints(self,img,draw = True):
        self.limlist = []
        if (self.result.pose_landmarks):
            for id,lm in enumerate(self.result.pose_landmarks.landmark):
                h,w,c = img.shape
                #print(id,lm)
                cx,cy = int(lm.x*w), int(lm.y*h)
                self.limlist.append([id,cx,cy])
                if (draw):
                    cv.circle(img,(cx,cy),6,(0,255,0),-1)
        return self.limlist
    
    
    def findangle(self, img, p1, p2, p3, draw = True):
        
        # Get Landmarks
        x1,y1 = self.limlist[p1][1:]
        x2,y2 = self.limlist[p2][1:]
        x3,y3 = self.limlist[p3][1:]
        
        # Get angle
        angle = math.degrees(math.atan2(y3-y2,x3-x2) - math.atan2(y1-y2,x1-x2))
        
        
        # Draws seperately
        if draw:
            cv.line(img,(x1,y1),(x2,y2),(0,0,0),2)
            cv.line(img,(x3,y3),(x2,y2),(0,0,0),2)
            cv.circle(img, (x1,y1), 6, (255,0,0), -1)
            cv.circle(img, (x1,y1), 12, (255,0,0), 2)
            cv.circle(img, (x2,y2), 6, (255,0,0), -1)
            cv.circle(img, (x2,y2), 12, (255,0,0), 2)
            cv.circle(img, (x3,y3), 6, (25,0,0), -1)
            cv.circle(img, (x3,y3), 12, (255,0,0), 2)
            
            cv.putText(img,str(int(abs(angle))),(x2-20,y2+20),cv.FONT_HERSHEY_PLAIN,
                       1,(255,255,255),2)
        return angle
                

def main():
    capture = cv.VideoCapture("Pose estimation vide.mp4")
    previous_time = 0
    detector = PoseDetector()
    while True:
        success, img = capture.read()
        img = detector.findpose(img)
        lmlist = detector.getPoints(img)
        if (len(lmlist) != 0):
            print(lmlist[14])
            cv.circle(img,(lmlist[14][1],lmlist[14][2]),15,(0,0,255),-1)

        current_time = time.time()
        fps = 1 / (current_time - previous_time)
        previous_time = current_time
        cv.putText(img, str(int(fps)), (10, 70), cv.FONT_HERSHEY_COMPLEX, 3, (255, 255, 0), 2)

        cv.imshow("Video", img)
        cv.waitKey(5)

if __name__ == "__main__":
        main()