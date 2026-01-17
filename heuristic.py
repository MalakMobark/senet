"""
تابع التقييم (Heuristic Function) للعبة Senet
"""

from constants import (
    HOUSE_OF_REBIRTH,
    HOUSE_OF_HAPPINESS,
    HOUSE_OF_WATER,
    HOUSE_OF_THREE_TRUTHS,
    HOUSE_OF_RE_ATOUM,
    HOUSE_OF_HORUS,
    WHITE
)

class Heuristic:
    @staticmethod
    def evaluate(state, maximizing_player=WHITE):
        """
        تقييم الحالة من منظور اللاعب الأعظمي (الكمبيوتر)
        قيمة أكبر => حالة أفضل للكمبيوتر
        """
        def piece_score(position):
            # أولوية الخروج
            if position >= HOUSE_OF_THREE_TRUTHS:
                return 50 + position * 2
            # تقدم على اللوح
            return position

        def total_score(pieces):
            return sum(piece_score(p) for p in pieces)

        white_score = total_score(state.white_pieces)
        black_score = total_score(state.black_pieces)

        return white_score - black_score if maximizing_player == WHITE else black_score - white_score
