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

    def calculate_fine_and_bonus(self):
        fined_amount: float =0
        match self.book.get_category():
            case Book.TEXT_BOOK:
                if self.get_days_rented() > 30:
                    fined_amount += ((self.days_rented - 30)
                                     * self.book.get_price() * 0.001)
                    fined_amount += 1
                else:
                    self.borrower.add_bonus(1)

            case Book.REFERENCE:
                if self.get_days_rented() > 30:
                    fined_amount += ((self.days_rented - 30)
                                     * self.book.get_price() * 0.005)
                    fined_amount += 1.5
                else:
                    self.borrower.add_bonus(1)

            case Book.NEW_BOOK:
                if self.get_days_rented() > 30:
                    fined_amount += ((self.days_rented - 30)
                                     * self.book.get_price() * 0.01)
                    fined_amount += 3
                else:
                    self.borrower.add_bonus(1)

            case _:
                pass

        return fined_amount

    def __str__(self) -> str:
        match self.book.get_category():
            case Book.TEXT_BOOK:
                type = "教材"
            case Book.REFERENCE:
                type = "参考书"
            case Book.NEW_BOOK:
                type = "新书"
            case _:
                type = "未知类型"

        return f"{type}{self.book} 借阅了 {self.days_rented} 天."
