from abc import abstractmethod

class Equation:
    def __init__(self,first_param = None,operator = None,second_param = None,restriction = None):
        self.first_param = first_param
        self.operator = operator
        self.second_param = second_param
        self.restriction = restriction

    @abstractmethod
    def calculate_result(self):
        pass

    @abstractmethod
    def check_restriction(self):
        pass

    @abstractmethod
    def generate_equation(self,restriction):
        pass

    def output_equation(self):
        return f"{self.first_param} {self.operator} {self.second_param} = "

    def check_same_equation(self,equation):
        if self.operator != equation.operator:
            return False
        else:
            if self.first_param == equation.first_param :
                if self.second_param == equation.second_param:
                    return True
                else:
                    return False
            elif self.first_param == equation.second_param:
                if self.second_param == equation.first_param:
                    return True
                else:
                    return False
        return False




