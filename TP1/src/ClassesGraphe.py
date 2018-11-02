from Vehicule import Vehicule
from CLSC import CLSC
from Arbre import Arbre
import copy

# Classe Arete
#   longueur : représente la longueur entre deux sommets (en minutes)
class Arete:
    def __init__(self, longueur):
        self.longueur = longueur


# Classe Sommet
#   identifiant : représente le sommet (1, 2, ..., 29)
#   borne : 1 si il y a une borne de recherge au sommet correspondant, 0 sinon
class Sommet:
    def __init__(self, identifiant, borne):
        self.identifiant = identifiant
        self.borne = borne

    def obtenirNomSommet(self):
        return str(CLSC(self.identifiant).name.replace("_", "-"))


# Classe Graphe
#   listeSommets : représente la liste de sommets
#   listeSommets : représente la liste de sommets qui sont des bornes
#   matriceArete : représente la matrice des arcs du graphe. Si la valeur à la position [i, j]
#                  est non-nulle, les sommets i + 1 et j + 1 sont reliés avec la distance correspondante
#   etiquettesSommetsPossibles : représente les étiquettes de tous les chemins possibles entre des sommets spécifiés
class Graphe:
    def __init__(self, nomFichier):
        self.listeSommets = []
        self.listeSommetsAvecBornes = []
        self.matriceArete = []
        self.etiquettesSommetsPossibles = []
        self.creerGraphe(nomFichier, 1)

    #Fonction qui crée une matrice contenant les relation entre chaque CLSC 
    #et la distance qui les sépare
    def creerlisteSommetsAvecBornes(self):
        self.listeSommetsAvecBornes = []
        for i in self.listeSommets:
            if i.borne:
                self.listeSommetsAvecBornes.append(i)

    def creerGraphe(self, nomFichier, numeroSommet):
        f = open(nomFichier, "r")

        #Arriver a la fin de la première partie en gardant la dernière valeur
        #Afin de connaître la grandeur du tableau a initialiser et initialise
        #le sommet.
        for ligne in f:
            if ligne == "\n":
                break
            else:                    
                info = ligne.split(",")
                self.listeSommets.append(Sommet(int(info[0]), int(info[1])))

        #Initialisation de la matrice avec la taille necessaire si elle n'existe pas deja
        if len(self.matriceArete) == 0:
            self.matriceArete = [[None for x in range(int(info[0]))] for y in range(int(info[0]))]

        #Iteration au travers de la deuxième partie et ajout a la matrice
        #des aretes les aretes initialises avec leur distance
        for ligne in f:
            noeuds = ligne.split(",")
            nd1 = int(noeuds[0])
            nd2 = int(noeuds[1])
            dist = int(noeuds[2])
            nouvelleArete = Arete(dist)
            self.matriceArete[nd1-1][nd2-1]=nouvelleArete
            self.matriceArete[nd2-1][nd1-1]=nouvelleArete    
        
        f.close()
        self.creerlisteSommetsAvecBornes()

    #Afficher le graphe selon les spécifications
    def lireGraphe(self):
        #Itère au travers de chaque sommet
        for i in self.listeSommets:
            k=1
            txt=""
            txt+= "(" + i.obtenirNomSommet() + ", " + str(i.identifiant) + ", ("
            
            #Itère au travers de chaque Arete et affiche le CLSC relié et la longueur
            for j in self.matriceArete[i.identifiant-1]:
                if j != None:
                    txt+= "(" + str(CLSC(k).name.replace("_","-")) + ", "+ str(j.longueur) + " mins),"
                k += 1    
            txt = txt[:-1]
            txt += "))"
            print(txt)

    #Fonction qui détermine le plus court chemin selon la matrice donnée avec l'algorithme de Dijkstra
    def dijkstra(self, origine, destination):
        etiquettesSommets = []
        sommetsSousGraphe= []
        infini = 99999999
        sommetCourant = 0          
        
        #Remplissage de la liste avec les étiquettes désirées
        #De sorte que [arondissement,infini,[]] pour les sommets autre que l'origine
        #et [arrondissement, 0, [arrondissement]] pour l'origine
        for i in range(len(self.listeSommets)):
            if not i+1 == origine:
                etiquettesSommets.append([self.listeSommets[i],[infini], []])
            else:
                etiquettesSommets.append([self.listeSommets[i],[0], [self.listeSommets[i]]])          

        #Tant que le sommet désiré n'est pas atteint ou que le sous-graphe n'est pas plein, on continue
        while (not(destination in sommetsSousGraphe) and len(sommetsSousGraphe) <= len(self.listeSommets)):
            plusPetiteDistance = infini
            
            #On trouve le sommet de distance minimale par rapport à l'origine
            for j in range(len(etiquettesSommets)):
                if (sum(etiquettesSommets[j][1]) < plusPetiteDistance ) and not(etiquettesSommets[j][0].identifiant in sommetsSousGraphe):
                    plusPetiteDistance = sum(etiquettesSommets[j][1])
                    sommetCourant = int(etiquettesSommets[j][0].identifiant)
                
            sommetsSousGraphe.append(sommetCourant)
            indice = 0
            #On met à jour les étiquettes des sommets reliés au sommet courant 
            #s'il y a changement à faire
            for j in self.matriceArete[sommetCourant-1]:
                #S'il n'y a pas d'arete qui connecte les 2 sommets, on ne modifie pas l'étiquette
                if j is not None:                    
                    #Si la distance par le nouveau chemin est plus petite, on met à jour l'étiquette
                    if sum(etiquettesSommets[sommetCourant-1][1]) + j.longueur < sum(etiquettesSommets[indice][1]):
                        etiquettesSommets[indice][1] = etiquettesSommets[sommetCourant-1][1].copy()
                        etiquettesSommets[indice][1].append(j.longueur)
                        etiquettesSommets[indice][2] = etiquettesSommets[sommetCourant-1][2].copy()
                        etiquettesSommets[indice][2].append(self.listeSommets[indice])
                indice+=1

        return etiquettesSommets[destination-1]
    

    #Fonction qui retourne les etiquettes des chemins allant du départ jusqu'à la borne désirée
    def cheminsVersBornes(self, depart, bornesVisitees):

        etiquetteVersBorneTemp = []
        etiquettesVersBornes = []
        
        bornesVisiteesCourantes = copy.deepcopy(bornesVisitees)
        retourSurPas = False

        #Itère dans la liste de sommets pour savoir ou sont les bornes
        for i in self.listeSommetsAvecBornes:
            identifiantsSommetsVisites = []
            if (i.identifiant is not depart and i.identifiant not in bornesVisiteesCourantes):
                etiquetteVersBorneTemp = self.dijkstra(depart, i.identifiant)
                
                #On vérifie si la suite du parcours implique de retourner aux bornes précédemment
                #Visitées. Si oui, inutile d'ajouter à la liste puisque le chemin est automatiquement
                #plus long
                for j in etiquetteVersBorneTemp[2]:
                    identifiantsSommetsVisites.append(j.identifiant)
                for j in bornesVisiteesCourantes:
                    if j in identifiantsSommetsVisites:
                        retourSurPas = True

                if retourSurPas == False:
                    etiquettesVersBornes.append(etiquetteVersBorneTemp)

        return etiquettesVersBornes
    
    #Fonction qui retourne les etiquettes de tous les chemins possibles, passant par toutes les combinaisons de bornes
    #ou par aucune borne
    def obtenirCheminsComplets(self, depart, destination, etiquetteSommetPrecedent, bornesVisitees):
        #On détermine si c'est la première récursion
        if (len(etiquetteSommetPrecedent)) is 0:
            premierParcours=True
        else: 
            premierParcours=False

        #Copie profonde de bornesVisitees afin de pouvoir la manipuler independamment à chaque recursion
        bornesVisiteesCourantes = copy.deepcopy(bornesVisitees)
        etiquetteDepartVersDestination=self.dijkstra(depart,destination)
        etiquettesOrigineVersBornes = []


        # S'il y a une premiere récursion on ajoute le sommet de départ (puisqu'il correspond à une borne)
        if not premierParcours:
            bornesVisiteesCourantes.append(depart)
            #Copie profonde d'etiquetteSommetPrecedent s'il y a précédemment eu parcours
            etiquetteOrigineVersDestination=copy.deepcopy(etiquetteSommetPrecedent)
            etiquetteOrigineVersDestination[0]=etiquetteDepartVersDestination[0]
            #On fusionne les deux listes pour obtenir le chemin complet de l'origine vers la destination
            for j in range(0, len(etiquetteDepartVersDestination[1])):                
                etiquetteOrigineVersDestination[1].append(etiquetteDepartVersDestination[1][j])
                etiquetteOrigineVersDestination[2].append(etiquetteDepartVersDestination[2][j])
        else:
            #Si c'est le premier parcours, l'etiquette du parcours correspond à celle du parcours le plus court
            #Entre le 1er depart et l'origine
            etiquetteOrigineVersDestination=copy.deepcopy(etiquetteDepartVersDestination)
       
        etiquettesDepartVersBornes = self.cheminsVersBornes(depart, bornesVisiteesCourantes)
        
        #Si ce n'est pas le premier parcours, on fusionne toutes les listes de l'origine vers les bornes.
        #S'il y a autant de bornes qui sont visitées que de bornes existantes, il n'y a pas de fusion à faire
        if not premierParcours and len(etiquettesDepartVersBornes)>0:
            for i in range(0, len(etiquettesDepartVersBornes)-1):
                etiquettesOrigineVersBornes.append(copy.deepcopy(etiquetteSommetPrecedent))
                etiquettesOrigineVersBornes[i][0]=copy.deepcopy(etiquettesDepartVersBornes[i][0])
                for j in range(1, len(etiquettesDepartVersBornes[i][1])):
                    etiquettesOrigineVersBornes[i][1].append(etiquettesDepartVersBornes[i][1][j])
                    etiquettesOrigineVersBornes[i][2].append(etiquettesDepartVersBornes[i][2][j])
        
        #Si c'est le premier parcours, le depart correspont à l'origine, donc pas de fusion necessaire
        elif premierParcours:
            etiquettesOrigineVersBornes = copy.deepcopy(etiquettesDepartVersBornes)
    
        #On ajoute etiquetteSommetPossibles (l'etiquette du chemin jusqu'à destination) à la liste des chemins possibles
        self.etiquettesSommetsPossibles.append(copy.deepcopy(etiquetteOrigineVersDestination))

        #Pour chaque chemin partant du point de départ vers une borne qui n'a pas déja été visitée
        if(len(bornesVisiteesCourantes)<len(self.listeSommetsAvecBornes)):
            for i in etiquettesOrigineVersBornes:
                self.obtenirCheminsComplets(i[0].identifiant, destination, i, bornesVisiteesCourantes)

    #Fonction qui détermine s'il y a un plus court chemin possible en sélectionnant
    #le bon chemin et la bonne auto. Lorsque fini, affiche les informations sur le véhicule et le parcours
    def plusCourtChemin(self, origine, destination, categoriePatient):
        etiquetteSommetOptimal = []
        succes = False
        #Itère au travers de la boucle deux fois afin de tester les deux types
        #De véhicule (si nécessaire)
        for k in range(2):
            minTempsParcouru = -1
            v = Vehicule(k)
            self.etiquettesSommetsPossibles = []

            self.obtenirCheminsComplets(origine, destination, [], [])

            for i in self.etiquettesSommetsPossibles:
                v.reinitialiser()
                parcoursReussi = v.parcourirChemin(i, categoriePatient)
                #Si le chemin est parcourable, il y a succes et ce chemin est evalué pour voir s'il est le plus court
                #L'etiquette correspondant a ce chemin est de plus temporairement entreposé dans etiquetteSommetOptimal
                if parcoursReussi and (v.tempsParcouru < minTempsParcouru or minTempsParcouru is -1):
                    minTempsParcouru = v.tempsParcouru
                    etiquetteSommetOptimal = i.copy()
                    succes = True
            # #On sort de la boucle si le chemin a été exécuté avec succès avec le premier véhicule
            if succes:
                break
        #Si succès, on parcourt le chemin a nouveau et on affiche les informations
        if succes:
            v.reinitialiser()
            v.parcourirChemin(etiquetteSommetOptimal, categoriePatient)
            v.afficherInfos()
        else: 
            print("Désolé, le transport est impossible")
            

    # Fonction servant à afficher le plus long chemin à partir d'un point
    def extraireSousGraphe(self, point, typeVehicule, etatPatient):

        # On utilise la classe Arbre pour créer l'arbre de chemins simples possibles
        # variable point étant la racine de l'arbre
        arbre = Arbre(point)
        arbre.remplirArbre(self.listeSommets, self.matriceArete, typeVehicule, etatPatient)

        # Créer liste contenant les feuilles de l'arbres uniquement
        liste = []
        arbre.creerListeChemins(liste)
        maxDist = 0
        indexMax = -1

        # Trouver feuille ayant la plus grande distance (en min)
        for i in range(len(liste)):
            if liste[i].distance > maxDist:
                maxDist = liste[i].distance
                indexMax = i

        # Affichage du chemin et la longueur de celui-ci en minutes
        print("\nChemin le plus long sur une charge :\n")
        if not indexMax == -1:
            strChemin = []
            liste[indexMax].afficheChemin(strChemin)
            strChemin[len(strChemin) - 1] = strChemin[len(strChemin) - 1][:-3]
            for string in strChemin:
                print(string, end="")
        print("\nLongueur : " + str(maxDist) + " minutes\n")
