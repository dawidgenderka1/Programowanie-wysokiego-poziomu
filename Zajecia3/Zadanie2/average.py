from typing import List

def average(numbers: List[float]) -> float:
    return sum(numbers) / len(numbers)

dane = [12.1, 4.98, 0.11, 9.0, 10.6, 12.91, 1.25]
srednia = average(dane)
print(f"Średnia: {srednia}")