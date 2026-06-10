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
