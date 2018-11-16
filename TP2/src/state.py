class State:
    def __init__(self, id, letter, endPoint):
        self.id = id
        self.letter = letter
        self.endPoint = endPoint

        self.nextStates = []

    def addNextState(self, nextState):
        self.nextStates.add(nextState)
