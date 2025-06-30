import cv2 as cv
import mediapipe as mp
import time


class FaceDetector():
    def __init__(self, minDetectCon = 0.5):
        self.minDetectCon = minDetectCon
        self.mpFaceDetection = mp.solutions.face_detection
        self.mpDraw = mp.solutions.drawing_utils
        self.FaceDetection = self.mpFaceDetection.FaceDetection(self.minDetectCon)

# Reading Image

    def find_face(self,img, draw = True):

        imgRGB = cv.cvtColor(img,cv.COLOR_BGR2RGB)
        self.result = self.FaceDetection.process(imgRGB)
        # print(self.result)

        # bboxs will contain all the information about each face
        bboxs = []
        # After each iteration, we gonna append the face information to this list

        if (self.result.detections):             # The whole code below it is
                                                 # only for detecting one face

            for id,detections in enumerate(self.result.detections):
                # Built in function to draw boundaries
                # self.mpDraw.draw_detection(img,detections)

                # Storing all the coordinate values
                bounding_box_C = detections.location_data.relative_bounding_box

                img_h, img_w, img_d = img.shape

                # Storing exact pixel values by multiplying with image height width in bbc
                bbc = int(bounding_box_C.xmin * img_w),int(bounding_box_C.ymin * img_h), \
                      int(bounding_box_C.width * img_w),int(bounding_box_C.height * img_h)


                bboxs.append([id,bbc,detections.score])

                # Draws by default

                if (draw):
                    img = self.fancyDraw(img,bbc)
                    cv.putText(img, f"{str(int(detections.score[0] * 100))} %",
                               (bbc[0], bbc[1] - 20), cv.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 2)

        return img, bboxs

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
    capture = cv.VideoCapture("video.mp4.mp4")
    previous_time = 0

    detector = FaceDetector()

    while True:
        success, img = capture.read()

        img, bbox = detector.find_face(img)

        current_time = time.time()
        fps = 1 / (current_time - previous_time)
        previous_time = current_time
        cv.putText(img, str(int(fps)), (10, 70), cv.FONT_HERSHEY_COMPLEX, 3, (255, 255, 0), 2)

        cv.imshow("Video", img)
        cv.waitKey(10)


if __name__ == "__main__":
    main()