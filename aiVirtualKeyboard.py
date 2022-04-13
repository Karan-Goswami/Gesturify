# This file contains only one module of project that is virtual keyboard section.

# This module of the project basically provides the functionality of using keyboard to type in something like notepad based on detection of hand tracking and detection.

# We used OpenCV library for this project.

# importing packages and libraries
import cv2
from handTrackingModule import handDetector
from time import sleep
from pynput.keyboard import Controller

# using webcam as it's id is 0 to create video capturing device


# resizing video capturing dimensions
# creating handdetector object

cap = cv2.VideoCapture(0)

# resizing video capturing dimensions
cap.set(3, 1280)  # width
cap.set(4, 720)  # height

# providing higher confidence value as by mistake key does not get pressed
detector = handDetector(detection_con=0.8)

# alphabets list
keys = [['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
        ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';'],
        ['Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/']]

finalText = ''

keyboard = Controller()

def drawALL(img, buttonList):

    for button in buttonList:
        x, y = button.pos
        w, h = button.size

        # Creating rectangular boxes that contains font
        cv2.rectangle(img, button.pos, (x+w, y+h), (255, 0, 255), cv2.FILLED)

        # putting text on the image
        cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN,
                    4, (255, 255, 255), 4)

    return img


class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text


# Creating button list
buttonList = []
# creating mulitple rows
for i in range(len(keys)):
    # Creating buttons object with loop
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100*j+50, 100*i+50], key))

class aiKeyboard():
# while True:
    # def __init__(self, img):
    #     self.img = img

    def func(self):
    # finding hands from the image/webcam

        while True:
            success, img = cap.read()
            img = detector.findHands(img)

            lmList, bbox = detector.findPosition(img, False)

            img = drawALL(img, buttonList)

            # checking for hand
            if lmList:
                for button in buttonList:
                    x, y = button.pos
                    w, h = button.size

                    # to check our finger is in between or not using landmarks
                    # hand_number[hand_landmark][x(1) or y(2)]
                    if x < lmList[8][1] < x+w and y < lmList[8][2] < y+h:
                        # Creating rectangular boxes that contains font and making dark purple
                        cv2.rectangle(img, (x-5, y-5), (x+w+5, y+h+5),
                                    (175, 0, 175), cv2.FILLED)

                        # putting text on the image
                        cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN,
                                    4, (255, 255, 255), 4)

                        # getting distance between landmark 8 and 12
                        # for ignoring other parameters we used '_' with x and y positions as index 1 and 2
                        l, _, _ = detector.findDistance(
                            lmList[8][1:3], lmList[12][1:3], img)

                        # print(l)

                        # setting the range for the click based on the landmarks

                        if l < 60:
                            keyboard.press(button.text)
                            # Creating rectangular boxes that contains font and making green
                            cv2.rectangle(img, button.pos, (x+w, y+h),
                                        (0, 255, 0), cv2.FILLED)

                            # putting text on the image
                            cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN,
                                        4, (255, 255, 255), 4)
                            global finalText
                            finalText += button.text

                            # to count the number of clicking of button
                            sleep(0.15)

                # Creating rectangular boxes that contains font and making dark purple
                cv2.rectangle(img, (50, 350), (700, 450),
                            (175, 0, 175), cv2.FILLED)

                # putting text on the image
                cv2.putText(img, finalText, (60, 430), cv2.FONT_HERSHEY_PLAIN,
                            5, (255, 255, 255), 5)

                cv2.imshow('Image', img)
                # q button pressing to exit the prompt
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        cap.release()
        cv2.destroyAllWindows()





