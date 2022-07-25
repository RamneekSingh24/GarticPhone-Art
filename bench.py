import time

import pyautogui

if __name__ == "__main__":
    pyautogui.PAUSE = 0
    y = 300
    n = 100
    x1 = 500
    x2 = x1 + n
    st = time.time()
    for i in range(x1, x2+1):
        pyautogui.click(i, y)
    ed = time.time()
    t1 = ed - st
    print(t1)

    st = time.time()
    pyautogui.moveTo(x1, y)
    pyautogui.dragTo(x2, y, button="left")

    ed = time.time()
    t2 = ed - st
    print(ed - st)
    print(t1 / t2)

    """
    1.2689902782440186
    0.050199031829833984
    26x faster / 100 clicks
    """