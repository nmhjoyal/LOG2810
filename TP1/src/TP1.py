import array as arr
from classes import Graphe

def main():

    g = Graphe("centresLocaux.txt")
    g.plusCourtChemin(22,27,2)

if __name__ == "__main__":
    main()
