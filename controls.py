from pynput.keyboard import Key, Controller as Keyboard, Listener
from pynput.mouse import Button, Controller as Mouse
from time import sleep

from mss import mss
import numpy as np
import cv2



class Control:

    def __init__(self):
        self.keyboard = Keyboard()
        self.mouse = Mouse()
        self.mss = mss()
        self.wait = True

        listener = Listener(on_release=self.on_release)
        listener.start()


    def on_release(self, key):
        if key == Key.alt_r:
            self.wait = not self.wait


    def sleep(self, *, pause=False):
        if pause:
            self.wait = True
        while self.wait:
            sleep(0.1)


    def send_key(self, key, d1 = 0.1, d2=0.1):
        match key:
            case Key():
                obj = self.keyboard
            case Button():
                obj = self.mouse

        obj.press(key)
        sleep(d1)
        obj.release(key)
        sleep(d2)


    def get_image(self, area):
        return np.asarray(self.mss.grab(area))



class Librarian(Control):

    def __init__(self):
        super().__init__()
        self.area = {"top": 439, "left": 878, "width": 272, "height": 92}


    def reroll(self):
        self.send_key(Key.esc)
        self.send_key(Button.left, d1=.4)
        self.send_key(Button.right, d2=2)
        self.send_key(Key.space)
        self.send_key(Button.right)


    def select_book(self, k):
        self.mouse.position = (860, 470+50*k)
        self.area['top'] = 439+50*k
        sleep(0.1)


    def get_book_image(self):
        img = self.get_image(self.area)
        img = cv2.resize(img, np.array(img.shape)[1::-1]//2, interpolation=cv2.INTER_NEAREST)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        match img[-1][-1]:
            case 18 | 19:
                return img
            case 198 | 255:
                return None
            case _:
                raise AssertionError
