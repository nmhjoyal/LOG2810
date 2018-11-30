from state import State
import queue

class Automate:
    def __init__(self, lexicon):
        self.origin = State()
        self.currentState = self.origin
        self.createAutomate(lexicon)
        self.fiveLast = queue.Queue(5)

    def createAutomate(self, lexicon):

        for i in lexicon: #pour chaque ligne
            self.currentState = self.origin #on revient au point de départ à chaque nouveau mot
            for j in i:#pour chaque caractère
                int index = ord(j)
                if self.currentState.getState(index) is None : #si on a pas encore d'enfants pour cette lettre
                    
                    self.currentState.setState(index,State)

                self.states[self.currentId] = State(self.currentId, i)
