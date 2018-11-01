import unittest
from ClassesGraphe import Graphe
from Arbre import Arbre

class Tests(unittest.TestCase):
    def testArbre(self):
        graphe = Graphe("centresLocaux.txt")
        arbre = Arbre(2)
        arbre.fillArbre(graphe.listeSommets, graphe.matriceArete, 0, 1)


