from Vehicule import Vehicule
from ClassesGraphe import Graphe
import copy

class Arbre:
    def __init__(self, racine):
        self.racine = NoeudArbre(racine, 0, None)

    def fillArbre(self, listeSommets, listeAretes, typeVehicule, etatPatient):
        self.racine.fillChildren(listeSommets, listeAretes, typeVehicule, etatPatient)

    def afficheArbre(self):
        print(str(self.racine.sommet) +"\n")
        self.racine.afficheChildren("> ")

    def trouvePlusLongChemin(self):
        liste = []
        self.racine.trouvePlusLongChemin(liste)

class NoeudArbre:
    def __init__(self, sommet, distance, parent):
        self.sommet = sommet
        self.distance = distance
        self.parent = parent
        self.children = []

    def fillChildren(self, listeSommets, listeAretes, typeVehicule, etatPatient):

        vehicule = Vehicule(typeVehicule)

        for i in range(len(listeSommets)):
            if listeAretes[self.sommet - 1][i] is not None:
                if not self.sommetExiste(i + 1):
                    next = NoeudArbre(i + 1, self.distance + listeAretes[self.sommet - 1][i].longueur, self)
                    self.children.append(next)

        for i in range(len(self.children)):
            distance = self.children[i].getDistance()
            if vehicule.parcourirCheminSansRecharge(distance, etatPatient):
                self.children[i].fillChildren(listeSommets, listeAretes, typeVehicule, etatPatient)

    def getDistance(self):
        return self.distance

    def sommetExiste(self, sommet):
        if self.parent is not None:
            if self.parent.sommet == sommet:
                return True
            else:
                return self.parent.sommetExiste(sommet)
        else:
            return False


    def afficheChildren(self, prefixe):
        if self.children is not None:
            for i in range(len(self.children)):
                print(prefixe + str(self.children[i].sommet) + " " + str(self.children[i].distance) + "\n")
                self.children[i].afficheChildren("> " + prefixe)
        else:
            print(prefixe + str(self.sommet) + " " + str(self.distance) + "\n")

    def trouvePlusLongChemin(self, liste):
        if self.children is not None:
            for i in range(len(self.children)):
                self.children[i].trouvePlusLongChemin(liste)
                return liste
        else:
            return liste.append(self.distance)


def mainTest():
    graphe = Graphe("centresLocaux.txt")
    arbre = Arbre(2)
    arbre.fillArbre(graphe.listeSommets, graphe.matriceArete, 1, 2)

    listInOrder = arbre.trouvePlusLongChemin()
    maxDist = 0

    for i in range(len(listInOrder)):
        if listInOrder[i] > maxDist:
            maxDist = listInOrder[i]
    print("\n" + str(maxDist))

if __name__ == "__main__":
    mainTest()