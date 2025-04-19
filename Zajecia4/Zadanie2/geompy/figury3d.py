import math

def objetosc_szescianu(bok: float) -> float:
    return bok ** 3

def pole_szescianu(bok: float) -> float:
    return 6 * bok ** 2

def objetosc_prostopadloscianu(a: float, b: float, h: float) -> float:
    return a * b * h

def pole_prostopadloscianu(a: float, b: float, h: float) -> float:
    return 2 * (a * b + a * h + b * h)

def objetosc_kuli(promien: float) -> float:
    return (4 / 3) * math.pi * promien ** 3

def pole_kuli(promien: float) -> float:
    return 4 * math.pi * promien ** 2
