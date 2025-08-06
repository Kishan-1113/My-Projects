import cv2 as cv
from collections import deque
import mediapipe as mp
import time
import math

class HandDetector():

    def __init__(self, mode=False, maxhands=3, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxhands = maxhands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=self.mode, max_num_hands=self.maxhands,
                                        min_detection_confidence=self.detectionCon,
                                        min_tracking_confidence=self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

        self.tipIds = [4, 8, 12, 16, 20]
        self.results = None  # Store results to use across methods

    def findHands(self, img, draw=True):
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

        return img

    def findPositions(self, img, draw=True):
        """
        Returns a list of dictionaries, each containing:
        - 'landmarks': list of [id, x, y]
        - 'bbox': bounding box (xmin, ymin, xmax, ymax)
        """
        hand_data = []
        if not self.results or not self.results.multi_hand_landmarks:
            return []

        for hand_index, handLms in enumerate(self.results.multi_hand_landmarks):
            lmlist = []
            xlist = []
            ylist = []

            h, w, c = img.shape
            for id, lm in enumerate(handLms.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmlist.append([id, cx, cy])
                xlist.append(cx)
                ylist.append(cy)
                if draw:
                    cv.circle(img, (cx, cy), 8, (250, 250, 0), -1)

            xmin, xmax = min(xlist), max(xlist)
            ymin, ymax = min(ylist), max(ylist)
            bbox = (xmin, ymin, xmax, ymax)

            if draw:
                cv.rectangle(img, (xmin - 20, ymin - 20), (xmax + 20, ymax + 20), (0, 255, 0), 2)

            hand_data.append({
                'landmarks': lmlist,
                'bbox': bbox
            })

        return hand_data

    def fingerCount(self, lmlist):
        if not lmlist or len(lmlist) < 21:
            return [0, 0, 0, 0, 0]

        fingers = []

        # Thumb (check x coordinate difference)
        if lmlist[self.tipIds[0]][1] < lmlist[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Other 4 fingers (check y coordinate)
        for id in range(1, 5):
            if lmlist[self.tipIds[id]][2] < lmlist[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers

    def findDistance(self, img, lmlist, p1, p2, draw=True, r=15, thickness=3):
        if len(lmlist) <= max(p1, p2):
            return img, 0, []

        x1, y1 = lmlist[p1][1:]
        x2, y2 = lmlist[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv.line(img, (x1, y1), (x2, y2), (255, 0, 255), thickness)
            cv.circle(img, (x1, y1), r, (255, 0, 255), -1)
            cv.circle(img, (x2, y2), r, (255, 0, 255), -1)

        length = math.hypot(x2 - x1, y2 - y1)
        return img, length, [x1, y1, x2, y2, cx, cy]

class FaceDetector():
    
    def __init__(self, minDetectCon = 0.5,static_img_mode = False,
                 max_num_face = 1, refine_landmark = True,min_det_con = 0.5, min_trac_con = 0.5):
        # Face detection part
        self.minDetectCon = minDetectCon
        self.mpFaceDetection = mp.solutions.face_detection
        self.mpDraw = mp.solutions.drawing_utils
        self.FaceDetection = self.mpFaceDetection.FaceDetection(self.minDetectCon)
        
        # Face mesh part
        self.stat_img_mode = static_img_mode
        self.max_num_face = max_num_face
        self.ref_lndmark = refine_landmark
        self.min_det_con = min_det_con
        self.min_trac_con = min_trac_con

        self.mpFaceMesh = mp.solutions.face_mesh
        self.facemesh = self.mpFaceMesh.FaceMesh(self.stat_img_mode,self.max_num_face,
                                                 self.ref_lndmark, self.min_det_con, self.min_trac_con)
        self.drawSpec = self.mpDraw.DrawingSpec(thickness=1, circle_radius=1, color=(255, 0, 0))

# Reading Image

    def find_face(self,img, draw = True):

        imgRGB = cv.cvtColor(img,cv.COLOR_BGR2RGB)
        self.result = self.FaceDetection.process(imgRGB)
        # print(self.result)

        # bboxs will contain all the information about each face
        bboxs = deque()
        # After each iteration, we gonna append the face information to this list

        if (self.result.detections):             # The whole code below it is
                                                 # only for detecting one face

            for id,detections in enumerate(self.result.detections):
                # Built in function to draw boundaries
                # self.mpDraw.draw_detection(img,detections)

                # Storing all the coordinate values
                bounding_box_C = detections.location_data.relative_bounding_box

                img_h, img_w, c = img.shape

                # Storing exact pixel values by multiplying with image height width in bbc
                bbc = int(bounding_box_C.xmin * img_w),int(bounding_box_C.ymin * img_h), \
                      int(bounding_box_C.width * img_w),int(bounding_box_C.height * img_h)


                bboxs.append([id,bbc,detections.score])

                # Draws by default

                if (draw):
                    img = self.fancyDraw(img,bbc)
                    cv.putText(img, f"{str(int(detections.score[0] * 100))} %",
                               (bbc[0], bbc[1] - 20), cv.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 2)

        return img, list(bboxs)


    def faceMesh(self, img, draw = True):

        self.imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.results = self.facemesh.process(self.imgRGB)

        self.faces = deque()      # Stores the coordinate of landmarks of all the faces detected in the image
        
        # "faces" will be a matrix, storing the landmark point in the format 
        # of faces[face_number][facial_landmark, Means, if you are having multiple 
        # faces in the same frame, you have to extract the coordinates in this way
        
        if (self.results.multi_face_landmarks):
            for facelms in self.results.multi_face_landmarks:
                
                if draw:
                    self.mpDraw.draw_landmarks(img, facelms, self.mpFaceMesh.FACEMESH_TESSELATION,
                                                self.drawSpec, self.drawSpec)
    
                face = deque()      # Store the coordinate of all the facial landmarks (x and y coordinate)
                                # of one face at a time and out of the loop, appends to another matrix
                
                for id, lm in enumerate(facelms.landmark):
                    # print(lm)
                    
                    # To get the pixel values or coordinates
                    ix, iy, ih = img.shape
                    x, y = int(lm.x * ix), int(lm.y * iy)
                    
                    # cv.putText(img, str(id), (x,y), cv.FONT_HERSHEY_PLAIN,
                    #           1, (255, 0, 255), thickness=1)
                    face.append([id,x,y])
                    
                self.faces.append(face)   # This line stores the facial coordinate of all the faces
                
        return img, list(self.faces)


    def findDistance(self, p1, p2, person=0, draw=True):
        # Finds the distance between any two landmarks within the face
        
        x1, y1 = self.faces[person][p1][1:]
        # p1 and p2 are the landmark number to find the distance between
        x2, y2 = self.faces[person][p2][1:]
        
        length = math.hypot(x2-x1, y2-y1)
        
        # if draw:
        #     cv.circle(img, (x1, y1), 5, (255,255,255),-1)
        #     cv.circle(img, (x2, y2), 5, (255,255,255),-1)
        
        return length


    def fancyDraw(self, img, bbc, l = 30,t = 3):
        x,y,w,h = bbc
        x1, y1 = x+w, y+h

        cv.rectangle(img, bbc, (0, 255, 0), 1)
        # Top left corner
        cv.line(img, (x, y), (x + l, y), (255, 0, 255), t)
        cv.line(img, (x, y), (x, y + l), (255, 0, 255), t)

        # Top right corner
        cv.line(img, (x1, y), (x1 - l, y), (255, 0, 255), t)
        cv.line(img, (x1, y), (x1, y + l), (255, 0, 255), t)

        # Bottom left corner
        cv.line(img, (x, y1), (x + l, y1), (255, 0, 255), t)
        cv.line(img, (x, y1), (x, y1 - l), (255, 0, 255), t)

        # Bottom right corner
        cv.line(img, (x1, y1), (x1 - l, y1), (255, 0, 255), t)
        cv.line(img, (x1, y1), (x1, y1 - l), (255, 0, 255), t)

        return img



def main():
    current_Time = 0
    previous_Time = 0
    detector = HandDetector()
    capture = cv.VideoCapture(0)

    while True:
        success, img = capture.read()
        img = cv.flip(img, 1)
        img = detector.findHands(img)
        hands = detector.findPositions(img, draw=True)

        for i, hand in enumerate(hands):
            lmlist = hand['landmarks']
            bbox = hand['bbox']
            fingers = detector.fingerCount(lmlist)
            print(f"Hand {i + 1}: Fingers = {fingers}")

            img, dist, pts = detector.findDistance(img, lmlist, 8, 12)
            # You can use `dist` and `pts` here

        current_Time = time.time()
        fps = 1 / (current_Time - previous_Time + 1e-5)
        previous_Time = current_Time
        cv.putText(img, str(int(fps)), (10, 70), cv.FONT_HERSHEY_COMPLEX, 3, (255, 255, 0), 2)
        cv.imshow("WebCam", img)
        
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    capture.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()
