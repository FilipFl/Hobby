import cv2
import numpy as np
from PIL import ImageGrab
from pynput.mouse import Button, Controller
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract.exe'

class CookieClickerAutomatizer:
    template = cv2.imread("image.png")
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    template_w, template_h = template.shape[0], template.shape[1]
    kernel = np.ones((5, 5), np.uint8)

    def __init__(self):
        self.mouse = Controller()
        self.counter = 0
        self.lastx = 0
        self.lasty = 0

    def get_text(self, frame):
        return pytesseract.image_to_string(frame, config="--psm 1")

    def process(self):
        frame = ImageGrab.grab(bbox=(0, 0, 1650, 1080), )
        frame = np.array(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        grayframe = frame.copy()
        grayframe = cv2.cvtColor(grayframe, cv2.COLOR_BGR2GRAY)
        self.seekgoldencookie(grayframe)
        self.checkforfortune(frame)
        self.castaspell(frame)

    def seekgoldencookie(self, frame):
        res = cv2.matchTemplate(frame, self.template, cv2.TM_CCOEFF)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        flag = False
        if max_val > 19000000:
            flag = True
        else:
            lastx = 0
            lasty = 0
        if flag:
            x = max_loc[0] + self.template_w / 2
            y = max_loc[1] + self.template_h / 2
            if self.lastx != x and self.lasty != y:
                self.mouse.position = (x, y)
                self.mouse.click(Button.left, 1)
                self.counter += 1
                print(self.counter)
                self.lastx = x
                self.lasty = y

    def checkforfortune(self, frame):
        cropped = frame[140:200, 650:1150]
        hsv = cv2.cvtColor(cropped, cv2.COLOR_BGR2HSV)
        yellow_lower = np.array([20, 100, 100])
        yellow_upper = np.array([30, 255, 255])
        mask_yellow = cv2.inRange(hsv, yellow_lower, yellow_upper)
        if mask_yellow.any() != 0:
            self.mouse.position = (850, 150)
            self.mouse.click(Button.left, 1)
            print("Fortune!")

    def castaspell(self, frame):
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


if __name__ == '__main__':
    automatizer = CookieClickerAutomatizer()
    while True:
        automatizer.process()



