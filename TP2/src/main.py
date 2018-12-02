from automate import Automate
import sys



def main():

    try:
        automate = Automate("lexique6.txt")
        automate.findWords("cas")
        automate.findWords("cas")
        automate.findWords("cas")
        automate.findWords("cas")


        [timeused, isfivelast] = automate.getLabel()
        print(timeused)
        print(isfivelast)
        automate.getAllLabel("lexique6.txt")

    except IOError:
        print("\nERREUR : Nom de fichier erroné")
    except ValueError:
        print("\nERREUR : Mot cherché n'existe pas dans ce lexique")
    except TypeError:
        print("\nERREUR : Mot de type inconnu")

if __name__ == "__main__":
    main()
