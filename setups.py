import pyautogui as pya
from pynput.keyboard import Key, Controller, Listener as kbListener
from pynput.mouse import Listener as mListener
import json
import time
import win32gui

keyboard = Controller()

class TerminalAlt:
    @staticmethod
    def pickAString(choices, question):
        print(question)
        for i, choice in enumerate(choices):
            print(f"{i+1}: {choice}")
        return list(choices)[int(input())-1]

    @staticmethod
    def enterData(question):
        return input(question + " ")


class Setupper:
    def __init__(self):
        with open("setups.json", "r") as setupsJson:
            self.setupsDict = json.load(setupsJson)

        hwnd = win32gui.FindWindow(None, "BloonsTD6")
        # x0, y0, x1, y1 = win32gui.GetWindowRect(hwnd)
        x0, y0 = (0, 0)
        self.winx = x0
        self.winy = y0

        with open("settings.json", "r") as settingsFile:
            settingsDict = json.load(settingsFile)
            delaysDict = settingsDict.get("timings")
            bindsDict = settingsDict.get("binds")
        self.mouseDelay = delaysDict.get("mouseDelay")
        self.keyboardDelay = delaysDict.get("keyboardDelay")

        self.upgradeBinds = [bindsDict.get(key) for key in bindsDict.keys()]

        self.recording = False
        self.stopRecording = True

    def mClick(self, coords):
        cx, cy = coords
        tx = int(cx) + self.winx
        ty = int(cy) + self.winy
        pya.moveTo(tx, ty)
        time.sleep(self.mouseDelay)
        pya.click()

    def kbPress(self, key):
        keyboard.press(key)
        time.sleep(self.keyboardDelay)
        keyboard.release(key)


    def chooseMap(self):
        question = "Which map would you like?"
        choices = self.setupsDict.keys()
        return TerminalAlt.pickAString(choices, question)
    
    def chooseSetup(self):
        question = "Which setup would you like to use"
        choices = self.chosenMapDict.keys()
        return self.chosenMapDict.get(TerminalAlt.pickAString(choices, question))

    def parseSetup(self, tower):
        # parse the setup
        # example "sm_935-426_023"
        arguments = tower.split("_")
        processedArguments = []

        for argument in arguments:
            if "-" in argument:
                processedArguments.append(argument.split("-"))
            else:
                processedArguments.append(argument)

        return processedArguments
    
    def placeSetup(self):
        # select map
        self.chosenMapDict = self.setupsDict.get(self.chooseMap())
        # select setup from map
        self.chosenSetup = self.chooseSetup()
        
        # parse setup text
        self.instructions = self.parseSetup(self.chosenSetup)
        
        print("you have 5 seconds to enter btd6")
        time.sleep(5)

        # place each tower
        for instruction in self.instructions:
            if instruction.__class__ == list:
                self.mClick(instruction)
            elif len(instruction) == 3:
                for path, count in enumerate(list(instruction)):
                    for i in range(int(count)):
                        self.kbPress(self.upgradeBinds[path])
            else:
                fancyKeys = {
                    "sell": Key.backspace
                }
                self.kbPress(fancyKeys.get(instruction, instruction))


    def whenClick(self, *args):
        if not self.stopRecording:
            return False
        if args[-2] == False:
            self.inputProcessor((args[0], args[1]))
            
    def whenPress(self, *args):
        if not self.stopRecording:
            return False
        self.inputProcessor(args[0])

    def inputProcessor(self, inp):
        if inp == Key.enter:
            if self.recording:
                self.stopRecording = False
                self.mouse_listener.stop()
                self.keyboard_listener.stop()
            self.recording = True
            pass
        if self.recording:
            if inp.__class__ == tuple:
                self.newSetup.append("-".join(str(inpp) for inpp in inp))
            else:
                inp = str(inp).strip("'")
                if inp in self.upgradeBinds:
                    if not self.upgrading:
                        self.upgrading = True
                    self.activeUpgrades[self.upgradeBinds.index(inp)] += 1
                else:
                    if self.upgrading:
                        self.upgrading = False
                        self.newSetup.append("".join(str(x) for x in self.activeUpgrades))
                        self.activeUpgrades = [0, 0, 0]
                    
                    if inp == str(Key.enter).strip("'"):
                        return
                    self.newSetup.append(inp)

    def appendSetup(self):
        newMap = TerminalAlt.pickAString(["new", "current"], "Would you like to enter a new map or use an existing one")
        if newMap == "current":
            mapName = self.chooseMap()
        else:
            mapName = TerminalAlt.enterData("Enter map name in lower case with dashes '-'")
            
        setupName = TerminalAlt.enterData("What should the setup be called? (should be in all caps with words separated by dashes '-')")
        
        self.newSetup = []
        self.upgrading = False
        self.activeUpgrades = [0, 0, 0]
        # input a setup here (big sad)
        self.mouse_listener = mListener(on_click=self.whenClick)
        self.keyboard_listener = kbListener(on_release=self.whenPress)
        print("It is now time to input the setup")
        print("you will begin and end recording by pressing enter")
        print("while recording only your key presses and mouse clicks are recorded")
        print("this means you must know the hotkeys to place your chosen towers and also the upgrade buttons")
        print("(defaults are ',' '.' and '/')")
        print("")
        print("you may now tab in and press enter to begin")
        # listeners start and will stop themselves when you press enter twice
        self.mouse_listener.start()
        self.keyboard_listener.start()
        self.mouse_listener.join()
        self.keyboard_listener.join()


        mapDict = {}
        mapDict.update({setupName: "_".join(self.newSetup)})
        self.setupsDict.update({mapName: mapDict})
        
        with open("setups.json", "w") as f:
            json.dump(self.setupsDict, f, indent=4)


if __name__ == "__main__":
    setupper = Setupper()
    setupper.placeSetup()



# TODO:
#   upgrades need to be changed from ._._/_/_/ to 023
