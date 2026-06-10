from book import Book
from student import Student

class Rental:
    def __init__(self,book:Book,borrower:Student,days_rented: int=30):
        self.book =book
        self.borrower = borrower
        self.days_rented = days_rented

    def get_book(self):
        return self.book

    def get_days_rented(self):
        return self.days_rented

    def get_fine(self):
        fined_amount: float =0
        if self.get_days_rented() > 30:
            fined_amount += ((self.days_rented - 30)
                             * self.book.get_fine())
            fined_amount += self.book.base_fine()
        else:
            self.borrower.add_bonus(self.book.get_bonus())

        return fined_amount

    def __str__(self) -> str:
        return f"{self.book} 借阅了 {self.days_rented} 天."
