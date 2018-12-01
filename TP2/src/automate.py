from state import State
import queue

class Automate:
    def __init__(self, lexicon):
        self.origin = State(None)
        self.currentState = self.origin
        self.createAutomate(lexicon)
        self.fiveLast = queue.Queue(5)

    def createAutomate(self, lexicon):
        if not open(lexicon, "r"):
            raise IOError

        f = open(lexicon, "r")
        for i in f:  # pour chaque ligne
            self.currentState = self.origin  # on revient au point de départ à chaque nouveau mot
            for j in i:  # pour chaque caractère
                if j is not "\n":
                    self.currentState.fill(j)  # regarde si l'enfant est deja present et le rajoute s'il ne l'est pas
                    self.currentState = self.currentState.getState(j)
                else:  # si c'est la fin du mot
                    self.currentState.makeTerminal()
                    word = i[:-1]
                    self.currentState.addWord(word)  # ajoute le mot au current state et à tous ses parents
        self.currentState = self.origin

    def add(self, lettre): # on ajoute une lettre
        child = self.currentState.getState(lettre)
        if child is 0:
            print("Attention le mot que vous tapez n'existe pas dans le lexique")
        else:
            self.currentState = child


    def findWords(self, lettres):
        self.currentState = self.origin
        for char in lettres:
            if type(char) is not str:
                raise TypeError
            self.currentState = self.currentState.getState(char)
        print (self.currentState.words)
        #return self.currentState.words

    def enter(self, char):
        if char == " " or char == ".":  # si c'est un espace ou une ponctuation met fin au met et met les labels à jour
            if self.currentState.isTerminal():
                self.currentState.addTimesUsed()
                if self.fiveLast.full():  # si la queue est pleine enleve le premier
                    temp = self.fiveLast.get(False)  # récupere le mot et indique qu'il n'est plus dans les 5 derniers
                    temp.removeLastFive()
                self.fiveLast.put_nowait(self.currentState)
                self.currentState.makeLastFive()
                self.currentState = self.origin
            else:  # si le mot terminé n'est pas un mot du lexique
                print("attention tu es cave ce mot n'existe pas")
                #return("Attention tu es cave ce mot n'existe pas")

        else:  # passe au prochain état si c'est une lettre
            self.add(char)

    def getFiveLast(self):
        return self.fiveLast