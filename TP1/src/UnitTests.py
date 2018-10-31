import Arbre
import unittest
import ClassesGraphe

class Tests(unittest.TestCase):
    def testArbre(self):
        graphe = ClassesGraphe("centresLocaux.txt")
        arbre = Arbre(2)
        arbre.fillArbre(graphe.listeSommets, graphe.matriceArete, 0, 1)

        arbre.afficheArbre()
