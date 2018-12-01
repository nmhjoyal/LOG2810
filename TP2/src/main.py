from automate import Automate
#from PyQt5.QtWidgets import *
#import interface as interface
#import sys


def main():

    try:
        automate = Automate("lexique6.txt")
        #automate.findWords("cas")
        automate.enter('c')
        automate.enter('a')
        automate.enter('s')
        automate.enter('e')
        automate.enter('r')
        automate.enter(' ')

        automate.enter('c')
        automate.enter('a')
        automate.enter('s')
        automate.enter(' ')


        print(automate.getFiveLast())
    except IOError:
        print("\nERREUR : Nom de fichier erroné")
    except ValueError:
        print("\nERREUR : Mot cherché n'existe pas dans ce lexique")
    except TypeError:
        print("\nERREUR : Mot de type inconnu")

if __name__ == "__main__":
    main()