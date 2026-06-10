"""100以内口算练习程序 - 主包"""

from .operation_base import OperationBase
from .equation import Equation
from .addition import Addition
from .subtraction import Subtraction
from .exercise import Exercise
from .exercise_collection import ExerciseCollection
from .practice import Practice
from .judgement import Judgement
from .console import MainMenu

__all__ = [
    'OperationBase',
    'Equation',
    'Addition',
    'Subtraction',
    'Exercise',
    'ExerciseCollection',
    'Practice',
    'Judgement',
    'MainMenu'
]

__version__ = '1.0.0'
__author__ = '100以内口算练习程序开发团队'