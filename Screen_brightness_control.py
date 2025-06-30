import cv2 as cv
import numpy as np
import time
import Hand_Tracking_module as htm
import math
# from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
# from ctypes import cast, POINTER
# from comtypes import CLSCTX_ALL
import screen_brightness_control as sbc

wcam, hcam = 640, 480

cap = cv.VideoCapture(0)
cap.set(3, wcam)
cap.set(4, hcam)

detector = htm.HandDetector(detectionCon=0.7)

# devices = AudioUtilities.GetSpeakers()
# interface = devices.Activate(
#     IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
# volume = cast(interface, POINTER(IAudioEndpointVolume))

# print(f"Audio output: {device.FriendlyName}")
# print(f"- Muted: {bool(volume.GetMute())}")
# print(f"- Volume level: {volume.GetMasterVolumeLevel()} dB")

# print(f"- Volume range: {volume.GetVolumeRange()[0]} dB - {volume.GetVolumeRange()[1]} dB")
#
# minVol = volume.GetVolumeRange()[0]
# maxVol = volume.GetVolumeRange()[1]

vol = 0
volBar = 400
volper = 0
brightness = 0

ptime = 0
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmlist = detector.findposition(img, draw=False)

    if len(lmlist) != 0:
        # print(lmlist[2], lmlist[8])

        x1, y1 = lmlist[4][1], lmlist[4][2]
        x2, y2 = lmlist[8][1], lmlist[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        cv.circle(img, (x1, y1), 15, (255, 0, 8), -1)
        cv.circle(img, (x2, y2), 15, (255, 0, 8), -1)
        cv.line(img, (x1, y1), (x2, y2), (255, 0, 255), 2)

        cv.circle(img, (cx, cy), 15, (255, 0, 8), -1)

        length = math.hypot(x2 - x1, y2 - y1)
        # print(length)

        # Hand range : 50 - 300    (Average)
        # Volume range : -65 to 0   (Output from the function)

        brightness = np.interp(length, [50, 300], [0, 100])
        volBar = np.interp(length, [50, 300], [400, 150])
        volper = brightness

        sbc.set_brightness(int(brightness))

        if (length < 100):
            cv.circle(img, (cx, cy), 15, (0, 255, 0), -1)
        elif (length > 270):
            cv.circle(img, (cx, cy), 15, (0, 0, 255), -1)

    cv.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
    cv.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), -1)
    cv.putText(img, f'{int(volper)} %', (40, 450), cv.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)

    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime

    cv.putText(img, str(int(fps)), (40, 70), cv.FONT_HERSHEY_COMPLEX, 3, (255, 0, 0), 2)
    cv.imshow("Webcam 1 ", img)
    cv.waitKey(1)
