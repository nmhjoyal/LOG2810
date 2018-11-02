from enum import Enum
from decimal import Decimal
import copy

class CLSC(Enum):
    Montreal_Nord =1
    Ahuntsic = 2
    Bordeaux_Cartierville = 3
    Saint_Laurent = 4
    René_Cassin = 5
    Notre_Dame_de_Grâce_Montréal_Ouest = 6
    Villeray = 7
    La_Petite_Patrie = 8
    Dorval_Lachine = 9
    LaSalle = 10
    St_Louis_du_parc = 11
    Faubourgs = 12
    Plateau_Mont_Royal = 13
    Olivier_Guimond = 14
    Hochelaga_Maisonneuve = 15
    Rosemont = 16
    Côte_des_Neiges = 17
    Métro = 18
    Parc_extension = 19 
    Lac_Saint_Louis = 20
    Pierrefonds = 21
    Rivière_des_Prairies = 22
    Pointe_aux_Trembles_Montréal_Est = 23
    Mercier_est_anjou = 24
    Saint_Léonard = 25
    Saint_Michel = 26
    Pointe_saint_charles = 27
    Verdun = 28
    Saint_Henri = 29

class Arete:
    def __init__(self, longueur):
        self.longueur=longueur

class Sommet:
    def __init__(self, identifiant, borne):
        self.identifiant=identifiant
        self.borne=borne

    def obtenirNomSommet(self):
        return str(CLSC(self.identifiant).name.replace("_","-"))

class Vehicule:
    def __init__(self, typeAmbulance):
        self.type = typeAmbulance
        self.batterie = 100
        self.tempsParcouru = 0
        self.clscsVisites = []
        #Definit la consommation horaire dependamment du type de voiture
        #0 = NI-MH
        if(self.type==0):
            self.consommationHoraire=[6,12,48]
        #1 = LI-Ion
        else:
            self.consommationHoraire=[5, 10, 30]
    
    def reinitialiser(self):
        self.batterie = 100
        self.tempsParcouru = 0
        self.clscsVisites = []
    
    def parcourirChemin(self, etiquetteSommet, categoriePatient):
        #Initialisation des valeurs pour parcourir le chemin
        consommationParMinute = self.consommationHoraire[categoriePatient]/60
 
        #Parcours chaque arete
        for i in range(len(etiquetteSommet[2])):
            tempsRestant = 0
            self.batterie -= round(Decimal(etiquetteSommet[1][i])*Decimal(consommationParMinute),2)
            self.tempsParcouru += etiquetteSommet[1][i]
            self.clscsVisites.append(etiquetteSommet[2][i].identifiant)
            
            #Détermine le temps restant jusqu'a la prochaine borne ou a la destination
            for j in range(i+1, len(etiquetteSommet[1])):
                tempsRestant += etiquetteSommet[1][j]
                if etiquetteSommet[2][j].borne:
                    break

        self.batterie -= sum(etiquetteSommet[1])*consommationParMinute
        #Vérifier si le véhicule peut faire le trajet sans batteries    
        if self.batterie > 20:
            print("Parcours suffisamment court, we gud")
            self.tempsParcouru = sum(etiquetteSommet[1])
        else:
            #On reinitialise batterie a 100 pour refaire le trajet complet avec recharges
            self.batterie = 100

            #Parcour chaque Arete
            for i in range(len(etiquetteSommet[1])):
                print(self.batterie)
                print(etiquetteSommet[1][i])
                print(consommationParMinute)
                print(round(etiquetteSommet[1][i]*consommationParMinute))
                self.batterie -= etiquetteSommet[1][i]*consommationParMinute
                self.tempsParcouru += etiquetteSommet[1][i]

                if ((i+1 <= len(etiquetteSommet)) and etiquetteSommet[2][i+1].borne == 1) and \
                   (self.batterie - (sum(etiquetteSommet[1],i+1)*consommationParMinute) < 20):
                    self.batterie = 100
                    self.tempsParcouru += 120

                elif (self.batterie < 20):
                    print("Peut pas recharger, autre chemin ou vehicule")
                    return False

            #Si la batterie est au-dessus de 20, il possible de continuer le trajet
            if (self.batterie >=20):
                #Verifie qu'on ne soit pas deja a la fin
                if i < len(etiquetteSommet[2]):
                    #Verifie s'il y a une borne
                    if etiquetteSommet[2][i].borne == 1: 
                        #Si on arrive a la prochaine borne ou la fin du trajet avec moins de 20%, on recharge
                        if self.batterie - round(Decimal(tempsRestant)*Decimal(consommationParMinute),2) < 20:
                            self.batterie = 100
                            self.tempsParcouru += 120
            #Si la batterie est rendue sous 20, il est impossible de réaliser le trajet
            else:
                return False
        #Parcours réussi
        return True

    def afficherInfos(self):
        #Affichage de toutes les informations demandees sur le véhicule
            print("Type de véhicule utilisé: ", end ="")
            if (self.type==0):
                print("NI-MH")
            else: 
                print("LI-ion")
            print ("Pourcentage final dans la batterie: {:0.2f}%".format(self.batterie))
            print ("Durée du chemin: {:} minutes ".format(self.tempsParcouru))
            print ("Chemin emprunté: ", end="")
            chemin = ""
            for i in self.clscsVisites:
                chemin += str(i) + "\u2192 "        
            chemin = chemin[:-2]
            print(chemin)

    def parcourirCheminSansRecharge(self, etiquetteSommet, categoriePatient):
        consommationParMinute = self.consommationHoraire[categoriePatient]/60

        self.batterie -= etiquetteSommet[1]*consommationParMinute

        if self.batterie > 20:
            self.tempsParcouru = etiquetteSommet[1]
            return True
        else:
            return False


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
            

#TODO: METTRE INFINI A NONE

            print(v.batterie)
            print("nope")


    def extraireSousGraphe(self, pointDepart, etiquettesSommets, vehicule, categoriePatient, cheminMax):

        for indiceSommet in range(len(self.listeSommets)):
            if self.matriceArete[pointDepart - 1][indiceSommet] is not None:
                pointExisteDeja = False
                for point in etiquettesSommets[2]:
                    if indiceSommet + 1 == point:
                        pointExisteDeja = True
                        break
                if not pointExisteDeja:
                    temp = copy.deepcopy(etiquettesSommets)
                    temp[1] += int(self.matriceArete[pointDepart - 1][indiceSommet].longueur)
                    temp[2].append(indiceSommet)
                    tempVehicule = Vehicule(vehicule.type)
                    if tempVehicule.parcourirCheminSansRecharge(temp, categoriePatient):
                        etiquettesSommets[1] += int(self.matriceArete[pointDepart - 1][indiceSommet].longueur)
                        etiquettesSommets[2].append(indiceSommet + 1)
                        self.extraireSousGraphe(indiceSommet + 1, etiquettesSommets, vehicule, categoriePatient, cheminMax)
                    else:
                        if cheminMax[1] > etiquettesSommets[1]:
                            cheminMax = copy.deepcopy(etiquettesSommets)
                            etiquettesSommets = [pointDepart, 0, []]
                            vehicule = Vehicule(vehicule.type)

        return cheminMax
