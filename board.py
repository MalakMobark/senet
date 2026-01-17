"""
تمثيل رقعة لعبة Senet وتطبيق قواعد البيوت الخاصة
"""

from constants import (
    BOARD_SIZE,
    HOUSE_OF_REBIRTH,
    HOUSE_OF_HAPPINESS,
    HOUSE_OF_WATER,
    HOUSE_OF_THREE_TRUTHS,
    HOUSE_OF_RE_ATOUM,
    HOUSE_OF_HORUS
)

class Board:
    def __init__(self):
        """
        اللوح يمثَّل بقاموس: position -> piece ("W" أو "B") أو None
        """
        self.cells = {i: None for i in range(1, BOARD_SIZE + 1)}

    def is_occupied(self, position):
        return self.cells.get(position) is not None

    def get_piece(self, position):
        return self.cells.get(position)

    def place_piece(self, position, piece):
        self.cells[position] = piece

    def remove_piece(self, position):
        self.cells[position] = None

    def move_piece(self, from_pos, to_pos):
        piece = self.cells[from_pos]
        self.cells[from_pos] = None
        self.cells[to_pos] = piece

    # ------------------ قواعد البيوت الخاصة ------------------

    def apply_special_house(self, position):
        """
        يعيد الموقع الجديد بعد تطبيق قواعد البيوت الخاصة
        ملاحظة: بيت الماء (27) يُعالج في Game وليس هنا
        """
        # لا نعالج بيت الماء هنا - يُعالج في Game
        # البيوت 28، 29، 30 يتم التحقق منها في منطق الخروج
        return position

    def must_pass_happiness(self, from_pos, to_pos):
        """
        يمنع القفز فوق بيت السعادة (26)
        """
        return from_pos < HOUSE_OF_HAPPINESS < to_pos

    # ------------------ طباعة اللوح ------------------

    def print_board(self):
        def cell(i):
            return self.cells[i] if self.cells[i] else '.'

        row1 = [cell(i) for i in range(10, 0, -1)]
        row2 = [cell(i) for i in range(11, 21)]
        row3 = [cell(i) for i in range(30, 20, -1)]

        print(" ".join(row1))
        print(" ".join(row2))
        print(" ".join(row3))
