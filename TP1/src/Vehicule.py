from decimal import Decimal

# Classe Vehicule
#   type : correspond au type de vehicule médicalisé (NI-NH ou LI-ion)
#   batterie : représente le pourcentage de batterie du véhicule
#   tempsParcouru : le temps parcouru par le véhicule
#   consommationHoraire : la consommation de batterie par heure selon l'état
#                         du patient
class Vehicule:
    def __init__(self, typeAmbulance):
        self.type = typeAmbulance
        self.batterie = 100
        self.tempsParcouru = 0
        self.clscsVisites = []
        #Definit la consommation horaire dependamment du type de voiture
        #0 = NI-MH
        if(self.type==0):
            self.consommationHoraire=[20,12,48]
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
            print("\n")
            print("/------AFFICHAGE DES INFORMATIONS PLUS COURT CHEMIN------/")
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
            print("/----FIN AFFICHAGE DES INFORMATIONS PLUS COURT CHEMIN----/")
            print("\n")

    # Fonction qui parcours une 'distance' (temps) sans-recharge
    # Retourne vrai ou faux si le véhicule est capable de parcourir ce temps sans
    # recharge
    def parcourirCheminSansRecharge(self, temps, categoriePatient):
        consommationParMinute = self.consommationHoraire[categoriePatient]/60
        self.batterie -= round(Decimal(temps*consommationParMinute),2)

        # On réinitialise la batterie pour faciliter l'utilisation de la fonction
        if self.batterie > 20:
            self.tempsParcouru = temps
            self.batterie = 100
            return True
        else:
            self.batterie = 100
            return False
