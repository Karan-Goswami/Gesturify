import cv2
import mediapipe as mp
import time
import math

class handDetector():
    def __init__(self, mode=False, maxHands=2, modelComplexity=1, detection_con=0.5, track_con=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelComplex = modelComplexity
        self.detection_con = detection_con
        self.track_con = track_con

        # Got the hand detection utility
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplex, self.detection_con, self.track_con)

        # Got those 21 points of hands on screen
        self.mpDraw = mp.solutions.drawing_utils

        # Landmarks of tip of fingers
        self.tipIds = [4, 8, 12, 16, 20]

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # if(img is not None):
        #     imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        self.results = self.hands.process(imgRGB)  

        if self.results.multi_hand_landmarks:
            # handLms: for each hand
            #mphands.HAND_CONNECTIONS for drawing connection to those 21 points
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img
    
    def findPosition(self, img, handNumber=0, draw=True):
        xList = []
        yList = []
        bbox = []
        self.lndmarkList = []

        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNumber]

            for ids, lndmark in enumerate(myHand.landmark):
                    # But these values are in decimal (they're giving ratio of image) so we will multiply these values with the resolution and we'll get the pixel values
                    # height, width and channel of img
                    h, w, c = img.shape

                    # cx and cy are pixel values
                    cx, cy = int(lndmark.x*w), int(lndmark.y*h)

                    xList.append(cx)
                    yList.append(cy)
                    
                    self.lndmarkList.append([ids,cx,cy])
                    # if draw:
                    #     cv2.circle(img, (cx,cy), 15, (255,0,255), cv2.FILLED)

                    xMin, xMax = min(xList), max(xList)
                    yMin, yMax = min(yList), max(yList)
                    bbox = xMin, yMin, xMax, yMax

                    # if draw:
                    #         cv2.rectangle(img, (xMin - 20, yMin - 20), (xMax + 20, yMax + 20),
                    #           (0, 255, 0), 2)

        return self.lndmarkList, bbox

    def fingersUp(self):
        fingers = []

        # Thumb
        if self.lndmarkList[self.tipIds[0]][1] > self.lndmarkList[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Fingers
        for ids in range(1, 5):
            if self.lndmarkList[self.tipIds[ids]][2] < self.lndmarkList[self.tipIds[ids] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        
        return fingers

    
    def findDistance(self, p1, p2, img, draw=True, r=15, t=3):
        try:
            x1, y1 = self.lndmarkList[p1][1:]
            x2, y2 = self.lndmarkList[p2][1:]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        except:
            x1, y1 = p1
            x2, y2 = p2
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            # info = (x1, y1, x2, y2, cx, cy)
            
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)

        if img is not None:
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
            return length, img, [x1, y1, x2, y2, cx, cy]
        else:
            return length, [x1, y1, x2, y2, cx, cy]
 
        # return length, img, [x1, y1, x2, y2, cx, cy]

def main():
    prevTime = 0
    currTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()

    while True:
        success, img = cap.read()
        
        img = detector.findHands(img)
        lndmarkList, bbox = detector.findPosition(img)
        # if len(detector.findPosition(img)) != 0:
        #     print(lndmarkList[4])


        # Logic for FPS
        currTime = time.time()
        fps = 1/(currTime-prevTime)
        prevTime = currTime

        # Showing FPS on Screen
        cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0),3)

        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()