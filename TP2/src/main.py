
def readFile(filename):
    f = open(filename, "r")
    lexicon = []

    for ligne in f:
        lexicon.append(list(ligne))

    f.close()

    return lexicon

def main():
    lexicon = readFile("lexique 1.txt")

    #for i in lexicon:
    print(lexicon[0])


if __name__ == "__main__":
    main()
