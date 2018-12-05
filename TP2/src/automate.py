from state import State
import queue

class Automate:
    def __init__(self, lexicon):
        self.origin = State(None)
        self.currentState = self.origin
        self.createAutomate(lexicon)
        self.fiveLast = queue.Queue(5)
        self.lastWord = ""

    def createAutomate(self, lexicon):
        if not open(lexicon, "r"):
            raise IOError

        f = open(lexicon, "r")
        for i in f:  # pour chaque ligne
            self.currentState = self.origin  # on revient au point de départ à chaque nouveau mot
            for j in i:  # pour chaque caractère
                if self.isAlphanumerical(j):
                    if j is not "\n":
                        self.currentState.fill(j)  # regarde si l'enfant est deja present et le rajoute s'il ne l'est pas
                        self.currentState = self.currentState.getState(j)
                    else:  # si c'est la fin du mot
                        self.currentState.makeTerminal()
                        word = i[:-1]
                        self.currentState.addWord(word)  # ajoute le mot au current state et à tous ses parents
        self.currentState = self.origin


    def findWords(self, lettres):
        self.currentState = self.origin
        isLastChar = False

        i=1 #Nombre de caracteres traités
        for char in lettres:
            if type(char) is not str:
                raise TypeError
            if i == len(lettres):
                isLastChar = True
            self.add(char,isLastChar)
            i += 1 
        self.setLastWord(lettres)

        return self.currentState.words

    def add(self, char, isLastChar):
        self.currentState = self.currentState.getState(char)
        if self.currentState.isTerminal() and isLastChar:        
                self.currentState.addTimesUsed()
                if self.fiveLast.full():  # si la queue est pleine enleve le premier
                    temp = self.fiveLast.get(False)  # récupere le mot et indique qu'il n'est plus dans les 5 derniers
                    temp.removeLastFive()
                self.fiveLast.put_nowait(self.currentState)
                self.currentState.makeLastFive()
        if self.currentState == 0:
            print("Attention le mot que vous tapez n'existe pas dans le lexique")

    def findWordsWithoutUpdate(self, lettres):
        self.currentState = self.origin
        for char in lettres:
            if type(char) is not str:
                raise TypeError
            self.addWithoutUpdate(char)
        self.setLastWord(lettres)
        return self.currentState.words

    def addWithoutUpdate(self, char):
        self.currentState = self.currentState.getState(char)

    def backspace(self):
        if self.currentState.getParent() is not None:
            self.currentState = self.currentState.getParent()

    def getFiveLast(self):
        return self.fiveLast

    def getLabel(self):  # retourne les label du current state, donc du mot en train de s'écrire
        if self.currentState.isTerminal():
            timeused = self.currentState.getTimeused()
            fivelast = self.currentState.ifLastFive()
            return (timeused, fivelast)  # retourne le nbr de fois utilisé en premier et s'il a été dans les 5 dernier mot dit dans le 2ieme
        else:
            return (0,0)

    def getAllLabel(self, lexicon):
        current = self.currentState

        self.currentState = self.origin
        if not open(lexicon, "r"):
            raise IOError

        f = open(lexicon, "r")
        for i in f:  # pour chaque ligne
            self.currentState = self.origin  # on revient au point de départ à chaque nouveau mot
            for j in i:  # pour chaque caractère
                if j is "\n":
                    print(i, self.currentState.getTimeused(), self.currentState.ifLastFive())
                    break
                else:
                    self.currentState = self.currentState.getState(j)
        self.currentState = current

    def setLastWord(self, word):
        self.lastWord = word

    def isLastWord(self, word):
        if (word == self.lastWord):
            return True
        else: 
            return False

    def isAlphanumerical(self, char):
        index = ord(char) - 97
        if 155 > index >= 0 or index == -58 or index == 242 or char == "\n":
            return True
        else:
            return False