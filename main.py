import pyautogui as pya
import time
import win32gui
import json
from pynput.keyboard import Key, Controller
from pynput.mouse import Listener

keyboard = Controller()


# ---- settings ----
def loadSettings():
    global settingsDict
    with open("settings.json", "r") as settingsf:
        settings = json.loads(settingsf.read())
        settingsDict = settings








    

def main():
    global posDict, binds

    def loadJson(name):
        with open(f"{name}.json", "r") as f:
            return json.loads(f.read())

    try:
        posDict = loadJson("pos")
    except:
        raise Exception("position json not found - try calibrating in settings")
    try:
        binds = loadJson("binds")
    except:
        raise Exception("binds json not found - try calibrating in settings")
    
    

    hwnd = win32gui.FindWindow(None, "BloonsTD6")

    x0, y0, x1, y1 = win32gui.GetWindowRect(hwnd)

            

    def clicketyClack(name):
        pos = posDict.get(name)
        cx, cy = pos

        tx = cx + x0
        ty = cy + y0
        pya.moveTo(tx, ty)
        time.sleep(settingsDict.get("mouseDelay"))
        pya.click()

    def clickClack(key):
        keyboard.press(key)
        time.sleep(settingsDict.get("keyboardDelay"))
        keyboard.release(key)

    def checkPixel(pos, col):
        cx, cy = pos
        tx = cx + x0
        ty = cy + y0
        if pya.pixel(tx, ty) != col:
            time.sleep(1)
            return False
        return True





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
    time.sleep(0.5)
    clickClack(Key.space)

    while True:
        # if level up click off (check not just the win screen)
        if not checkPixel(posDict.get("levelup"), levelupcol):
            time.sleep(1)
            if not checkPixel(posDict.get("winCheck"), (255, 255, 255)):
                clicketyClack("levelup")
                time.sleep(0.5)
                clicketyClack("levelup")

        # if win
        if checkPixel(posDict.get("winCheck"), (255, 255, 255)):
        
            # win
            clicketyClack("winCheck") # next
            time.sleep(settingsDict.get("navSpeed"))
            clicketyClack("freeplay") # freeplay

            clickClack(Key.esc) # remove freeplay dialogue
            time.sleep(settingsDict.get("navSpeed"))
            clickClack(Key.esc) # pause
            time.sleep(settingsDict.get("navSpeed"))
            clicketyClack("restart") # restart
            time.sleep(settingsDict.get("navSpeed"))
            clicketyClack("restartConfirmation")
            time.sleep(settingsDict.get("navSpeed"))
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
    
    def settingsChange():
        settingsList = settingsDict.keys()
        print("Which setting would you like to change?")
        for i, setting in enumerate(settingsList):
            print(i+1, " ", setting, ": ", settingsDict.get(setting))
        choice = int(input())
        settingToChange = list(settingsList)[choice-1]
        with open("settings.json", "w") as f:
            settingsDict.update({settingToChange: float(input("Enter new float in seconds: "))})
            f.write(json.dumps(settingsDict))



if __name__ == "__main__":
    Terminal = terminal()
    loadSettings()

    def runMacro():
        # ensure window is focused
        print("you have 5 seconds to alt tab to btd6")
        time.sleep(5)
        while True:
            main()
    
    def settings():
        def sure(): pass
        def unsure(): exit()
        def resetBinds():
            terminal.choice(sure, unsure)
            with open("defaults.json", "r") as defaultb:
                with open("binds.json", "w") as b:
                    b.write(defaultb.read().get("binds"))
        def resetPos():
            terminal.choice(sure, unsure)
            with open("defaults.json", "r") as defaultp:
                with open("pos.json", "w") as p:
                    p.write(defaultp.read().get("pos"))
        
        def adjustDelays():
            print("If your computer is especially slow, you may need to slow down some of these (especially navSpeed)\nin order to not have the script fail and accidentally start playing freeplay")
            terminal.settingsChange()
            


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
The steps in order are:""")
                steps = """Churchill placement (click somewhere that churchill fits)
Super Monkey placement (click somewhere that supermonkey fits)
Super Monkey upgrade (click on the super monkey so that you can upgrade it to 0/2/3 - then play (speed up) and DO NOT CLICK ANYWHERE until you win)
Levelup (Click somewhere on the map that is not changing colour - this is used to see if the screen changes colour (you level up) and will then click off it automatically)
Win check (after winning click somewhere on the white part of the next button (this is used to check when you have won))
Freeplay (click the freeplay button)
Restart (press escape twice to first remove the freeplay dialogue and then pause it - Then click the restart button)
Restart confirmation (Click the restart confirmation button)"""
                        
                print(steps)
                
                print("Click location: ", list(poslist)[0])
                print(steps.split("\n")[0])
                poses = []
                def whenClick(*args):
                    nonlocal counter
                    if args[3] == False: # mouse up events only
                        print(*args)
                        poses.append([args[0], args[1]])
                        counter += 1
                        
                        if counter >= poscount:
                            return False
                        
                        print("Click location: ", list(poslist)[counter])
                        print(steps.split("\n")[counter])
                        
                    
                with Listener(on_click=whenClick) as listener:
                    listener.join()
                if len(poslist) != len(poses):
                    raise Exception("mismatch in positions collected")
                newposes = {name: coords for name, coords in zip(poslist, poses)}
                f.write(json.dumps(newposes))
                print("Calibration complete!")
                print("run the script again to use the macro")


        terminal.choice(resetBinds, resetPos, calibratePositions, adjustDelays)
    print("Welcome to my macro! it is recommended that you go into binds.json to adjust your keybinds \nso that the script does not press the wrong buttons")
    terminal.choice(runMacro, settings)

    

    
