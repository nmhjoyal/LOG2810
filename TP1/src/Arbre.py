from Vehicule import Vehicule
import copy

# Classe Arbre
#   racine : l'identifiant du sommet qui servira comme racine de l'arbre
class Arbre:
    def __init__(self, racine):
        self.racine = NoeudArbre(racine, 0, None)

    # racine est de type NoeudArbre, il appelle donc la fonction remplirEnfants.
    # La fonction prend la liste de sommets et la matrice d'aretes pour bâtir l'arbre.
    def remplirArbre(self, listeSommets, matriceAretes, typeVehicule, etatPatient):
        self.racine.remplirEnfants(listeSommets, matriceAretes, typeVehicule, etatPatient, [])

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
        self.enfants = []
        

    # Fonction prenant en paramètre la liste des sommets et la matrice des arcs d'un graphe afin de
    # bâtir l'arbre correspondant
    def remplirEnfants(self, listeSommets, matriceAretes, typeVehicule, etatPatient, sommetsVisites):
        sommetsVisitesCourant = copy.deepcopy(sommetsVisites)
        print(sommetsVisitesCourant)
        if (self.parent is not None):
            sommetsVisitesCourant.append(self.parent.sommet)
        vehicule = Vehicule(typeVehicule)

        # Pour chaque élément de la liste de sommets, nous vérifions s'il existe un arc entre les sommets.
        if (vehicule.parcourirCheminSansRecharge):
            for i in range(len(listeSommets)):

                if matriceAretes[self.sommet - 1][i] is not None:
                    # Avant d'ajouter l'élément à l'arbre, nous vérifions qu'il n'existe pas déjà dans le chemin simple,
                    # et que la nouvelle distance ne dépense pas plus que 80% de la batterie
                    distance = self.obtenirDistance() + matriceAretes[self.sommet - 1][i].longueur
                    if not self.sommet in sommetsVisitesCourant and vehicule.parcourirCheminSansRecharge(distance, etatPatient):
                        next = NoeudArbre(i + 1, self.distance + matriceAretes[self.sommet - 1][i].longueur, self)
                        self.enfants.append(next)

        # Pour chaque enfant nouvellement ajouté, nous rappelons la fonction sur ceux-ci
        for i in range(len(self.enfants)):
            if (len(self.enfants)>0):
                distance = self.enfants[i].obtenirDistance()
                if not self.enfants[i].estBloque(listeSommets, matriceAretes, sommetsVisitesCourant) and vehicule.parcourirCheminSansRecharge(distance, etatPatient):
                    self.enfants[i].remplirEnfants(listeSommets, matriceAretes, typeVehicule, etatPatient, sommetsVisitesCourant)

    # Retourne la distance correspondant au Noeud
    def obtenirDistance(self):
        return self.distance

    # Fonction qui vérifie si chaque sommet lié au sommet courant existe déjà dans ce chemin
    def estBloque(self, listeSommets, matriceAretes, sommetsVisites):
        bloque = []
        for i in range(len(listeSommets)):
            if matriceAretes[self.sommet - 1][i] is not None:
                if listeSommets[i] in sommetsVisites:
                    bloque.append(True)
                else:
                    bloque.append(False)
        #Retourne true si aucun false est dans bloqué et (si aucun false est dans bloqué, alors il y a bloquage).
        if False not in bloque:
            return True

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
        if not len(self.enfants) == 0:
            for i in range(len(self.enfants)):
                self.enfants[i].creerListeChemins(liste)
        else:
            liste.append(self)

    # Fonction qui affiche un chemin (en partant du sommet final)
    def afficheChemin(self, string):
        if self.parent is not None:
            self.parent.afficheChemin(string)

        string.append(str(self.sommet) + " > ")