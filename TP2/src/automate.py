from state import State

class Automate:
    def __init__(self, lexicon):
        self.states = []
        self.currentId = 0;
        self.createAutomate(lexicon)

    def createAutomate(self, lexicon):
        self.states[0] = State(0, "")
        self.currentId += 1

        currentWord = 0

        for i in lexicon[currentWord]:
            self.states[self.currentId] = State(self.currentId, i)
