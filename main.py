import time
import pyautogui as pyg
from PIL import Image
import requests
from io import BytesIO
import math
import sys

sys.setrecursionlimit(10000)

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


def sort_clock_wise(points):
    return sorted(points, key=clockwiseangle_and_distance)

def clockwiseangle_and_distance(point):
    origin = [2, 3]
    refvec = [0, 1]
    # Vector between point and the origin: v = p - o
    vector = [point[0]-origin[0], point[1]-origin[1]]
    # Length of vector: ||v||
    lenvector = math.hypot(vector[0], vector[1])
    # If length is zero there is no angle
    if lenvector == 0:
        return -math.pi, 0
    # Normalize vector: v/||v||
    normalized = [vector[0]/lenvector, vector[1]/lenvector]
    dotprod  = normalized[0]*refvec[0] + normalized[1]*refvec[1]     # x1*x2 + y1*y2
    diffprod = refvec[1]*normalized[0] - refvec[0]*normalized[1]     # x1*y2 - y1*x2
    angle = math.atan2(diffprod, dotprod)
    # Negative angles represent counter-clockwise angles so we need to subtract them
    # from 2*pi (360 degrees)
    if angle < 0:
        return 2*math.pi+angle, lenvector
    # I return first the angle because that's the primary sorting criterium
    # but if two vectors have the same angle then the shorter distance should come first.
    return angle, lenvector




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
imgW = min(imgW, 100)
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



def get_connected_components(positions):
    n = len(positions)
    adj = [[]] * n
    for i in range(n):
        for j in range(i+1,n):
            x1,y1 = positions[i]
            x2,y2 = positions[j]
            if abs(x1 - x2) == dot_diameter or abs(y1 -y2) == dot_diameter:
                adj[i].append(j)

    c_no = 0

    component_no = [0] * n

    def dfs(a):
        component_no[a] = c_no
        for b in adj[a]:
            if component_no[b] == 0:
                dfs(b)



    for i in range(n):
        if component_no[i] == 0:
            c_no += 1
            dfs(i)

    components = [[]] * (c_no)

    for i in range(n):
        components[component_no[i] - 1].append(positions[i])

    return components


def draw_line(x, y1, y2):
    if y1 == y2:
        pyg.click(x, y1)
    else:
        pyg.moveTo(x, y1)
        pyg.dragTo(x, y2, button="left")


for color, clicks in clicks_for_color.items():
    # comps = get_connected_components(clicks)
    pyg.click(color)
    # for pos in clicks:
    #     pyg.click(pos)
    cols = {}
    for (x, y) in clicks:
        if x not in cols:
            cols[x] = []
        cols[x].append(y)

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
