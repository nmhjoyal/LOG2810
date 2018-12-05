from automate import Automate
import sys



def main():

    try:
        automate = Automate("lexique6.txt")

        automate.findWords("abces")
        automate.findWords("abces")
        automate.findWords("abces")
        automate.findWords("abces")
        automate.findWords("abces")
        automate.findWords("abces")
        print(automate.findWords("abc"))

        print(automate.getLabel()[0])
        print(automate.getLabel()[1])

    except IOError:
        print("\nERREUR : Nom de fichier erroné")
    except ValueError:
        print("\nERREUR : Mot cherché n'existe pas dans ce lexique")
    except TypeError:
        print("\nERREUR : Mot de type inconnu")

if __name__ == "__main__":
    main()
