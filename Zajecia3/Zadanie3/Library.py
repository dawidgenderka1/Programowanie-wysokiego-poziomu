from typing import Dict, Optional

class Library:
    def __init__(self):
        self.books: Dict[str, str] = {}

    def add_book(self, isbn: str, title: str) -> None:
        self.books[isbn] = title

    def find_book(self, isbn: str) -> Optional[str]:
        return self.books.get(isbn)

library = Library()
library.add_book("978-83-11-20301-0", "Kamienie na szaniec")
library.add_book("978-83-240-5679-9", "Dzieci z Bullerbyn")

print(library.find_book("978-83-11-20301-0"))
print(library.find_book("123-45-6789"))