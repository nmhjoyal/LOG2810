class Vehicule:
    def __init__(self, typeAmbulance):
        self.type = typeAmbulance
        self.batterie = 100
        self.tempsParcouru = 0
        self.consommationHoraire = []

        #Definit la consommation horaire dependamment du type
        #0 = NI-MH
        if(self.type==0):
            self.consommationHoraire=[6,12,48]
        #1 = LI-Ion
        else:
            self.consommationHoraire=[5, 10, 30]

    def parcourirChemin(self, etiquetteSommet, categoriePatient):
        consommationParMinute = self.consommationHoraire[categoriePatient]/60

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

            return True


    def parcourirCheminSansRecharge(self, etiquetteSommet, categoriePatient):
        consommationParMinute = self.consommationHoraire[categoriePatient]/60

        self.batterie -= etiquetteSommet*consommationParMinute

        if self.batterie > 20:
            self.tempsParcouru = etiquetteSommet
            self.batterie = 100
            return True
        else:
            self.batterie = 100
            return False