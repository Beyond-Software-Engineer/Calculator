from typing import Optional
from book import Book


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

    def returned_message(self) -> str:

        total_amount: float = 0
        fined_amount: float = 0
        bonus: int = 0
        message: str = ''
        for rental in self.rentals:
            bonus = 0
            fined_amount: float = 0
            match rental.get_book().get_category():
                case Book.TEXT_BOOK:
                    if rental.get_days_rented() > 30:
                        fined_amount += ((rental.get_days_rented() - 30)
                                         * rental.get_book().get_price() * 0.001)
                        fined_amount += 1
                    else:
                        bonus = 1

                case Book.REFERENCE:
                    if rental.get_days_rented() > 30:
                        fined_amount += ((rental.get_days_rented() - 30)
                                         * rental.get_book().get_price() * 0.005)
                        fined_amount += 1.5
                    else:
                        bonus = 2

                case Book.NEW_BOOK:
                    if rental.get_days_rented() > 30:
                        fined_amount += ((rental.get_days_rented() - 30)
                                         * rental.get_book().get_price() * 0.01)
                        fined_amount += 3
                    else:
                        bonus = 3

                case _:
                    pass

            self.add_bonus(bonus)
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

    aBook = Book("Python 进阶", 35.5)
    student.add_book(aBook, 12)

    aBook = Book("Java 导论", 37.5, Book.TEXT_BOOK)   # 第三个参数为1（教材）
    student.add_book(aBook, 45)

    aBook = Book("C#秘笈", 41.7, Book.REFERENCE)     # 第三个参数为3（参考书）
    student.add_book(aBook, 38)

    aBook = Book("软件构造", 29.8, Book.REFERENCE)    # 第三个参数为3
    student.add_book(aBook, 28)

    print(student.returned_message())


