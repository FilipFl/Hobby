import cv2
import numpy as np
from PIL import ImageGrab
from pynput.mouse import Button, Controller
import pytesseract
import time
import argparse

pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract.exe'

class CookieClickerAutomatizer:
    kernel = np.ones((5, 5), np.uint8)
    reindeertemplate = cv2.imread("newdeer.png")
    reindeertemplate = cv2.resize(reindeertemplate, (int(reindeertemplate.shape[1] / 2), int(reindeertemplate.shape[0] / 2)))
    reindeertemplate_w, reindeertemplate_h = reindeertemplate.shape[0], reindeertemplate.shape[1]

    def __init__(self, options):
        self.working = True
        self.mouse = Controller()
        self.cookiecounter = 0
        self.fortunecounter = 0
        self.spellcounter = 0
        self.reindeercounter = 0
        self.wrathcounter = 0
        self.lastspelltime = time.perf_counter()
        self.lastfortunetime = time.perf_counter()
        self.lastcookietime = time.perf_counter()
        self.lastwrathtime = time.perf_counter()
        self.options = options
        print(self.options)
        if self.options[-1] is True:
            self.screensize = (1920, 1080)
            self.manatop = (1000, 422)
            self.manabot = (1076, 435)
            self.toplimit = 300
            self.rightlimit = 1516
            self.wraththresh = True
            self.deerthresh = True
            self.goldthresh = True
            self.spellpoint = (1044, 356)
            self.mouserest = (1044, 700)
            self.template = cv2.imread("smallgold.png")
            self.wrathtemplate = cv2.imread("smallwrath.png")
        else:
            self.screensize = (1650,1080)
            self.manatop = (900, 340)
            self.manabot = (950, 370)
            self.toplimit = 300
            self.rightlimit = 1516
            self.wraththresh = True
            self.deerthresh = True
            self.goldthresh = True
            self.spellpoint = (924, 284)
            self.mouserest = (924, 700)
            self.template = cv2.imread("image.png")
            self.wrathtemplate = cv2.imread("badcookie.png")
        self.template = cv2.cvtColor(self.template, cv2.COLOR_BGR2GRAY)
        self.template_w, self.template_h = self.template.shape[0], self.template.shape[1]
        self.wrathtemplate_w, self.wrathtemplate_h = self.wrathtemplate.shape[0], self.wrathtemplate.shape[1]

    def is_working(self):
        return self.working

    def get_text(self, frame):
        return pytesseract.image_to_string(frame, config="--psm 1")

    def process(self):
        if self.mouse.position[1] < 100:
            self.working = False
            print("Exiting!")
        else:
            frame = ImageGrab.grab(bbox=(0, 0, self.screensize[0], self.screensize[1]), )
            frame = np.array(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            if self.options[0]:
                grayframe = frame.copy()
                grayframe = cv2.cvtColor(grayframe, cv2.COLOR_BGR2GRAY)
                self.seekgoldencookie(grayframe)
            if self.options[1]:
                self.castaspell(frame)
            if self.options[2]:
                self.checkforfortune(frame)
            if self.options[3]:
                self.seekreindeer(frame)
            if self.options[4]:
                self.seekwrath(frame)

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
                self.mouse.position = self.mouserest
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
                self.mouse.position = self.mouserest
                self.lastfortunetime = time.perf_counter()
                self.fortunecounter += 1
                print("I clicked {}. fortune!".format(self.fortunecounter))


    def castaspell(self, frame):
        if self.lastspelltime < time.perf_counter()-1:
            cropped = frame[self.manatop[1]:self.manabot[1], self.manatop[0]:self.manabot[0]]
            cropped = cv2.resize(cropped, (500, 300), 0, 0)
            cropped = cv2.dilate(cropped, self.kernel, iterations=4)
            cropped = cv2.erode(cropped, self.kernel, iterations=3)
            mask1 = cv2.inRange(cropped, (220, 220, 220), (255, 255, 255))
            cropped = cv2.bitwise_and(cropped, cropped, mask=mask1)
            cropped = cv2.bitwise_not(cropped)
            str = self.get_text(cropped)
            mana = str.split("/")
            try:
                if mana[0].isdigit() and mana[1].isdigit():
                    if mana[0] == mana[1]:
                        self.mouse.position = self.spellpoint
                        self.mouse.click(Button.left,1)
                        self.mouse.position = self.mouserest
                        self.lastspelltime = time.perf_counter()
                        self.spellcounter += 1
                        print("I casted {}. spell!".format(self.spellcounter))
            except IndexError:
                self.working = False

    def seekreindeer(self, frame):
        frame = cv2.resize(frame, (840, 525))
        res = cv2.matchTemplate(frame, self.reindeertemplate, cv2.TM_CCOEFF)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        flag = False
        if max_val > 19000000:
            flag = True
        if flag:
            x = 35 + (max_loc[0] + self.reindeertemplate_w / 2) * 2
            y = (max_loc[1] + self.reindeertemplate_h / 2) * 2
            if 250 < y < 360 and 650 < x < 1200 or 1360 < x:
                pass
            else:
                self.mouse.position = (x, y)
                self.mouse.click(Button.left, 1)
                self.mouse.position = self.mouserest
                self.reindeercounter += 1
                print("Clicked {}. reindeer!".format(self.reindeercounter))

    def seekwrath(self, frame):
        if self.lastwrathtime < time.perf_counter()-1:
            res = cv2.matchTemplate(frame, self.wrathtemplate, cv2.TM_CCOEFF)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            flag = False
            if max_val > 40000000:
                flag = True
            if flag:
                x = max_loc[0] + self.wrathtemplate_w / 2
                y = max_loc[1] + self.wrathtemplate_h / 2
                self.mouse.position = (x, y)
                self.mouse.click(Button.left, 1)
                self.mouse.position = self.mouserest
                self.lastwrathtime = time.perf_counter()
                self.wrathcounter += 1
                print("I clicked {}. wrath cookie!".format(self.wrathcounter))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--golden", help="Seek golden cookies", action="store_true")
    parser.add_argument("--spell", help="Cast a spell", action="store_true")
    parser.add_argument("--fortune", help="Search for fortune", action="store_true")
    parser.add_argument("--deer", help="Seek reindeers", action="store_true")
    parser.add_argument("--wrath", help="Seek wrath cookies", action="store_true")
    parser.add_argument("--single", help="Single screen setup", action="store_true")

    args = parser.parse_args()
    flags = [False for i in range(6)]
    if args.golden:
        flags[0] = True
    if args.spell:
        flags[1] = True
    if args.fortune:
        flags[2] = True
    if args.deer:
        flags[3] = True
    if args.wrath:
        flags[4] = True
    if args.single:
        flags[5] = True

    automatizer = CookieClickerAutomatizer(flags)

    while automatizer.is_working():
        automatizer.process()





