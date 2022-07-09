import time
import pyautogui as pyg
from PIL import Image
import requests
from io import BytesIO
import math

url = "https://pbs.twimg.com/media/E4LtA9ZXwAsgl1V?format=jpg&name=small"

colorsNames = [['black', 'darkgrey', 'darkblue'],
               ['white', 'grey', 'blue'],
               ['darkgreen', 'maroon', 'darkbrown'],
               ['green', 'red', 'orange'],
               ['brown', 'darkpink', 'darkpeach'],
               ['yellow', 'pink', 'peach']]

colorsRGB = {
    'black': (0, 0, 0),
    'darkblue': (0, 0, 139),
    'white': (255, 255, 255),
    'grey': (128, 128, 128),
    'blue': (0, 0, 255),
    'darkgreen': (0, 100, 0),
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
        color_diff = math.sqrt(abs(r - cr) ** 2 + abs(g - cg) ** 2 + abs(b - cb) ** 2)
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

pyg.PAUSE = 0  # 75 clicks / sec
imgW = int(min(canvasWidth, canvasHeight / imgAsr))
imgW = min(imgW, 65)
imgH = int(imgW * imgAsr)

img = img.resize((imgW, imgH), Image.ANTIALIAS)
pix = img.load()


def focus():
    pyg.click(canvasTopX, canvasTopY)


i = 0


def prepare(img):
    clicks_for_color = {}
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            color = closest_color(pix[x, y][:3])
            color_pos = colorToPos[color]
            cx = canvasTopX + x * dot_diameter
            cy = canvasTopY + y * dot_diameter
            if color_pos not in clicks_for_color:
                clicks_for_color[color_pos] = []
            clicks_for_color[color_pos].append((cx, cy))
    return clicks_for_color


time.sleep(5)
focus()

st = time.time()

clicks_for_color = prepare(img)


def draw_line(x, y1, y2):
    if y1 == y2:
        pyg.click(x, y1)
    else:
        pyg.moveTo(x, y1)
        pyg.dragTo(x, y2, button="left")


for color, clicks in clicks_for_color.items():
    cols = {}
    for (x, y) in clicks:
        if x not in cols:
            cols[x] = []
        cols[x].append(y)

    pyg.click(color)
    for x, ys in cols.items():
        ys = sorted(ys)
        n = len(ys)
        line_start = ys[0]
        line_end = ys[0]
        for y in ys[1:]:
            if y == line_end + dot_diameter:
                line_end = y
            else:
                draw_line(x, line_start, line_end)
                line_start = y
                line_end = y

        draw_line(x, line_start, line_end)

ed = time.time()

print(ed - st)

# print(canvasWidth, canvasHeight)


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
