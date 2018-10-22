import array as arr
from enum import Enum

class Arrondissements(Enum):
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

#Fonction qui crée une matrice contenant les relation entre chaque CLSC 
#et la distance qui les sépare
def creerGraphe(nomfichier):
    
    f = open(nomfichier, "r")

    #Initialisation de value a 0 pour qu'elle existe a l'exterieur de la boucle
    value = 0

    #Arriver a la fin de la première partie en gardant la dernière valeur
    #Afin de connaître la grandeur du tableau a initialiser
    for ligne in f:
        if ligne != "\n":
            value = ligne.split(",")
            continue
        else:
            break
    
    length = int(value[0])

    #Initialisation de la matrice
    Matrice=[[0 for x in range(length)] for y in range(length)]

    #Iteration au travers de la deuxième partie et ajout a la matrice
    #des CLSCs et leur distance
    for ligne in f:
        noeuds = ligne.split(",")
        nd1 = int(noeuds[0])
        nd2 = int(noeuds[1])
        dist = int(noeuds[2])
        Matrice[nd1-1][nd2-1]=[nd2,dist]
        Matrice[nd2-1][nd1-1]=[nd1,dist]
        continue

    #for m in Matrice:
    #    print(m)
    #   continue

    return Matrice

def lireGraphe(Matrice):
    i=1
    k=1

    for m in Matrice:
        chaine=""
        chaine+="(" + Arrondissements(i).name.replace("_","-") + ", " + str(i) + ", ("
        for j in m:
            if j!=0:
                chaine+="(" + Arrondissements(j[0]).name.replace("_","-") + "," + str(j[1]) + "),"
                continue
            continue
        chaine = chaine[:-1]
        chaine+="))"
        print(chaine)
        i+=1
        continue


def main():
    Matrice = creerGraphe("centresLocaux.txt")
    lireGraphe(Matrice)

if __name__ == "__main__":
    main()





