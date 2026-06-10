from typing import Optional
from book import Book
from textbook import TextBook
from reference import Reference
from newbook import NewBook


class Student:
    def __init__(self, name: str, bonus: int = 0):
        from rental import Rental
        self.name = name
        self.bonus = bonus
        self.rentals: list[Optional[Rental]] = []

    def add_book(self,book:Book,days_rented:int):
        from rental import Rental
        rental:Rental = Rental(book,self,days_rented)
        self.rentals.append(rental)

    def add_bonus(self, bonus):
        self.bonus += bonus

    def get_bonus(self):
        return self.bonus

    def returned_message(self):
        total_amount: float = 0
        fined_amount: float =0
        bonus = 0
        message = ''
        for rental in self.rentals:
            fined_amount =rental.get_fine()
            total_amount += fined_amount
            while self.get_bonus() >= 7 and total_amount > 1:
                self.add_bonus(-7)
                total_amount -= 1

            message += f"{rental}\n"

        message += f"缴纳罚金:{total_amount:.2f} 元.\n"
        message += f"还书奖励:{self.get_bonus()}点.\n"

        return message


if __name__ == '__main__':
    # 以下完全对应Java的main方法逻辑
    student = Student("zhangsan")

    aBook: Book = TextBook("Python 进阶", 35.5)
    student.add_book(aBook, 12)

    aBook = TextBook("Java 导论", 37.5)   # 第三个参数为1（教材）
    student.add_book(aBook, 45)

    aBook = Reference("C#秘笈", 41.7)     # 第三个参数为3（参考书）
    student.add_book(aBook, 38)

    aBook = NewBook("软件构造", 29.8)    # 第三个参数为3
    student.add_book(aBook, 28)

    print(student.returned_message())


