class Book:
    TEXT_BOOK = 1
    REFERENCE = 3
    NEW_BOOK = 5
    def __init__(self,title,price,category:int = 0):
        self.title = title
        self.price = price
        self.category = category

    def get_category(self):
        return self.category

    def get_price(self):
        return self.price

    def __str__(self):
        return f"{self.title}"