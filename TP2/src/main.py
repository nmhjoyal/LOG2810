from automate import Automate


def main():
    try:
        automate = Automate("lexique6.txt")
        automate.findWords("cas")
    except IOError:
        print("\nERREUR : Nom de fichier erroné")
    except ValueError:
        print("\nERREUR : Mot cherché n'existe pas dans ce lexique")
    except TypeError:
        print("\nERREUR : Mot de type inconnu")

if __name__ == "__main__":
    main()