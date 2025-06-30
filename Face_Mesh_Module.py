import cv2 as cv
import mediapipe as mp
import time

class Facemesh():
    def __init__(self,stat_img_mode = False, max_num_face = 1, ref_lndmrk = False,
                 min_det_con = 0.5, min_trac_con = 0.5):

        self.stat_img_mode = stat_img_mode
        self.max_num_face = max_num_face
        self.ref_lndmark = ref_lndmrk
        self.min_det_con = min_det_con
        self.min_trac_con = min_trac_con

        self.mpDraw = mp.solutions.drawing_utils
        self.mpFaceMesh = mp.solutions.face_mesh
        self.facemesh = self.mpFaceMesh.FaceMesh(self.stat_img_mode,self.max_num_face,
                                                 self.ref_lndmark, self.min_det_con, self.min_trac_con)
        self.drawSpec = self.mpDraw.DrawingSpec(thickness=1, circle_radius=1, color=(255, 0, 0))


    def faceMesh(self, img, draw = True):

        self.imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.results = self.facemesh.process(self.imgRGB)

        faces = []

        if (self.results.multi_face_landmarks):

            for facelms in self.results.multi_face_landmarks:

                if draw:
                    self.mpDraw.draw_landmarks(img, facelms, self.mpFaceMesh.FACEMESH_TESSELATION,
                                                self.drawSpec, self.drawSpec)

                face = []
                for id, lm in enumerate(facelms.landmark):
                    # print(lm)
                    # To get the pixel values
                    ix, iy, ih = img.shape
                    x, y = int(lm.x * ix), int(lm.y * iy)
                    # cv.putText(img, str(id), (x,y), cv.FONT_HERSHEY_PLAIN,
                    #           1, (255, 0, 255), thickness=1)
                    face.append([x,y])
                faces.append(face)
        return img, faces



def main():
    cap = cv.VideoCapture("video1.mp4")
    prev_time = 0

    detector = Facemesh()
    while True:
        success, img = cap.read()
        img, faces = detector.faceMesh(img)

        if len(faces) != 0:
            print(len(faces))
        ctime = time.time()
        fps = 1 / (ctime - prev_time)
        prev_time = ctime
        cv.putText(img, str(f"{int(fps)}"), (20, 70), cv.FONT_HERSHEY_PLAIN,
                   3, (255, 0, 255), thickness=2)

        cv.imshow("vidos", img)

        cv.waitKey(10)

if __name__ == "__main__":
    main()