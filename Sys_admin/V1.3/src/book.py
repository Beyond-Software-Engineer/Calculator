from abc import ABC, abstractmethod


class Book(ABC):
    def __init__(self,title,price):
        self.title = title
        self.price = price

    @abstractmethod
    def get_fine(self):
        pass

    @abstractmethod
    def base_fine(self):
        pass

    @abstractmethod
    def get_bonus(self):
        pass

    @abstractmethod
    def get_category(self):
        pass

    def get_price(self):
        return self.price


    def __str__(self):
        return f"{self.get_category()} 《{self.title}》"