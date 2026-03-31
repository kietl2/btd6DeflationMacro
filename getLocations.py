import pyautogui as pya
import time
import win32gui


hwnd = win32gui.FindWindow(None, "BloonsTD6")

x0, y0, x1, y1 = win32gui.GetWindowRect(hwnd)

while True:
    time.sleep(1)
    print(pya.position())