# length-utils
# made by ezd.li
# in cooperation with dcbot.dev
#
# German
#
#      _          _               _             _                
#   __| |   ___  | |__     ___   | |_        __| |   ___  __   __
#  / _` |  / __| | '_ \   / _ \  | __|      / _` |  / _ \ \ \ / /
# | (_| | | (__  | |_) | | (_) | | |_   _  | (_| | |  __/  \ V / 
#  \__,_|  \___| |_.__/   \___/   \__| (_)  \__,_|  \___|   \_/  
#                                                                



class MinLength:
    def __init__(self, n):
        self.n = n

    def __ge__(self, other):
        """
        Ermöglicht den Vergleich, wenn das Objekt auf der rechten Seite steht.
        Beispiel: if password <= length.min(5):
        Hier wird intern len(password) <= 5 geprüft.
        """
        try:
            return len(other) <= self.n
        except TypeError:
            raise TypeError("Der übergebene Wert hat keine Länge.")

    def __le__(self, other):
        """
        Ermöglicht den Vergleich in umgekehrter Richtung.
        Beispiel: if password >= length.min(5):
        Hier wird intern len(password) >= 5 geprüft.
        """
        try:
            return len(other) >= self.n
        except TypeError:
            raise TypeError("Der übergebene Wert hat keine Länge.")

def min(n):
    """
    Gibt ein MinLength-Objekt zurück, mit dem man den Vergleich anhand der Länge durchführen kann.
    """
    return MinLength(n)
