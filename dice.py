"""
تمثيل رمية العصّي في لعبة Senet
أربع عصي لكل منها وجه فاتح (1) وداكن (0)
"""

import random

class Dice:
    @staticmethod
    def roll():
        """
        تنفيذ رمية واحدة للعصي
        في حال كان المجموع 0 تُحسب 5
        """
        sticks = [random.choice([0, 1]) for _ in range(4)]
        total = sum(sticks)
        return 5 if total == 0 else total

    @staticmethod
    def probabilities():
        """
        الاحتمالات الرياضية لنتائج رمية العصّي
        محسوبة من جميع الحالات الممكنة (2^4 = 16)
        """
        return {
            1: 4 / 16,
            2: 6 / 16,
            3: 4 / 16,
            4: 1 / 16,
            5: 1 / 16
        }
