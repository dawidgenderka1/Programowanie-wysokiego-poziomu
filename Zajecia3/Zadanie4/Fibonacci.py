from typing import Iterator

def fibonacci(n: int) -> Iterator[int]:
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

for liczba in fibonacci(12):
    print(liczba)
