from enum import Enum

# Accents et leur numéro ASCII associé -97


class Accents(Enum):
    cCedille = 134  # ç
    eGrave = 135  # è
    eAigu = 136  # é
    eCirconflex = 137  # ê
    iCirconflex = 141  # î
    iTrema = 142  # ï
    oCirconflex = 147  # ô
    uGrave = 152  # ù
    uCirconflex = 154  # û


def charToIndice(char):
    switcher = {
        'ç': 27,
        'è': 28,
        'é': 29,
        'ê': 30,
        'î': 31,
        'ï': 32,
        'ô': 33,
        'ù': 34,
        'û': 35,
        "'": 36,
        'œ': 37,
        'æ': 38
    }
    return switcher.get(char)
