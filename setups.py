import pyautogui as pya
import json

class TerminalAlt:
    @staticmethod
    def pickAString(choices, question):
        print(question)
        for i, choice in enumerate(choices):
            print(f"{i+1}: {choice}")
        return list(choices)[int(input())-1]


class Setupper:
    def __init__(self):
        with open("setups.json", "r") as setupsJson:
            self.mapsDict = json.load(setupsJson)

    def chooseMap(self):
        question = "Which map would you like to use?"
        choices = self.mapsDict.keys()
        return self.mapsDict.get(TerminalAlt.pickAString(choices, question))
    
    def chooseSetup(self):
        question = "Which setup would you like to use"
        choices = self.chosenMapDict.keys()
        return self.chosenMapDict.get(TerminalAlt.pickAString(choices, question))

    def placeSetup(self):
        self.chosenMapDict = self.chooseMap()
        self.chosenSetup = self.chooseSetup()
        print(self.chosenSetup)




if __name__ == "__main__":
    setupper = Setupper()
    setupper.placeSetup()


"""
TODO:
    continue adding all default keybinds 
    continue adding parsing for each tower in placeSetup
"""