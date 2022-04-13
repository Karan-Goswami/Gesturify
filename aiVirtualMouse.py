import cv2
import numpy as np
import handTrackingModule as htm
import autopy
import time

prevTime = 0
currTime = 0

frameReduction = 100
wCam, hCam = 640, 480

# Smoothening because without it, mouse flickers a lot
smoothening = 7
prevLocX, prevLocY = 0, 0
currLocX, currLocY = 0, 0

cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)

detector = htm.handDetector(maxHands=1)

# Size of Screen
wScr, hScr = autopy.screen.size()
# 1536.0 864.0

class aiMouse():
    # def __init__(self, img):
    #     self.img = img

    def func(self):    
        global prevLocX, prevLocY, currLocX, currLocY, wCam, hCam, currTime, prevTime
        # Detecting Landmark
        # img = detector.findHands(self.img)
        # lmlist, bbox = detector.findPosition(img)

        
        while True:
            success, img = cap.read(1)
            img = detector.findHands(img)
            lmlist, bbox = detector.findPosition(img)


            # Getting tip of index and middle finger
            if len(lmlist)!=0:
                # Index finger
                x1, y1 = lmlist[8][1:]
                # middle finger
                x2, y2 = lmlist[12][1:]

                # Detecting which fingers are up
                fingers = detector.fingersUp()
                
                # Created a rectangle so as mouse pad
                cv2.rectangle(img, (frameReduction, frameReduction), (wCam - frameReduction, hCam - frameReduction), (255, 0, 255), 2)
                
                # Only Index finger is up and middle finger is down then it is in moving mode
                if fingers[1] == 1 and fingers[2] == 0:
                    
                    # Converting coordinates (converting one range to another range)
                    x3 = np.interp(x1, (frameReduction, wCam - frameReduction), (0, wScr))
                    y3 = np.interp(y1, (frameReduction, hCam - frameReduction), (0, hScr))

                    # Smootheing the mouse
                    currLocX = prevLocX + (x3 - prevLocX)/smoothening
                    currLocY = prevLocY + (y3 - prevLocY)/smoothening


                    # With these coordinates we use hand as mouse
                    # But when you move your hand to right, mouse goes to left. So, we need to flip the direction
                    autopy.mouse.move(wScr - currLocX, currLocY)

                    # Highlighting the index finger
                    cv2.circle(img, (x1, y1), 15, (0, 0, 255), cv2.FILLED)
                    
                    prevLocX, prevLocY = currLocX, currLocY
                
                # If both the index and middle fingers are up
                if fingers[1] == 1 and fingers[2] == 1:
                    # 8, 12 are landmark ids
                    # Checking distance between two fingers
                    length, img, lineInfo = detector.findDistance(8, 12, img)    
                    # print(length)

                    # Performing mouse click if distance is short
                    if length < 40:
                        cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)

                        autopy.mouse.click()
            currTime = time.time()
            fps = 1/(currTime-prevTime)
            prevTime = currTime
            cv2.putText(img, str(int(fps)), (20,50), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0),3)
            
            cv2.imshow("AI Mouse", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()    