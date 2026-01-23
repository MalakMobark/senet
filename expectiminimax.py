import math
from constants import WHITE, BLACK, HOUSE_OF_WATER, HOUSE_OF_HAPPINESS, HOUSE_OF_REBIRTH
from move import Move
from dice import Dice


class Expectiminimax:
    def __init__(self, depth=2):
        """
        تهيئة الخوارزمية مع تحديد عمق البحث.
        """
        self.depth = depth
        # احتمالات نتائج رمي العصي في لعبة سينيت (2^4 = 16 حالة)
        self.probabilities = {1: 4/16, 2: 6/16, 3: 4/16, 4: 1/16, 5: 1/16}

    def get_best_move(self, state, roll):
        """
        الدالة الرئيسية التي تستدعيها اللعبة لاختيار أفضل حركة للكمبيوتر.
        """
        _, best_move_idx = self.decide(state, self.depth, True, roll)
        return best_move_idx

    def evaluate(self, state):
        """
        دالة تقييم الحالة
        """
        terminal = state.is_terminal()
        if terminal == "YOU LOSE":
            return 100000
        if terminal == "YOU WIN!":
            return -100000

        score = 0

        # مكافأة الخروج
        score += len(state.black_exited) * 20000
        score -= len(state.white_exited) * 20000

        # تقييم أحجار الكمبيوتر (BLACK)
        for pos in state.black_pieces:
            score += pos * 1000

            if pos == HOUSE_OF_HAPPINESS:
                score += 1000
            if pos == 28 or pos == 29:
                score += 1500

        # تقييم أحجار اللاعب (WHITE)
        for pos in state.white_pieces:
            score -= pos * 1000

        # منطق الهجوم
        for w_pos in state.white_pieces:
            is_protected = any(
                abs(w_pos - other_w) == 1
                for other_w in state.white_pieces
                if w_pos != other_w
            )
            if not is_protected:
                score += 500

        return score

    def decide(self, state, depth, is_maximizing, roll=None):
        """
        المحرك الرئيسي مع إضافة منطق الإجبار للحالات الخاصة
        """
        if depth == 0 or state.is_terminal():
            return self.evaluate(state), None

        # -------- Chance Node --------
        if roll is None:
            expected_value = 0
            for r, prob in self.probabilities.items():
                val, _ = self.decide(state, depth - 1, is_maximizing, r)
                expected_value += val * prob
            return expected_value, None

        # -------- Decision Node --------
        legal_moves = Move.legal_moves(state, roll)

        if not legal_moves:
            new_state = state.clone()
            new_state.switch_turn()
            val, _ = self.decide(new_state, depth - 1, not is_maximizing, None)
            return val, None
        


                # استبعاد حجر الخانة 26 إذا الرمية 1 أو 2 أو 3، بشرط وجود خيارات أخرى
        if roll in (1, 2, 3):
            current_pieces = state.black_pieces if state.turn == BLACK else state.white_pieces

            # كل الحركات التي ليست من الخانة 26
            non_26_moves = [
                move_idx for move_idx in legal_moves
                if current_pieces[move_idx] != 26
            ]

            # إذا في حركات بديلة، نلعب بها ونتجاهل حجر 26
            if non_26_moves:
                legal_moves = non_26_moves


        # =================================================
        # منطق الإجبار (Forced Moves) - يُنفذ قبل الخوارزمية
        # =================================================
        forced_moves = []
        # 1. إذا في حجر بالخانة 30، لازم يلعب فيه مشان يطلع (بأي رمية)
        for move_idx in legal_moves:
            current_pieces = state.black_pieces if state.turn == BLACK else state.white_pieces
            if current_pieces[move_idx] == 30:
                forced_moves.append(move_idx)

        # 2. إذا في حجر بالخانة 26 والرمية 5، لازم يلعب فيه مشان يطلع
        

        # 2. إذا في حجر بالخانة 26 والرمية 4 أو 5، لازم يلعب فيه (إجباري دائماً)
        if not forced_moves and roll in (4, 5):
            for move_idx in legal_moves:
                current_pieces = state.black_pieces if state.turn == BLACK else state.white_pieces
                if current_pieces[move_idx] == 26:
                    forced_moves.append(move_idx)

        if not forced_moves:
            current_pieces = state.black_pieces if state.turn == BLACK else state.white_pieces
            for move_idx in legal_moves:
                if current_pieces[move_idx] + roll == HOUSE_OF_HAPPINESS:
                    forced_moves.append(move_idx)


        # إذا تحقق أي من الشروط، نحصر الخيارات بالحركات الإجبارية فقط
        if forced_moves:
            legal_moves = forced_moves

        # استكمال الخوارزمية بشكل طبيعي (سواء بالحركات الإجبارية أو بكل الحركات إذا لم يتوفر الشرط)
        if is_maximizing:
            best_val = -math.inf
            best_move = None
            for move_idx in legal_moves:
                new_state = Move.apply(state, move_idx, roll)
                val, _ = self.decide(new_state, depth - 1, False, None)
                if val > best_val:
                    best_val = val
                    best_move = move_idx
            return best_val, best_move
        else:
            worst_val = math.inf
            for move_idx in legal_moves:
                new_state = Move.apply(state, move_idx, roll)
                val, _ = self.decide(new_state, depth - 1, True, None)
                if val < worst_val:
                    worst_val = val
            return worst_val, None