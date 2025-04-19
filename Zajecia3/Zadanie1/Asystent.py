class Asystent:
    def __init__(self, nazwa, wersja):
        self.nazwa = nazwa
        self.wersja = wersja

class AnalizaJezykowa:
    def analizuj_zapytanie(self, zapytanie):
        zapytanie = zapytanie.lower()
        if "pogoda" in zapytanie:
            return {"intencja": "pogoda", "slowa_kluczowe": ["pogoda, temperatura"]}
        elif "czas" in zapytanie or "godzina" in zapytanie:
            return {"intencja": "czas", "slowa_kluczowe": ["czas", "godzina"]}
        else:
            return {"intencja": "inna", "slowa_kluczowe": []}

class GeneratorOdpowiedzi:
    def generuj_odpowiedz(self, analiza):
        intencja = analiza["intencja"]
        if intencja == "pogoda":
            return "Dzisiaj jest słonecznie (22°C)."
        elif intencja == "czas":
            from datetime import datetime
            return f"Aktualna godzina to {datetime.now().strftime('%H:%M')}."
        else:
            return "Przepraszam, nie rozumiem zapytania."

class InteligentnyAsystent:
    def __init__(self, nazwa, wersja):
        self.asystent = Asystent(nazwa, wersja)
        self.analizator = AnalizaJezykowa()
        self.generator = GeneratorOdpowiedzi()

    def odpowiedz_na_zapytanie(self, zapytanie):
        analiza = self.analizator.analizuj_zapytanie(zapytanie)
        odpowiedz = self.generator.generuj_odpowiedz(analiza)
        return odpowiedz

asystent = InteligentnyAsystent("Asystent", "1.0")

zapytania = [
    "Jaka jest dziś pogoda?",
    "Która godzina?",
    "Czy potrafisz tańczyć?"
]

for zapytanie in zapytania:
    print(f"Użytkownik: {zapytanie}")
    print(f"Asystent: {asystent.odpowiedz_na_zapytanie(zapytanie)}\n")
