from Sys_admin.main.src.addition import Addition
from Sys_admin.main.src.equation import Equation
from Sys_admin.main.src.subtraction import Subtraction


def test_check_same_equation():
    test_equation1 :Equation = Addition(15,33,0,100)
    test_equation2 :Equation = Addition(15,33,0,100)
    test_equation3 :Equation = Addition(33,15,0,100)

    assert test_equation1.check_same_equation(test_equation2) == True ,"完全相同的等式被检查失败"
    assert test_equation1.check_same_equation(test_equation3) == True ,"交换左右操作数的等式被检查失败"

def test_check_restriction():
    test_restriction1 :Equation= Addition(105,15,0,100)
    test_restriction2 :Equation= Addition(-2,1,0,100)

    assert test_restriction1.check_restriction() == False ,"检查加法超出规定上限的约束失败"
    assert test_restriction2.check_restriction() == False,"检查加法超出规定下限的约束失败"

    test_restriction3 :Equation= Subtraction(105,4,0,100)
    test_restriction4 :Equation= Subtraction(-2,1,0,100)

    assert test_restriction3.check_restriction() == False ,"检查减法超出规定上限的约束失败"
    assert test_restriction4.check_restriction() == False,"检查减法超出规定下限的约束失败"

def test_calculate_result():
    test_calculate1 :Equation = Addition(70,30)
    test_calculate2 :Equation = Subtraction(100,1)
    test_calculate3 :Equation = Subtraction(100,0)

    assert test_calculate1.calculate_result() == 100 ,"等式的加法计算结果出错"
    assert test_calculate2.calculate_result() == 99 ,"等式的减法计算结果出错"
    assert test_calculate3.calculate_result() == 100 ,"等式的加法计算出错"
