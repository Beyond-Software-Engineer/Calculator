from book import Book

class TextBook(Book):
    def __init__(self,title,price):
        super().__init__(title,price)

    def get_fine(self):
        return self.price * 0.001

    def base_fine(self) -> float:
        return 1

    def get_category(self):
        return "教材"

    def get_bonus(self):
        return 1

    def get_free_days(self):
        return 30