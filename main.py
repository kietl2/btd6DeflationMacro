import pyautogui as pya
import time
import win32gui
import json
from pynput.keyboard import Key, Controller
from pynput.mouse import Listener

import setups

keyboard = Controller()


# ---- timings ----
def loadTimings():
    global timingsDict
    with open("settings.json", "r") as settingsf:
        settings = json.load(settingsf)
        timings = settings.get("timings")
        timingsDict = timings






def settingsGet(dic):
    with open("settings.json", "r") as f:
        settingsDict = json.load(f)
        return settingsDict.get(dic)
    
def settingsSet(dic, dataDict, fullDict):
    with open("settings.json", "r+") as settingsFile:
        settingsDict = json.load(settingsFile)
        if fullDict:
            settingsDict.update(dataDict)
        else:
            specDict = settingsDict.get(dic, {})
            specDict.update(dataDict)
            settingsDict[dic] = specDict
        settingsFile.seek(0)
        json.dump(settingsDict, settingsFile, indent=4)
        settingsFile.truncate()

def main():
    global posDict, binds

    with open(f"settings.json", "r") as f:
        settingsDict = json.load(f)

    try:
        posDict = settingsDict.get("pos")
    except:
        raise Exception("position json not found - try calibrating in settings")
    try:
        binds = settingsDict.get("binds")
    except:
        raise Exception("binds json not found - try calibrating in settings")

    keyboardDelay = timingsDict.get("keyboardDelay")
    mouseDelay = timingsDict.get("mouseDelay")
    navSpeed = timingsDict.get("navSpeed")
    
    

    hwnd = win32gui.FindWindow(None, "BloonsTD6")

    x0, y0, x1, y1 = win32gui.GetWindowRect(hwnd)

            

    def clicketyClack(name):
        dellywelly = mouseDelay/2
        pos = posDict.get(name)
        cx, cy = pos

        tx = cx + x0
        ty = cy + y0
        time.sleep(dellywelly)
        pya.moveTo(tx, ty)
        time.sleep(dellywelly)
        pya.click()

    def clickClack(key):
        dellywelly = keyboardDelay/2
        time.sleep(dellywelly)
        keyboard.press(key)
        time.sleep(dellywelly)
        keyboard.release(key)

    def checkPixel(pos, col):
        cx, cy = pos
        tx = cx + x0
        ty = cy + y0
        if pya.pixel(tx, ty) != col:
            return False
        return True





    # get the levelup point's colour
    cx, cy = posDict.get("levelup")
    tx = cx + x0
    ty = cy + y0
    levelupcol = pya.pixel(tx, ty)

    setupper.placeSetup()

    # start game
    clickClack(Key.space)
    time.sleep(timingsDict.get("navSpeed"))
    clickClack(Key.space)

    while True:
        # if level up click off (check not just the win screen)
        if not checkPixel(posDict.get("levelup"), levelupcol):
            time.sleep(1)
            if not (checkPixel(posDict.get("winCheck"), (255, 255, 255)) or checkPixel(posDict.get("loseCheck"), (255, 255, 255))):
                clicketyClack("levelup")
                time.sleep(0.5)
                clicketyClack("levelup")

        # if win
        if checkPixel(posDict.get("winCheck"), (255, 255, 255)):
        
            # win
            clicketyClack("winCheck") # next
            time.sleep(navSpeed)
            clicketyClack("freeplay") # freeplay

            clickClack(Key.esc) # remove freeplay dialogue
            time.sleep(navSpeed)
            clickClack(Key.esc) # pause
            time.sleep(navSpeed)
            clicketyClack("restart") # restart
            time.sleep(navSpeed)
            clicketyClack("restartConfirmation")
            time.sleep(navSpeed)
            break

        # if lose
        if checkPixel(posDict.get("loseCheck"), (255, 255, 255)):
            clicketyClack("loseCheck")
            time.sleep(navSpeed)
            clicketyClack("restartConfirmation")
            time.sleep(navSpeed)
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
    
    def timingsChange():
        timingsList = timingsDict.keys()
        print("Which setting would you like to change?")
        for i, setting in enumerate(timingsList):
            print(i+1, " ", setting, ": ", timingsDict.get(setting))
        choice = int(input())
        settingToChange = list(timingsList)[choice-1]
        newData = {settingToChange: float(input("Enter new float in seconds: "))}
        settingsSet("timings", newData, False)


if __name__ == "__main__":
    try:
        with open("settings.json", "x") as s, open("defaults.json", "r") as d:
            s.write(d.read())
    except:
        pass
    setupper = setups.Setupper()
    Terminal = terminal()
    loadTimings()

    def runMacro():
        setupper.prepareSetup()
        print("you have 5 seconds to enter btd6")
        time.sleep(5)
        while True:
            main()
     
    def settings():
        def sure(): pass
        def unsure(): exit()
        def resetBinds():
            terminal.choice(sure, unsure)
            with open("defaults.json", "r") as defaultb, open("settings.json", "r+") as b:
                defaults = json.load(defaultb)
                setdata = json.load(b)
                setdata.setdefault("binds", {})
                setdata["binds"].update(defaults.get("binds", {}))
                b.seek(0)
                json.dump(setdata, b, indent=4)
                b.truncate()
        def resetPos():
            terminal.choice(sure, unsure)
            with open("defaults.json", "r") as defaultp, open("settings.json", "r+") as p:
                defaults = json.load(defaultp)
                setdata = json.load(p)
                setdata.setdefault("pos", {})
                setdata["pos"].update(defaults.get("pos", {}))
                p.seek(0)
                json.dump(setdata, p, indent=4)
                p.truncate()
        
        def adjustDelays():
            print("If your computer is especially slow, you may need to slow down some of these (especially navSpeed)\nin order to not have the script fail and accidentally start playing freeplay")
            terminal.timingsChange()

        def addSetup():
            setupper.appendSetup()
            


        def calibratePositions():
            with open("defaults.json", "r") as defaults:
                fulldata = json.load(defaults)
                posDict = fulldata.get("pos")
                poscount = len(list(posDict.keys()))
                counter = 0
                poslist = posDict.keys()
                
            with open("dialogue.json", "r") as dialogueFile:
                dialogueDict = json.load(dialogueFile)
                print("\n".join(x for x in dialogueDict.get("info"))) 
                steps = dialogueDict.get("steps")
                print(steps[0])
                
            poses = []
            def whenClick(*args):
                nonlocal counter
                if args[3] == False: # mouse up events only
                    poses.append([args[0], args[1]])
                    counter += 1
                    
                    if counter >= poscount:
                        return False
                    
                    print(steps[counter])
                    
                
            with Listener(on_click=whenClick) as listener:
                listener.join()
            if len(poslist) != len(poses):
                raise Exception("mismatch in positions collected")
            newposes = {name: coords for name, coords in zip(poslist, poses)}
                
            settingsSet("pos", newposes, False)
            print("Calibration complete!")
            print("run the script again to use the macro")


        terminal.choice(resetBinds, resetPos, calibratePositions, adjustDelays, addSetup)
    print("Welcome to my macro! it is recommended that you go into binds.json to adjust your keybinds \nso that the script does not press the wrong buttons")
    terminal.choice(runMacro, settings)

    

    
