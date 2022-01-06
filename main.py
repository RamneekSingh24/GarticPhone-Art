# TODO : improve speed
# too slow, 100*100 pixels in 280 secs

import time
import pyautogui as pyg
from pprint import pprint
from PIL import Image
import requests
from io import BytesIO
import math

url = "https://scontent.fjai2-3.fna.fbcdn.net/v/t1.6435-1/p480x480/131321493_345922260232932_7824312325167757271_n.jpg?_nc_cat=1&ccb=1-5&_nc_sid=c6021c&_nc_ohc=kwHU0KfTlYIAX-hzL-7&_nc_ht=scontent.fjai2-3.fna&oh=00_AT9nPIszcrlm80o6WC7tVKEPU3oTaJ9TaGKb49wzLD9Jjw&oe=61FBEB44"
#url = "https://cdn.vox-cdn.com/thumbor/Pkmq1nm3skO0-j693JTMd7RL0Zk=/0x0:2012x1341/1200x800/filters:focal(0x0:2012x1341)/cdn.vox-cdn.com/uploads/chorus_image/image/47070706/google2.0.0.jpg"



colorsNames = [['black', 'darkgrey', 'darkblue'],
          ['white', 'grey', 'blue'],
          ['darkgreen', 'maroon', 'darkbrown'],
          ['green', 'red', 'orange'],
          ['brown', 'darkpink', 'darkpeach'],
          ['yellow', 'pink', 'peach']]

colorsRGB = {
    'black' : (0, 0, 0),
    'darkblue' : (0, 0, 139),
    'white' : (255, 255, 255),
    'grey' : (128, 128, 128),
    'blue' : (0, 0, 255),
    'darkgreen' : (0, 100, 0),
    'maroon': (128, 0, 0),
    'darkbrown': (101, 67, 33),
    'green': (0, 128, 0),
    'red': (255, 0, 0),
    'orange': (255, 165, 0),
    'brown': (165, 42, 42),
    'darkpink': (231, 84, 128),
    'darkpeach': (222, 126, 93),
    'yellow': (255, 255, 0),
    'pink': (255, 192, 203),
    'peach': (255, 229, 180),
}
def closest_color(rgb):
    r, g, b = rgb
    color_diffs = []
    for name, color in colorsRGB.items():
        cr, cg, cb = color
        color_diff = math.sqrt(abs(r - cr)**2 + abs(g - cg)**2 + abs(b - cb)**2)
        color_diffs.append((color_diff, name))
    return min(color_diffs)[1]


response = requests.get(url)
img = Image.open(BytesIO(response.content))
imgH, imgW = img.size
imgAsr = imgH / imgW


dxColors = 35
dyColors = 38

baseColorsX = 357
baseColorsY = 342

colorToPos = {}


for r in range(6):
    for c in range(3):
        colorToPos[colorsNames[r][c]] = (baseColorsX + dxColors * c, baseColorsY + dyColors * r)

canvasTopX = 473
canvasTopY = 279
canvasBotX = 1152
canvasBotY = 653
dot_diameter = 5


canvasWidth = (canvasBotX - canvasTopX) / dot_diameter
canvasHeight = (canvasBotY - canvasTopY) / dot_diameter


"""
w, asr*h
w <= c
asr * w <= ch
w <= min(cw, ch/asr)
"""

pyg.PAUSE = 0
imgW = int(min(canvasWidth, canvasHeight / imgAsr))
imgW = min(imgW, 50)
imgH = int(imgW * imgAsr)




img = img.resize((imgW, imgH), Image.ANTIALIAS)
pix = img.load()


def focus():
    pyg.click(canvasTopX, canvasTopY)


i = 0



def draw(x, y):
    global i
    i += 1
    color = closest_color(pix[x, y])
    color_pos = colorToPos[color]
    pyg.click(color_pos)
    cx = canvasTopX + x * dot_diameter
    cy = canvasTopY + y * dot_diameter
    pyg.click(cx, cy)





time.sleep(5)
focus()

st = time.time()

for x in range(img.size[0]):
    for y in range(img.size[1]):
        draw(x, y)


ed = time.time()

print(ed - st)

















#print(canvasWidth, canvasHeight)


""" Color pos test [Works]"""
# for pos in colorToPos.values():
#     print(pos)
#     time.sleep(1)
#
#     pyg.moveTo(pos[0], pos[1])
#     clickNotOnTop()
#
#     time.sleep(0.1)
#     clickNotOnTop()
#
#     cx, cy = pyg.position()






