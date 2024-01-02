import cv2
import time
import os
import cvzone.HandTrackingModule as htm

# Menyiapkan kamera
wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# Memanggil lokasi dan membaca citra jari
folderPath = "jari"
# myList = os.listdir(folderPath)
overlayList = []
imPath = ["0.png", "1.png", "2.png", "3.png", "4.png", "5.png"]

for i in imPath:
# for imPath in myList:
    image = cv2.imread(f"{folderPath}/{i}")
    overlayList.append(image)

pTime = 0
detector = htm.HandDetector(detectionCon=0.75)
# Menyimpan nilai titik setiap ujung jari
tipIds = [4, 8, 12, 16, 20]

while True:
    success, img = cap.read()
    img = detector.findHands(img, draw=True)
    # Menyimpan posisi titik (landmark) jari yang terbaca
    lmList = detector.findPosition(img, draw=False)
    # print(f"lmlist: {lmList}")
    # print(f"len lmlist:  {len(lmList)}")

    if len(lmList) != 0:
        fingers = [] # menyimpan nilai 0/1 (jari tertutup/terbuka)

        # Ibu jari terbuka jika posisi titik 4 > 3
        if lmList[0][tipIds[0]][1] > lmList[0][tipIds[0] - 1][1]:
        # if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Jari-jari lainnya terbuka jika posisi titik id < id-2
        for id in range(1, 5):
            if lmList[0][tipIds[id]][1] < lmList[0][tipIds[id] - 2][1]:
            # if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        totalFingers = fingers.count(1)

        # Menampilkan gambar tangan dan angka
        h, w, c = overlayList[totalFingers].shape
        img[0:h, 0:w] = overlayList[totalFingers]
        # h, w, c = overlayList[totalFingers - 1].shape
        # img[0:h, 0:w] = overlayList[totalFingers - 1]
        cv2.rectangle(img, (20, 225), (170, 425), (0,255, 0), cv2.FILLED)
        cv2.putText(img, str(totalFingers), (45, 375), cv2.FONT_HERSHEY_PLAIN,
                    10, (255, 0, 0), 25)

    # Menghitung dan menampilkan FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN,
                3, (255, 0, 0), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)