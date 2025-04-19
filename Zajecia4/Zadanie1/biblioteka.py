from typing import List


class Ksiazka:
    def __init__(self, tytul: str, autor: str, dostepna: bool = True):
        self.tytul = tytul
        self.autor = autor
        self.dostepna = dostepna

    def __repr__(self):
        return f"<Ksiazka: {self.tytul} - {self.autor}>"


class Biblioteka:
    def __init__(self):
        self.lista_ksiazek: List[Ksiazka] = []

    def dodaj_ksiazke(self, ksiazka: Ksiazka) -> None:
        self.lista_ksiazek.append(ksiazka)

    def wypozycz_ksiazke(self, tytul: str) -> str:
        for ksiazka in self.lista_ksiazek:
            if ksiazka.tytul == tytul:
                if ksiazka.dostepna:
                    ksiazka.dostepna = False
                    return f"Wypożyczono: {tytul}"
                return f"Książka {tytul} niedostępna"
        return f"Brak książki: {tytul}"

    def zwroc_ksiazke(self, tytul: str) -> str:
        for ksiazka in self.lista_ksiazek:
            if ksiazka.tytul == tytul:
                ksiazka.dostepna = True
                return f"Zwrócono: {tytul}"
        return f"Nie należy do biblioteki: {tytul}"

    def dostepne_ksiazki(self) -> List[str]:
        return [ksiazka.tytul for ksiazka in self.lista_ksiazek if ksiazka.dostepna]


def main() -> None:
    biblioteka = Biblioteka()
    biblioteka.dodaj_ksiazke(Ksiazka("Wiedźmin", "Sapkowski"))
    biblioteka.dodaj_ksiazke(Ksiazka("Solaris", "Lem"))
    biblioteka.dodaj_ksiazke(Ksiazka("Lalka", "Prus", False))

    print(biblioteka.wypozycz_ksiazke("Solaris"))
    print(biblioteka.wypozycz_ksiazke("Lalka"))
    print(biblioteka.zwroc_ksiazke("Lalka"))
    print("Dostępne książki:", biblioteka.dostepne_ksiazki())


if __name__ == "__main__":
    main()
