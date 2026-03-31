import pyautogui as pya
import time
import win32gui
import json
from pynput.keyboard import Key, Controller
from pynput.mouse import Listener

keyboard = Controller()


# ---- settings ----
keyboardDelay = 0.1
mouseDelay = 0





hwnd = win32gui.FindWindow(None, "BloonsTD6")

x0, y0, x1, y1 = win32gui.GetWindowRect(hwnd)

def loadJson(name):
    with open(f"{name}.json", "r") as f:
        return json.loads(f.read())
        

def clicketyClack(name):
    pos = posDict.get(name)
    cx, cy = pos

    tx = cx + x0
    ty = cy + y0
    pya.moveTo(tx, ty)
    time.sleep(mouseDelay)
    pya.click()

def clickClack(key):
    keyboard.press(key)
    time.sleep(keyboardDelay)
    keyboard.release(key)

def checkPixel(pos, col):
    cx, cy = pos
    tx = cx + x0
    ty = cy + y0
    while pya.pixel(tx, ty) != col:
        time.sleep(1)
        pass
    

def main():
    global posDict, binds
    posDict = loadJson("pos")
    binds = loadJson("binds")

    # ensure window is focused
    pya.getWindowsWithTitle("BloonsTD6")[0].activate() 
    time.sleep(0.1)


    # get the levelup point's colour
    cx, cy = posDict.get("levelup")
    tx = cx + x0
    ty = cy + y0
    levelupcol = pya.pixel(tx, ty)

    # place churchill
    clickClack(binds.get("hero"))
    clicketyClack("cPlacement")

    # place super monkey
    clickClack(binds.get("super"))
    clicketyClack("smPlacement")
    
    # upgrade 0/2/3
    clicketyClack("smPlacement")
    clickClack(binds.get("up1"))
    clickClack(binds.get("up1"))
    clickClack(binds.get("up2"))
    clickClack(binds.get("up2"))
    clickClack(binds.get("up2"))

    # start game
    clickClack(Key.space)
    clickClack(Key.space)

    while True:
        # if level up click off (check not just the win screen)
        if checkPixel(posDict.get("levelup"), levelupcol) and not checkPixel(posDict.get("winCheck"), (255, 255, 255)):
            clickClack(posDict.get("levelup"))
            time.sleep(0.5)
            clickClack(posDict.get("levelup"))

        # if win
        if checkPixel(posDict.get("winCheck"), (255, 255, 255)):
        
            # win
            clicketyClack("winCheck") # next
            time.sleep(1)
            clicketyClack("freeplay") # freeplay

            clickClack(Key.esc) # remove freeplay dialogue
            time.sleep(0.5)
            clickClack(Key.esc) # pause
            time.sleep(0.5)
            clicketyClack("restart") # restart
            time.sleep(0.5)
            clicketyClack("restartConfirmation")
            time.sleep(0.5)
            break
    




class terminal():
    def __init__(self):
        pass
    def choice(*funcs):
        print("Would you like to:")
        for i, func in enumerate(funcs):
            print(i + 1, func.__name__)

        choice = int(input(">"))
        funcs[choice-1]()



if __name__ == "__main__":
    Terminal = terminal()

    def runMacro():
        while True:
            main()
    
    def settings():
        def sure(): pass
        def unsure(): exit()
        def resetBinds():
            terminal.choice(sure, unsure)
            with open("defaultbinds.json", "r") as defaultb:
                with open("binds.json", "w") as b:
                    b.write(defaultb.read())
        def resetPos():
            terminal.choice(sure, unsure)
            with open("defaultpos.json", "r") as defaultp:
                with open("pos.json", "w") as p:
                    p.write(defaultp.read())

        def calibratePositions():
            
            with open("defaultpos.json", "r") as defp:
                data = json.loads(defp.read())
                poscount = len(list(data.keys()))
                print(poscount)
                counter = 0

                poslist = data.keys()
                
            
            with open("pos.json", "w") as f:
                print("""INFO:
For the duration of calibration ensure your game is on you primary monitor (you can move the window after)
To move the btd6 window you can press Windows + Shift + Left or right arrow keys
The steps in order are:
    Churchill placement (click somewhere that churchill fits)
    Super Monkey placement (click somewhere that supermonkey fits)
    Super Monkey upgrade (click on the super monkey so that you can upgrade it to 0/2/3)
    Now start the game (with space) and wait until it ends (NOT CLICKING AT ALL WHILE YOU WAIT)
    Win check (after winning click somewhere on the white part of the next button (this is used to check when you have won))
    Freeplay (click the freeplay button)
    Restart (press escape twice to first remove the freeplay dialogue and then pause it - Then click the restart button)
    Restart confirmation (Click the restart confirmation button)
    Levelup (Click somewhere on the map that is not changing colour - this is used to see if the screen changes colour (you level up) and will then click off it automatically)
                        """)
                
                print("Click location: ", list(poslist)[0])
                poses = []
                def whenClick(*args):
                    nonlocal counter
                    if args[-1] == False: # mouse up events only
                        if counter+1 >= poscount:
                            return False
                        print(*args)
                        poses.append([args[0], args[1]])
                        counter += 1
                        print("Click location: ", list(poslist)[counter])
                        
                    
                with Listener(on_click=whenClick) as listener:
                    listener.join()
                newposes = {name: coords for name, coords in zip(poslist, poses)}
                f.write(json.dumps(newposes))


        terminal.choice(resetBinds, resetPos, calibratePositions)

    terminal.choice(runMacro, settings)

    

    
