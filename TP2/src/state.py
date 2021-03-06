import copy
from accents import charToIndice

class State:

    def __init__(self, parent):
        self.timesUsed = 0
        self.isEndPoint = 0
        self.isLastFive = 0
        self.words = []
        self.parent = parent
        self.childrenStates = []
        # 26 lettres plus les lettes accentées typiques, et apostrophe
        for i in range(38):
            self.childrenStates.append(None)

    def addTimesUsed(self):
        self.timesUsed += 1

    def addWord(self, word):
        self.words.append(word)
        if self.parent is not None:
            self.parent.addWord(word)

    def getState(self, char):
        index = ord(char) - 97
        if 155 > index > 26 or index == -58 or index == 242:
            index = charToIndice(char)
        if self.childrenStates[index] is not None:
            return self.childrenStates[index]
        raise ValueError

    def setChild(self, index, state):
        self.childrenStates[index] = state

    def fill(self, char):
        index = ord(char) - 97
        if 155 > index > 26 or index == -58 or index == 242:
            index = charToIndice(char)
        if self.childrenStates[index] is None:
            self.setChild(index, State(self))

    def makeTerminal(self):
        self.isEndPoint = 1

    def isTerminal(self):
        return self.isEndPoint

    def makeLastFive(self):
        self.isLastFive += 1

    def removeLastFive(self):
        self.isLastFive -= 1

    def ifLastFive(self):
        if self.isLastFive >=1:
            return True
        elif self.isLastFive == 0:
            return False
        else:
            print("erreur dans le isLastFive")

    def getTimeused(self):
        return self.timesUsed

    def getWords(self):
        return self.words

