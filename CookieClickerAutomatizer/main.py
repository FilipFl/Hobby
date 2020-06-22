import cv2
import numpy as np
from PIL import ImageGrab
from pynput.mouse import Button, Controller
import pytesseract
import time

pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract.exe'

class CookieClickerAutomatizer:
    template = cv2.imread("image.png")
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    template_w, template_h = template.shape[0], template.shape[1]
    kernel = np.ones((5, 5), np.uint8)

    def __init__(self):
        self.mouse = Controller()
        self.cookiecounter = 0
        self.fortunecounter = 0
        self.spellcounter = 0
        self.lastx = 0
        self.lasty = 0
        self.lastspelltime = time.perf_counter()
        self.lastfortunetime = time.perf_counter()
        self.lastcookietime = time.perf_counter()

    def get_text(self, frame):
        return pytesseract.image_to_string(frame, config="--psm 1")

    def process(self):
        frame = ImageGrab.grab(bbox=(0, 0, 1650, 1080), )
        frame = np.array(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        grayframe = frame.copy()
        grayframe = cv2.cvtColor(grayframe, cv2.COLOR_BGR2GRAY)
        self.seekgoldencookie(grayframe)
        self.checkforfortune(frame)
        self.castaspell(frame)

    def seekgoldencookie(self, frame):
        if self.lastcookietime < time.perf_counter()-1:
            res = cv2.matchTemplate(frame, self.template, cv2.TM_CCOEFF)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            flag = False
            if max_val > 19000000:
                flag = True
            if flag:
                x = max_loc[0] + self.template_w / 2
                y = max_loc[1] + self.template_h / 2
                self.mouse.position = (x, y)
                self.mouse.click(Button.left, 1)
                self.mouse.position = (924, 400)
                self.cookiecounter += 1
                self.lastcookietime = time.perf_counter()
                print("I clicked {}. cookie!".format(self.cookiecounter))


    def checkforfortune(self, frame):
        if self.lastfortunetime < time.perf_counter()-1:
            cropped = frame[140:200, 650:1150]
            hsv = cv2.cvtColor(cropped, cv2.COLOR_BGR2HSV)
            yellow_lower = np.array([20, 100, 100])
            yellow_upper = np.array([30, 255, 255])
            mask_yellow = cv2.inRange(hsv, yellow_lower, yellow_upper)
            if mask_yellow.any() != 0:
                self.mouse.position = (850, 150)
                self.mouse.click(Button.left, 1)
                self.mouse.position = (924, 400)
                self.lastfortunetime = time.perf_counter()
                self.fortunecounter += 1
                print("I clicked {}. fortune!".format(self.fortunecounter))


    def castaspell(self, frame):
        if self.lastspelltime < time.perf_counter()-1:
            cropped = frame[340:370, 900:950]
            cropped = cv2.resize(cropped, (500, 300), 0, 0)
            cropped = cv2.dilate(cropped, self.kernel, iterations=4)
            cropped = cv2.erode(cropped, self.kernel, iterations=3)
            mask1 = cv2.inRange(cropped, (220, 220, 220), (255, 255, 255))
            cropped = cv2.bitwise_and(cropped, cropped, mask=mask1)
            cropped = cv2.bitwise_not(cropped)
            str = self.get_text(cropped)
            mana = str.split("/")
            if mana[0].isdigit() and mana[1].isdigit():
                if mana[0] == mana[1]:
                    self.mouse.position = (924, 284)
                    self.mouse.click(Button.left,1)
                    self.mouse.position = (924, 400)
                    self.lastspelltime = time.perf_counter()
                    self.spellcounter += 1
                    print("I casted {}. spell!".format(self.spellcounter))



if __name__ == '__main__':
    automatizer = CookieClickerAutomatizer()
    while True:
        automatizer.process()



