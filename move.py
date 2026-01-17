"""
تابع الانتقال (Transition Function) في لعبة Senet - مصحح 28/29
"""

from constants import (
    BOARD_SIZE,
    HOUSE_OF_REBIRTH,
    HOUSE_OF_HAPPINESS,
    HOUSE_OF_WATER,
    HOUSE_OF_THREE_TRUTHS,  # 28
    HOUSE_OF_RE_ATOUM,      # 29
    HOUSE_OF_HORUS,
    WHITE
)


class Move:

    @staticmethod
    @staticmethod
    def legal_moves(state, roll):
        """
        إرجاع جميع الحركات القانونية حسب الرمية الحالية
        """
        moves = []
        my_pieces = state.current_pieces()
        opp_pieces = state.opponent_pieces()

        for idx, pos in enumerate(my_pieces):
            target = pos + roll

            # 1. بيت 30: الخروج مسموح دائماً (حسب منطقك في game.py)
            if pos == HOUSE_OF_HORUS:
                moves.append(idx)
                continue

            # 2. بيت 28: يحتاج رمية 3 حصراً للخروج
            if pos == HOUSE_OF_THREE_TRUTHS:
                if roll == 3:
                    moves.append(idx)
                continue

            # 3. بيت 29: يحتاج رمية 2 حصراً للخروج
            if pos == HOUSE_OF_RE_ATOUM:
                if roll == 2:
                    moves.append(idx)
                continue

            # 4. التعديل الهام: بيت السعادة (26)
            # السماح بالخروج إذا كانت الرمية 5 (target = 31)
            if pos == HOUSE_OF_HAPPINESS and roll == 5:
                moves.append(idx)
                continue

            # 5. منع تجاوز اللوح للحركات العادية الأخرى
            if target > 30:
                continue

            # 6. الشروط العادية (عدم التصادم مع أحجارك والقفز فوق 26)
            if target in my_pieces:
                continue

            if state.board.must_pass_happiness(pos, target):
                continue

            # حركة عادية قانونية
            moves.append(idx)

        return moves
        
    @staticmethod
    def apply(state, piece_index, roll):
        new_state = state.clone()

        if new_state.turn == WHITE:
            my_pieces = new_state.white_pieces
            opp_pieces = new_state.black_pieces
            exited_pieces = new_state.white_exited  # الأحجار الخارجة
        else:
            my_pieces = new_state.black_pieces
            opp_pieces = new_state.white_pieces
            exited_pieces = new_state.black_exited  # الأحجار الخارجة

        pos = my_pieces[piece_index]

        # ✅ بيت 28: شروط خاصة
        if pos == HOUSE_OF_THREE_TRUTHS:
            if roll == 3:
                # الخيار 1: إخراج الحجر (يمكن تنفيذه كحركة عادية)
                # الخيار 2: إرجاع للـ 15 (يتم التعامل معه في game.py)
                pass  # نسمح بالحركة لتكون خياراً للمستخدم
            else:
                # إجباري: إرجاع للـ 15
                my_pieces[piece_index] = HOUSE_OF_REBIRTH
                return new_state

        # ✅ بيت 29: شروط خاصة ( lazem 2 )
        if pos == HOUSE_OF_RE_ATOUM:
            if roll == 2:
                # الخيار 1: إخراج الحجر
                # الخيار 2: إرجاع للـ 15 (يتم التعامل معه في game.py)
                pass  # نسمح بالحركة لتكون خياراً للمستخدم
            else:
                # إجباري: إرجاع للـ 15
                my_pieces[piece_index] = HOUSE_OF_REBIRTH
                return new_state

        target = pos + roll
        # بيت الماء 27 → رجوع فوري
        if target == HOUSE_OF_WATER:
            pieces = new_state.white_pieces + new_state.black_pieces
            for back in range(15, 0, -1):
                if back not in pieces:
                    my_pieces[piece_index] = back
                    return new_state


        if pos == HOUSE_OF_HORUS:
            # لا نفعل شيئاً هنا
            # القرار (خروج أو عودة) يتم في game.py
            return new_state



                # تبادل
        if target in opp_pieces:
            opp_idx = opp_pieces.index(target)
            opp_pieces[opp_idx] = pos

        my_pieces[piece_index] = target

        # ✅ رجوع مضمون
        return new_state
