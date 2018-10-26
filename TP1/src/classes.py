from enum import Enum

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
    Hochelage_Maisonneuve = 15
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
        self.consommationHoraire = []
        
        #Definit la consommation horaire dependamment du type
        #0 = NI-NH
        if(type==0):
            self.consommationHoraire=[6,12,48]
        #1 = LI-Ion
        else:
            self.consommationHoraire=[5, 10, 30]

    def parcourirChemin(self, etiquetteSommet, categoriePatient):
            self.batterie -= etiquetteSommet[1]*(self.consommationHoraire[categoriePatient]/60)            
            if self.batterie > 20:
                print("Parcours suffisamment court, we gud")
                return self.batterie
            else: 
                print("Parcours trop long")
                return self.batterie
        

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
                if int(info[0]) == numeroSommet:
                    n = numeroSommet - len(self.listeSommets)
                    if (n > 0):
                        for i in (range(n)):
                            self.listeSommets.append(None)
                    if self.listeSommets[numeroSommet-1] == None:
                        self.listeSommets[numeroSommet-1] = Sommet(numeroSommet, info[1])

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

            if self.matriceArete[nd1-1][nd2-1] == None or self.matriceArete[nd2-1][nd1-1] == None:
                nouvelleArete = Arete(dist)
                if nd1 == numeroSommet:  
                    self.matriceArete[nd1-1][nd2-1]=nouvelleArete
                    self.matriceArete[nd2-1][nd1-1]=nouvelleArete     
                    self.creerGraphe(nomFichier, nd2)
                elif nd2 == numeroSommet:
                    self.matriceArete[nd1-1][nd2-1]=nouvelleArete
                    self.matriceArete[nd2-1][nd1-1]=nouvelleArete
                    self.creerGraphe(nomFichier, nd1)              

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
                    txt+= "(" + str(k) + " " + str(CLSC(k).name.replace("_","-")) + ", "+ str(j.longueur) + "),"
                k += 1    
            txt = txt[:-1]
            txt += "))"
            print(txt)

    #(POUR L'INSTANT) Trouve le plus court chemin qui relie 2 point
    def plusCourtChemin(self, origine, destination, categoriePatient):
        
        etiquettesSommets = []
        sommetsSousGraphe= []
        infini = 999999    
        sommetCourant = 0          
        
        #Remplissage de la liste avec les étiquettes désirées
        #De sorte que [arondissement,infini,[]] pour les sommets autre que l'origine
        #et [arrondissement, 0, [arrondissement]] pour l'origine
        for i in range(len(self.listeSommets)):
            if not i+1 == origine:
                etiquettesSommets.append([self.listeSommets[i],infini, []])
            else:
                etiquettesSommets.append([self.listeSommets[i],0, [i+1]])          

        #Tant que le sommet désiré n'est pas atteint ou que le sous-graphe n'est pas plein, on continue
        while (not(destination in sommetsSousGraphe) and len(sommetsSousGraphe) <= len(self.listeSommets)):
            plusPetiteDistance = infini  
            
            #On trouve le sommet de distance minimale par rapport à l'origine
            for j in range(len(etiquettesSommets)):
                if (etiquettesSommets[j][1] < plusPetiteDistance) and not(etiquettesSommets[j][0].identifiant in sommetsSousGraphe):
                    plusPetiteDistance = etiquettesSommets[j][1]
                    sommetCourant = etiquettesSommets[j][0].identifiant
                
            sommetsSousGraphe.append(sommetCourant)
            indice = 0
            #On met à jour les étiquettes des sommets reliés au sommet courant 
            #s'il y a changement à faire
            for j in self.matriceArete[sommetCourant-1]:
                
                #S'il n'y a pas d'arete qui connecte les 2 sommets, on ne modifie pas l'étiquette
                if j is not None:                    
                    #Si la distance par le nouveau chemin est plus petite, on met à jour l'étiquette
                    if etiquettesSommets[sommetCourant-1][1] + j.longueur < etiquettesSommets[indice][1]:
                        etiquettesSommets[indice][1] = etiquettesSommets[sommetCourant-1][1] + j.longueur
                        etiquettesSommets[indice][2] = etiquettesSommets[sommetCourant-1][2].copy()
                        etiquettesSommets[indice][2].append(indice+1)
                indice+=1
        
        v = Vehicule(0)
        batterieRestante = v.parcourirChemin(etiquettesSommets[destination-1], 2)
        
        #Affichage de toutes les informations demandees sur le véhicule
        print("Type de véhicule utilisé: ", end ="")
        if (v.type==0):
            print("NI-NH")
        else: 
            print("LI-ion")
        print ("Pourcentage final dans les batteries: ", end="")
        print (batterieRestante)
        print ("Chemin utilisé: ", end="")

        chemin = ""
        for i in etiquettesSommets[destination-1][categoriePatient]:
            chemin += str(i) + "->"        
        chemin = chemin[:-2]
        print(chemin)
        

        #A RETOURNER : type vehicule utilise (NI-NH ou LI-ion)
        #  % energie final, +court chemin, longueur en minutes,  si refusé : message excuse