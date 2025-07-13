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
