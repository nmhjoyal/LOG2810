import copy


class State:

    def __init__(self, parent):
        self.timesUsed = 0
        self.isEndPoint = 0
        self.isLastFive = 0
        self.words = []
        self.parent = parent
        self.childrenStates = [26]

    def addTimesUsed(self):
        self.timesUsed += 1

    def addWord(self, word):
        self.words.__add__(word)

    def addWords(self, words):
        self.words = copy.deepcopy(words)

    def getState(self, char):
        index = ord(char) - 97
        return self.childrenStates[index]

    def setChild(self, index, state):
        self.childrenStates[index] = state

    def setParent(self, parentState):
        self.parent = parentState

    def fill(self, char):
        index = ord(char) - 97
        if self.childrenStates[index] is None:
            self.setChild(index, State(self))

