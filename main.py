import numpy as np
import cv2
import pickle
from time import monotonic

from controls import Librarian
from parsers import DescriptionParser


game = Librarian()
book = DescriptionParser()

book.load_example(cv2.imread('resources/ascii.png', 0))
with open('resources/enchantment.txt') as file:
    needed_enchantments = {''.join(line.split()) for line in file}
with open('resources/found.txt') as file:
    needed_enchantments -= {''.join(line.split()) for line in file}


game.sleep(pause=True)
for i in range(64):
    game.reroll()
    for k in range(2):
        game.select_book(k)
        book_image = game.get_book_image()
        if type(book_image) != np.ndarray:
            continue
            
        enchantment = book.get_enchantment(book_image)
        print(f'{i:2} {enchantment}')

        if enchantment in needed_enchantments:
            open('resources/found.txt', 'a').write(f'{enchantment}\n')
            needed_enchantments.remove(enchantment)
            game.sleep(pause=True)
            break
    else:
        game.sleep()
