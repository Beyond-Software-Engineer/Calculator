import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from conftest import ai_test

from src.addition import Addition
from src.equation import Equation
from src.exercise import Exercise


@ai_test
def test_generate_addition_question():
    """测试：生成 100 以内加法题目"""
    exercise = Exercise(100)
    exercise.generate_addition_exercise(100)
    assert len(exercise.operations) > 0
    question = exercise.operations[0]
    assert "+" in question.as_string()

@ai_test
def test_calculate_correct_answer():
    """测试：计算加法答案正确"""
    test_equation1 :Equation = Addition(10,20)
    correct_answer = test_equation1.calculate_result()
    assert correct_answer == 30

@ai_test
@pytest.mark.parametrize("param1 , param2 , user_answer, expected", [
     (5,5, 10, True),
     (3,3, 6, True),
     (0,0, 0, True),
])
def test_check_user_answer(param1 , param2, user_answer, expected):
    """测试：校验用户输入答案"""
    test_equation :Equation = Addition(param1,param2)
    result = (test_equation.calculate_result() == user_answer)
    assert result == expected
