from Vehicule import Vehicule

# Classe Arbre
#   racine : l'identifiant du sommet qui servira comme racine de l'arbre
class Arbre:
    def __init__(self, racine):
        self.racine = NoeudArbre(racine, 0, None)

    # racine est de type NoeudArbre, il appelle donc la fonction fillChildren.
    # La fonction prend la liste de sommets et la liste d'aretes pour bâtir l'arbre.
    def fillArbre(self, listeSommets, listeAretes, typeVehicule, etatPatient):
        self.racine.fillChildren(listeSommets, listeAretes, typeVehicule, etatPatient)

    # Fonction qui crée la liste des feuilles de l'arbres (les chemins les plus long)
    def creerListeChemins(self, liste):
        self.racine.creerListeChemins(liste)

# Classe NoeudArbre
#   sommet : représente l'identifiant du noeud
#   distance : représente la distance entre le sommet et la racine
#              (la racine aura 0 car elle n'a pas de parent)
#   parent : Noeud précédent le noeud courant. Sert surtout à vérifier l'existance d'un
#            sommet particulier d'un chemin
class NoeudArbre:
    def __init__(self, sommet, distance, parent):
        self.sommet = sommet
        self.distance = distance
        self.parent = parent
        self.children = []

    # Fonction prenant en paramètre la liste des sommets et la liste des arcs d'un graphe afin de
    # bâtir l'arbre correspondant
    def fillChildren(self, listeSommets, listeAretes, typeVehicule, etatPatient):

        vehicule = Vehicule(typeVehicule)

        # Pour chaque element de la liste de sommets, nous vérifions qu'il existe un arc entre les sommets.
        for i in range(len(listeSommets)):
            if listeAretes[self.sommet - 1][i] is not None:

                # Avant d'ajouter l'élément à l'arbre, nous vérifions qu'il n'existe pas déjà dans le chemin simple,
                # et que la nouvelle distance ne dépense pas plus que 80% de la batterie
                distance = self.getDistance() + listeAretes[self.sommet - 1][i].longueur
                if not self.sommetExiste(i + 1) and vehicule.parcourirCheminSansRecharge(distance, etatPatient):
                    next = NoeudArbre(i + 1, self.distance + listeAretes[self.sommet - 1][i].longueur, self)
                    self.children.append(next)

        # Pour chaque enfant nouvellement ajouté, nous rappelons la fonction sur ceux-ci
        for i in range(len(self.children)):
            distance = self.children[i].getDistance()
            if not self.children[i].estBloque(listeSommets, listeAretes) and vehicule.parcourirCheminSansRecharge(distance, etatPatient):
                self.children[i].fillChildren(listeSommets, listeAretes, typeVehicule, etatPatient)

    # Retourne la distance correspondant au Noeud
    def getDistance(self):
        return self.distance

    # Fonction qui vérifie si chaque sommet lié au sommet courant existe déjà dans ce chemin
    def estBloque(self, listeSommets, listeAretes):
        bloque = False
        for i in range(len(listeSommets)):
            if listeAretes[self.sommet - 1][i] is not None:
                if self.sommetExiste(i + 1):
                    bloque = True
                else:
                    bloque = False
        return bloque

    # Fonction qui vérifie l'existance d'un sommet dans le chemin
    def sommetExiste(self, sommet):
        if self.parent is not None:
            if self.parent.sommet == sommet:
                return True
            else:
                return self.parent.sommetExiste(sommet)
        else:
            return False

    # Fonction qui sert à créer la liste des feuilles de l'arbre
    # Utile afin de déterminer la distance la plus longue
    def creerListeChemins(self, liste):
        if not len(self.children) == 0:
            for i in range(len(self.children)):
                self.children[i].creerListeChemins(liste)
        else:
            liste.append(self)

    # Fonction qui affiche un chemin (en partant du sommet final)
    def afficheChemin(self, string):
        if self.parent is not None:
            self.parent.afficheChemin(string)

        string.append(str(self.sommet) + " > ")