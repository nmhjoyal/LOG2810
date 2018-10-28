import array as arr
from classes import Graphe
from classes import Vehicule

POINT_MAX = 29
POINT_MIN = 1

def main():
    #Initialisation du graphe et choix
    g = Graphe("centresLocaux.txt")
    #càg.plusCourtChemin(22,27,2)

    choix = ""
    print("Veulliez sélectionner une option ci-dessous (ex. entrer 'A' sur le clavier pour mettre à jour la carte")

    #INTERFACE
    #Menu principal, se réaffiche tant que l'usager ne rentre pas la lettre 'D'
    while(not(choix == "D")):
        choix = input("/--------------------------MENU--------------------------/ "
              "\n(A) Mettre à jour la carte."
              "\n(B) Déterminer le plus court chemin sécuritaire."
              "\n(C) Extraire sous-graphe."
              "\n(D) Quitter. \n")

        #Convertir en majuscule
        choix = choix.upper()
        if(choix == "A"):
            nomFichier = input("\nVeuillez entrer le nom du fichier contenant la carte voulue (extension .txt)\n")
            ouvrirFichierReussi = False
            #Redemande le nom d'un fichier tant qu'on trouve pas un fichier correspondant
            while(not(ouvrirFichierReussi)):
                try:
                    g = Graphe(nomFichier)
                    # ** Il faudra peut-être réinitialiser les variables globales POINT_MAX et POINT_MIN **

                    ouvrirFichierReussi = True
                #Affiche une erreur si nom du fichier n'existe pas
                except FileNotFoundError:
                    nomFichier = input("\nNom de fichier erroné, veuillez entrer le nom du fichier\n")
                    ouvrirFichierReussi = False

            g.lireGraphe()
            print("\nGraphe mis à jour\n")

        elif(choix == "B"):
            strA = input("\nVeuillez entrer le point de départ\n")
            strB = input("\nVeuillez entrer le point d'arrivée\n")
            donneesCorrectes = False

            #Redemande les points si les donnees entrées sont erronées
            while (not(donneesCorrectes)):
                try:
                    pointA = int(strA)
                    pointB = int(strB)

                    #Vérifie si les points se situent sur la carte
                    if(pointA >= POINT_MIN and pointA <= POINT_MAX and pointB >= POINT_MIN and pointB <= POINT_MAX):
                        donneesCorrectes = True
                        #g.plusCourtChemin(pointA, pointB, 2)
                    else:
                        strA = input("\nPoints ne se situent pas dans la carte, veuillez entrer un nouveau point de départ\n")
                        strB = input("\nVeuillez entrer le point d'arrivée\n")

                #Si l'usager rentre des points dans un format erroné (ex. un mot)
                except ValueError:
                    print("\nDonnées erronées, veuillez entrer les points par leur nombre correspondant\n")
                    strA = input("\nVeuillez entrer le point de départ\n")
                    strB = input("\nVeuillez entrer le point d'arrivée\n")
                    
        elif(choix == "C"):
            strPoint = input("\nVeuillez entrer le point de départ\n")
            donneesCorrectes = False

            #Redemande le point
            while(not(donneesCorrectes)):
                try:
                    point = int(strPoint)

                    #Vérifie si le point se situe sur la carte
                    if(point >= POINT_MIN and point <= POINT_MAX):

                        vehicule = input("\nVeuillez entrer le type d'ambulance\n")
                        vehicule = vehicule.upper()
                        if vehicule == "NI-NH" or vehicule == " LI-ION":
                            donneesCorrectes = True
                            if vehicule == "NI-NH":
                                objVehicule = Vehicule(0)
                            else:
                                objVehicule = Vehicule(1)
                            etatPatient = input("\nVeuillez entrer l'état du patient, soit : \n1 - faible risque,\n2 - risque moyen,\n3 - haut risque.\n")
                            etat = int(etatPatient)
                            etiquettesSommets = [point, 0, []]
                            cheminMax = [point, 0, []]
                            etiquettesSommets[2].append(point)
                            g.extraireSousGraphe(point, etiquettesSommets, objVehicule, etat - 1, cheminMax)
                            print("\nChemin le plus long sur une charge :\n")
                            output = ""
                            for point in etiquettesSommets[2]:
                                output += str(point)
                                output += " -> "
                            print(output[:-4] + "\n" + "Longueur : " + str(len(etiquettesSommets[2]) - 1))
                        else:
                            print("\nType d'ambulance invalide, veuillez rentrer les données\n")
                    else:
                        strPoint = input("\nPoint ne se situe pas dans la carte, veuillez entrer un nouveau point de départ\n")

                #Si l'usager rentre des points dans un format erroné (ex. un mot)
                except ValueError:
                    strPoint = input("\nDonnée erronée, veuillez entrer le point par son nombre correspondant\n")
            print("Extraire un sous-graphe")

        elif(choix == "D"):
            #Casse la boucle aussitôt que 'D' choisi
            break
        else:
            #Si l'usager rentre autre chose que A, B, C ou D
            print("Option invalide. Veuillez choisir une des options suivantes: \n")

    

if __name__ == "__main__":
    main()
