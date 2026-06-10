"""练习模块 - 练习和批改功能"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from practice.practice import Practice
from practice.judgement import Judgement

__all__ = ['Practice', 'Judgement']