"""习题模块 - 习题生成和管理"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from exercise.exercise import Exercise
from exercise.exercise_collection import ExerciseCollection

__all__ = ['Exercise', 'ExerciseCollection']