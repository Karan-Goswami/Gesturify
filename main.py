import cv2
import time
from handTrackingModule import handDetector
import aiVirtualMouse as avm
import aiVirtualKeyboard as avk
import aiVirtualVolumeController as avc

wCam, hCam = 1280, 720
prevTime = 0
currTime = 0

detector = handDetector(detection_con=0.8)

def main():

    ###############################
    # creating option menu
    keys = ['VIRTUAL KEYBOARD', 'VIRTUAL MOUSE', 'VOLUME CONTROLLER']
    ###############################

    # choice = int(input("Enter Your Choice: "))
    # if choice == 1:
    #     wCam, hCam = 640, 480
    # elif choice == 2:
    #     wCam, hCam = 1280, 720
    # else:
    #     wCam, hCam = 648,488
        
    global currTime, prevTime, wCam, hCam

    

    while True:
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        cap.set(3,wCam)
        cap.set(4,hCam)

        success, img = cap.read(0)
        img = detector.findHands(img)
        lmList, bbox = detector.findPosition(img, False)
        size = [0, 200, 400]
        # virtualMouse = avm.aiMouse(img)

        # creating shapes to make menu page

        cv2.rectangle(img, (50, 40), (1150, 130),
                    (175, 0, 175), cv2.FILLED)

        cv2.rectangle(img, (50, 240), (1150, 330),
                    (175, 0, 175), cv2.FILLED)

        cv2.rectangle(img, (50, 440), (1150, 530),
                    (175, 0, 175), cv2.FILLED)

        # providing text from menu
        for i in range(len(keys)):
            cv2.putText(img, keys[i], (60, 100+size[i]), cv2.FONT_HERSHEY_PLAIN,
                        5, (255, 255, 255), 5)

        # getting distance and performing choice operation
        if lmList:
            l, _, _ = detector.findDistance(lmList[8][1:3], lmList[12][1:3], img)

            if l < 60:
                # below code is for option 1 selection
                if (50 <= lmList[7][1] <= 1150) and (60 <= lmList[7][2] <= 150):
                    cv2.rectangle(img, (50, 40), (1150, 130),
                                (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, keys[0], (60, 100+size[0]), cv2.FONT_HERSHEY_PLAIN,
                                5, (255, 255, 255), 5)

                    string = 'AI Virtual Keyboard'

                    if string:
                        virtualKeyboard = avk.aiKeyboard()
                        virtualKeyboard.func()
                        print(string)

                # below code is for option 2 selection
                if (50 <= lmList[7][1] <= 1150) and (260 <= lmList[7][2] <= 350):
                    cv2.rectangle(img, (50, 240), (1150, 330),
                                (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, keys[1], (60, 100+size[1]), cv2.FONT_HERSHEY_PLAIN,
                                5, (255, 255, 255), 5)

                    string = 'AI Virtual Mouse'

                    if string:
                        virtualMouse = avm.aiMouse()
                        virtualMouse.func()
                        print(string)

                # below code is for option 3 selection
                if (50 <= lmList[7][1] <= 1150) and (460 <= lmList[7][2] <= 550):
                    cv2.rectangle(img, (50, 440), (1150, 530),
                                (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, keys[2], (60, 100+size[2]), cv2.FONT_HERSHEY_PLAIN,
                                5, (255, 255, 255), 5)

                    string = 'AI Volume Controller'

                    if string:
                        virtualVolumeCtrl = avc.aiVolumeCtrl()
                        virtualVolumeCtrl.func()
                        # print(string)
                time.sleep(0.25)
        # Logic for FPS
        currTime = time.time()
        fps = 1/(currTime-prevTime)
        prevTime = currTime

        # Showing FPS on Screen
        cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0),3)

        cv2.imshow("Main", img)
        if cv2.waitKey(1) & 0xFF == ord('k'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()