from book import Book

class NewBook(Book):
    def __init__(self,title,price):
        super().__init__(title,price)

    def get_fine(self) -> float:
        return self.price * 0.01

    def base_fine(self) -> float:
        return 3

    def get_category(self):
        return "新书"

    def get_bonus(self):
        return 3

    def get_free_days(self):
        return 10