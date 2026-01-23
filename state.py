"""
تمثيل حالة اللعبة (Game State) في Senet
"""

from constants import (
    WHITE, BLACK,
    PIECES_PER_PLAYER,
    HOUSE_OF_THREE_TRUTHS,
    HOUSE_OF_RE_ATOUM,
    HOUSE_OF_HORUS
)
from board import Board

class GameState:
    def __init__(self):
        self.board = Board()
        # اللاعب (أنت) = الأبيض        
        self.white_pieces = [2, 4, 6, 8, 10, 12, 14]

        # الكمبيوتر = الأسود
        # self.black_pieces = [1, 3, 5, 7, 9, 11, 13]
        self.black_pieces = [1, 3, 5, 7, 9, 11, 13]

        # الأحجار الخارجة من الرقعة
        self.white_exited = []  # الأحجار البيضاء الخارجة
        self.black_exited = []  # الأحجار السوداء الخارجة

        self.turn = WHITE  # الأبيض يبدأ
        self.roll = None

    def clone(self):
        new_state = GameState.__new__(GameState)
        new_state.board = self.board
        new_state.turn = self.turn
        new_state.white_pieces = self.white_pieces[:]
        new_state.black_pieces = self.black_pieces[:]
        new_state.white_exited = self.white_exited[:]  # نسخ الأحجار الخارجة
        new_state.black_exited = self.black_exited[:]
        return new_state

    def switch_turn(self):


        # تبديل الدور
        self.turn = BLACK if self.turn == WHITE else WHITE

    def current_pieces(self):
        return self.white_pieces if self.turn == WHITE else self.black_pieces

    def opponent_pieces(self):
        return self.black_pieces if self.turn == WHITE else self.white_pieces

    def is_terminal(self):
        if len(self.white_pieces) == 0:
            return "YOU WIN!"
        elif len(self.black_pieces) == 0:
            return "YOU LOSE"
        return False

    def can_exit_piece(self, position, roll):
        """
        شروط الخروج من البيوت 28، 29
        بيت 30: لا يحتاج شرط خاص (الخروج اختياري)
        """
        if position == HOUSE_OF_THREE_TRUTHS:
            return roll == 3
        if position == HOUSE_OF_RE_ATOUM:
            return roll == 2
        # بيت 30: لا شرط مطلوب (دائمًا يمكن الخروج أو العودة)
        return False  # هذا يجعل الخروج اختياريًا
