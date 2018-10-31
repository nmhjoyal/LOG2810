from enum import Enum
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



    def extraireSousGraphe(self, pointDepart, etiquettesSommets, vehicule, categoriePatient, cheminMax):

        noChemin = 0

        for indiceSommet in range(len(self.listeSommets)):
            listeChemins = [noChemin, [pointDepart, 0, []]]
            if self.matriceArete[pointDepart - 1][indiceSommet] is not None:
                temp = copy.deepcopy(listeChemins[noChemin])
                temp[1] += int(self.matriceArete[pointDepart - 1][indiceSommet].longueur)
                temp[2].append(indiceSommet)
                tempVehicule = Vehicule(vehicule.type)

                currentSommet = pointDepart - 1
                prochainSommet = indiceSommet

                while tempVehicule.parcourirCheminSansRecharge(temp, categoriePatient):
                    listeChemins[noChemin][1] += self.matriceArete[currentSommet][prochainSommet].longueur
                    listeChemins[noChemin][2].append(prochainSommet)

                    for indiceProchain in range(len(self.listeSommets)):
                        if self.matriceArete[prochainSommet][indiceProchain] is not None:
                            pointExisteDeja = False
                            for point in listeChemins[noChemin][2]:
                                if indiceProchain + 1 == point:
                                    pointExisteDeja = True
                                    break
                            if not pointExisteDeja:
                                temp = copy.deepcopy(listeChemins[noChemin])
                                temp[1] += int(self.matriceArete[prochainSommet][indiceProchain].longueur)
                                temp[2].append(indiceProchain)
                                tempVehicule = Vehicule(vehicule.type)
                                if tempVehicule.parcourirCheminSansRecharge(temp, categoriePatient):
                                    listeChemins[noChemin][1] += self.matriceArete[currentSommet][prochainSommet].longueur
                                    listeChemins[noChemin][2].append(prochainSommet)
                                    noChemin += 1
                                    listeChemins[noChemin] = copy.deepcopy(listeChemins[noChemin - 1])
                                    prochainSommet = indiceProchain
                                    break




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
