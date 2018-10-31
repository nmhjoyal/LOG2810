import Vehicule
import CLSC

class Arete:
    def __init__(self, longueur):
        self.longueur=longueur


class Sommet:
    def __init__(self, identifiant, borne):
        self.identifiant=identifiant
        self.borne=borne

    def obtenirNomSommet(self):
        return str(CLSC(self.identifiant).name.replace("_","-"))


class Graphe:

    def __init__(self, nomFichier):
        self.listeSommets = []
        self.matriceArete = []
        self.creerGraphe(nomFichier, 1)

    #Fonction qui crée une matrice contenant les relation entre chaque CLSC
    #et la distance qui les sépare
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

    #(POUR L'INSTANT) Trouve le plus court chemin qui relie 2 point
    def plusCourtChemin(self, origine, destination, categoriePatient):

        etiquettesSommets = []
        sommetsSousGraphe= []
        infini = 9999999999
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
                if (sum(etiquettesSommets[j][1]) < plusPetiteDistance) and not(etiquettesSommets[j][0].identifiant in sommetsSousGraphe):
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

        v = Vehicule(0)
        reussite = v.parcourirChemin(etiquettesSommets[destination-1], categoriePatient)

        if reussite:
            #Affichage de toutes les informations demandees sur le véhicule
            print("Type de véhicule utilisé: ", end ="")

            if (v.type==0):
                print("NI-MH")
            else:
                print("LI-ion")
            print("Pourcentage final dans les batteries: {:0.2f}%".format(v.batterie))

            print("Chemin utilisé: ", end="")
            chemin = ""
            for i in etiquettesSommets[destination-1][categoriePatient]:
                chemin += str(i.identifiant) + "\u2192 "
            chemin = chemin[:-2]
            print(chemin)
            print("Durée du chemin: {:} minutes ".format(v.tempsParcouru), end="")
        else:
            print(v.batterie)
            print("nope")