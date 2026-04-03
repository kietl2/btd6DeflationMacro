import pyautogui as pya
from pynput.keyboard import Key, Controller
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
        return self.setupsDict.get(TerminalAlt.pickAString(choices, question))
    
    def chooseSetup(self):
        question = "Which setup would you like to use"
        choices = self.chosenMapDict.keys()
        return self.chosenMapDict.get(TerminalAlt.pickAString(choices, question))

    def parseTower(self, tower):
        # parse each tower of the setup
        # example tower "sm_935-426_023"
        arguments = tower.split("_")
        if len(arguments) > 2:
            return {"placeBind": arguments[0],
                    "position": arguments[1].split("-"),
                    "upgrades": arguments[2]}
        else:
            return {"placeBind": arguments[0],
                    "position": arguments[1].split("-")}

    def upgradeTower(self, position, upgrades):
        self.mClick(position)
        for i, upgrade in enumerate(list(upgrades)):
                count = int(upgrade)
                for j in range(count):
                    self.kbPress(self.upgradeBinds[i])

    def sellTower(self, position):
        if self.upgradeBinds[3] == "backspace":
            sellBind = Key.backspace
        else:
            sellBind = self.upgradeBinds[3]
        
        self.mClick(position)
        self.kbPress(sellBind)


    def placeTower(self, towerDict):
        placeBind = towerDict.get("placeBind")
        position = towerDict.get("position")
        upgrades = towerDict.get("upgrades", None)
        if placeBind not in ("up", "sell"):
            self.kbPress(placeBind)
            self.mClick(position)
        if placeBind == "sell":
            self.sellTower(position)
        if upgrades:
            self.upgradeTower(position, upgrades)

    def saveSetups(self):
        with open("setups.json", "w") as setupsFile:
            json.dump(self.setupsDict, setupsFile)
    
    def placeSetup(self):
        # select map
        self.chosenMapDict = self.chooseMap()
        # select setup from map
        self.chosenSetup = self.chooseSetup()
        
        # parse tower text
        towerDicts = []
        for tower in self.chosenSetup:
            towerDict = self.parseTower(tower)
            towerDicts.append(towerDict)
        
        print("you have 5 seconds")
        time.sleep(5)
        # place each tower
        for towerDict in towerDicts:
            self.placeTower(towerDict)

    def appendSetup(self):
        newMap = TerminalAlt.pickAString(["new", "current"], "Would you like to enter a new map or use an existing one")
        if newMap == "current":
            self.chosenMapDict = self.chooseMap()
        else:
            newMapName = TerminalAlt.enterData("Enter map name in lower case with dashes '-'")
            self.chosenMapDict = {}

        setupName = TerminalAlt.enterData("What should the setup be called? (should be in all caps with words separated by dashes '-')")
        
        newSetup = []
        # input a setup here (big sad)
        print("It is now time to input the setup")
        print("Each 'step' is composed of 1 of 3 things:")
        print("1: placing a tower (and optionally upgrading it)")
        print("2: selling a tower")
        print("3: upgrading a tower")
        print("In order to tell the program which of these you are inputting, you must:")
        print("1: press a tower hotkey and click somewhere")
        print("2: click somewhere (on a tower) then press the sell bind")
        print("3: click somewhere then press the upgrade binds")
        print("After each step, press enter")
        print("When you are done, press enter twice in a row")

        self.chosenMapDict.update({setupName: newSetup})
        self.setupsDict.update(self.chosenMapDict)
        self.saveSetups()


if __name__ == "__main__":
    setupper = Setupper()
    setupper.appendSetup()



# TODO:
#   finish letting you input setups 
