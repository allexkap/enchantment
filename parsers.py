import numpy as np
import cv2



class DescriptionParser:

    def __init__(self):
        pass

    @staticmethod
    def show(img, delay):
        cv2.imshow('lib', img)
        cv2.waitKey(delay)

    @staticmethod
    def crop(img):
        offsets = []
        for k in range(4):
            for i, line in enumerate(img):
                if any(line):
                    offsets.append(i)
                    break
            else:
                offsets.append(0)
            img = np.rot90(img)
        for i in range(2):
            offsets[1+i] = img.shape[1-i] - offsets[1+i]
        return img[offsets[0]:offsets[2], offsets[3]:offsets[1]]


    def load_example(self, img):
        self.hash_example = {}
        for i in range(128):
            if 48 <= i <= 57 or 65 <= i <= 90 or 97 <= i <= 122:
                x, y = (i % 16) * 8, (i // 16) * 8
                letter = DescriptionParser.crop(img[y:y+8, x:x+8])
                self.hash_example[hash(letter.tobytes())] = chr(i)


    def get_enchantment(self, img):
        img = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)[1]
        img = DescriptionParser.crop(img)
    
        letters = [[]]
        for x in range(img.shape[1]):
            if bool(letters[-1]) ^ any(img[-8:, x]):
                letters[-1].append(x)
                if len(letters[-1]) == 2:
                    letters.append([])
        letters.pop()

        out = []
        for letter in letters:
            h = hash(DescriptionParser.crop(img[-8:, letter[0]:letter[1]]).tobytes())
            out.append(self.hash_example[h])
        return ''.join(out)