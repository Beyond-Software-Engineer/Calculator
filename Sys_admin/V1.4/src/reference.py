from book import Book

class Reference(Book):
    def __init__(self,title,price):
        super().__init__(title,price)

    def get_fine(self):
        return self.price * 0.005

    def base_fine(self) -> float:
        return 1.5

    def get_category(self):
        return "参考书"

    def get_bonus(self):
        return 2

    def get_free_days(self):
        return 15