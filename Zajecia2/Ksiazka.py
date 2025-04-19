class Ksiazka:
    def __init__(self, tytul: str, autor: str, rok_wydania: int):
        self.tytul = tytul
        self.autor = autor
        self.rok_wydania = rok_wydania
    
    def opis(self):
        return self.tytul + " (" + self.autor + "), " + str(self.rok_wydania)

class Ebook(Ksiazka):
    def __init__(self, tytul: str, autor: str, rok_wydania: int, rozmiar_pliku: float):
        super().__init__(tytul, autor, rok_wydania)
        self.rozmiar_pliku = rozmiar_pliku
    
    def opis(self):
        return self.tytul + " (" + self.autor + "), " + str(self.rok_wydania) + " , " + str(self.rozmiar_pliku) + " MB"

class Audiobook(Ksiazka):
    def __init__(self, tytul: str, autor: str, rok_wydania: int, czas_trwania: int):
        super().__init__(tytul, autor, rok_wydania)
        self.czas_trwania = czas_trwania
    
    def opis(self):
        return self.tytul + " (" + self.autor + "), " + str(self.rok_wydania) + " , " + str(self.czas_trwania) + " minut"

ebook1 = Ebook("Python dla każdego", "John Smith", 2020, 5.3)
audiobook1 = Audiobook("Sztuka Programowania", "Donald Knuth", 2015, 720)

print(ebook1.opis())
print(audiobook1.opis())
