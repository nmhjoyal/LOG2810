from state import State
import queue

class Automate:
    def __init__(self, lexicon):
        self.origin = State()
        self.currentState = self.origin
        self.createAutomate(lexicon)
        self.fiveLast = queue.Queue(5)

    def createAutomate(self, lexicon):

        for i in lexicon:  # pour chaque ligne
            self.currentState = self.origin  # on revient au point de départ à chaque nouveau mot
            for j in i:  # pour chaque caractère
                if j is not "\n":
                    self.currentState.fill(j)  # regarde si l'enfant est deja present et le rajoute s'il ne l'est pas
                    self.currentState = self.currentState.getState(j)
                else: #si c'est la fin du mot
                    self.currentState.makeTerminal()
                    word = i[:-1]
                    self.currentState.addWord(word)  # ajoute le mot au current state et à tous ses parents



