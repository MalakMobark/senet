"""
منطق اللعبة الرئيسي (Player vs Computer)
"""

import pygame
from state import GameState
from dice import Dice
from move import Move
from expectiminimax import Expectiminimax
from renderer import Renderer
from input_handler import InputHandler
from constants import WHITE, BLACK
from constants import WINDOW_WIDTH, WINDOW_HEIGHT


class Game:
    def __init__(self, depth=2):
        self.state = GameState()
        self.renderer = Renderer()
        self.ai = Expectiminimax(depth)
        self.roll = None
        self.current_roll = None
        self.legal_moves = []
        self.can_move = False
        self.running = True

    # -------------------------------------------------
    # دالة مساعدة لإيجاد أقرب خانة فارغة قبل 15
    # -------------------------------------------------
    def find_nearest_empty_before_15(self, pieces_list):
        """
        إيجاد أقرب خانة فارغة ≤ 15 لوضع حجر عائد من بيوت خاصة
        pieces_list: قائمة الأحجار الخاصة باللاعب
        ترجع: رقم الخانة الفارغة أو None إذا كانت كل الخانات مشغولة
        """
        # الحصول على جميع الأحجار في اللعب (كلا اللاعبين)
        all_pieces = set(self.state.white_pieces + self.state.black_pieces)
        
        # البحث من الخلف (15 → 1)
        for pos in range(15, 0, -1):
            # التحقق إذا الخانة فارغة تماماً
            if pos not in all_pieces:
                return pos
        return None  # حالة نادرة جداً: كل الخانات ممتلئة

    # -------------------------------------------------
    # رمي العصّي
    # -------------------------------------------------
    def roll_dice(self):
        if self.can_move:
            return

        self.renderer.is_shaking = True
        
        # حلقة الحركة (20 إطار لفتلة أنعم وأطول شوي)
        for frame in range(20):
            self.renderer.draw_board()
            self.renderer.draw_score_boxes(self.state)
            self.renderer.draw_pieces(self.state)
            self.renderer.draw_toss_button()
            
            # نمرر frame للريندرر عشان يحسب زاوية الدوران
            self.renderer.draw_info("Rolling...", current_roll=3, anim_frame=frame)
            
            self.renderer.update()
            pygame.time.delay(30) # سرعة الفتل
            
        self.renderer.is_shaking = False
        self.current_roll = Dice.roll()
        self.legal_moves = Move.legal_moves(self.state, self.current_roll)
        self.can_move = True

        if not self.legal_moves:
            self.apply_penalty_houses(self.state.turn)
            self.can_move = False
            self.state.switch_turn()

    # -------------------------------------------------
    # عقوبة البيوت 28 و 29
    # -------------------------------------------------
    def apply_penalty_houses(self, player):
        pieces = (
            self.state.white_pieces if player == WHITE
            else self.state.black_pieces
        )

        for i, pos in enumerate(pieces):

            # بيت الماء 27 → رجوع إجباري
            if pos == 27:
                nearest = self.find_nearest_empty_before_15(pieces)
                if nearest is not None:
                    pieces[i] = nearest

            # بيت 28 → لازم 3
            elif pos == 28 and self.current_roll != 3:
                nearest = self.find_nearest_empty_before_15(pieces)
                if nearest is not None:
                    pieces[i] = nearest

            # بيت 29 → لازم 2
            elif pos == 29 and self.current_roll != 2:
                nearest = self.find_nearest_empty_before_15(pieces)
                if nearest is not None:
                    pieces[i] = nearest

    # -------------------------------------------------
    # دور اللاعب (الأبيض)
    # -------------------------------------------------
    def handle_player_turn(self, event):
        if event.type != pygame.MOUSEBUTTONDOWN:
            return

        # زر Toss
        if self.renderer.toss_rect and self.renderer.toss_rect.collidepoint(event.pos):
            self.roll_dice()
            # تطبيق عقوبات 28 و 29 بعد الرمي
            return

        if not self.can_move:
            return

        row, col = InputHandler.get_clicked_cell(event.pos)
        position = InputHandler.cell_to_position(row, col)
        if position is None:
            return

        pieces = self.state.white_pieces
        if position not in pieces:
            return

        idx = pieces.index(position)
        if idx not in self.legal_moves:
            return

        # حفظ مواقع الأحجار قبل الحركة
        original_positions = self.state.white_pieces[:]
        had_piece_on_30 = 30 in original_positions
        idx_30 = original_positions.index(30) if had_piece_on_30 else None
        # تنفيذ الحركة
        self.state = Move.apply(self.state, idx, self.current_roll)
        # إذا كان هناك حجر على 28 أو 29 ولم يتم اختياره → يرجع
        for i, pos in enumerate(original_positions):

            # حجر في 28 ولم يتم اختياره → يرجع
            if pos == 28 and idx != i:
                self.state.white_pieces[i] = self.find_nearest_empty_before_15(
                    self.state.white_pieces
                )

            # حجر في 29 ولم يتم اختياره → يرجع
            if pos == 29 and idx != i:
                self.state.white_pieces[i] = self.find_nearest_empty_before_15(
                    self.state.white_pieces
                )


        # تحقق من أي أحجار خرجت عن اللوح (>30)
        new_white_pieces = []
        for piece in self.state.white_pieces:
            if piece > 30:
                # أخرج الحجر وأضفه لقائمة exited
                self.state.white_exited.append(piece)
            else:
                new_white_pieces.append(piece)
        self.state.white_pieces = new_white_pieces

        
        # بعد الحركة: أي حجر كان في 30 ولم يتحرك → نعيده للـ 15
        if had_piece_on_30:
            if idx == idx_30:
                # اللاعب اختار حجر 30 → خروج
                self.state.white_exited.append(30)
                self.state.white_pieces.pop(idx_30)
            else:
                # اللاعب حرّك حجر آخر → حجر 30 يعود للـ 15
                nearest = self.find_nearest_empty_before_15(self.state.white_pieces)
                if nearest is not None:
                    self.state.white_pieces[idx_30] = nearest

        # إنهاء الدور
        self.can_move = False
        self.state.switch_turn()

        print("=== AFTER PLAYER MOVE ===")
        print("TURN:", self.state.turn)
        print("WHITE PIECES:", sorted(self.state.white_pieces))
        print("BLACK PIECES:", sorted(self.state.black_pieces))
        print("=========================")

    # -------------------------------------------------
    # دور الكمبيوتر (الأسود)
    # -------------------------------------------------
    def handle_ai_turn(self):
        # 1. إذا لم يرمِ بعد
        if not self.can_move:
            self.roll_dice()
            return

        # 2. لا يوجد حركات قانونية
        if not self.legal_moves:
            self.can_move = False
            self.state.switch_turn()
            return

        # 3. استدعاء خوارزمية Expectiminimax (التعديل هنا)
        # نستخدم get_best_move للحصول على مؤشر الحجر الأفضل
        move = self.ai.get_best_move(self.state, self.current_roll)

        if move is None:
            self.can_move = False
            self.state.switch_turn()
            return

        # --- الحفاظ على منطقك الخاص كما هو دون تغيير ---
        original_positions = self.state.black_pieces[:]
        had_piece_on_30 = 30 in original_positions
        idx_30 = original_positions.index(30) if had_piece_on_30 else None
        
        # تنفيذ حركة الكمبيوتر
        self.state = Move.apply(self.state, move, self.current_roll)
        
        for i, pos in enumerate(original_positions):
            # حجر في 28 ولم يتم اختياره → يرجع
            if pos == 28 and i != move:
                self.state.black_pieces[i] = self.find_nearest_empty_before_15(
                    self.state.black_pieces
                )

            # حجر في 29 ولم يتم اختياره → يرجع
            if pos == 29 and i != move:
                self.state.black_pieces[i] = self.find_nearest_empty_before_15(
                    self.state.black_pieces
                )

        # تحقق من أي أحجار خرجت عن اللوح (>30)
        new_black_pieces = []
        for piece in self.state.black_pieces:
            if piece > 30:
                self.state.black_exited.append(piece)
            else:
                new_black_pieces.append(piece)
        self.state.black_pieces = new_black_pieces

        # بعد الحركة: أي حجر كان في 30 ولم يتحرك → نعيده للـ 15
        if had_piece_on_30:
            if move == idx_30:
                # الـ AI اختار حجر 30 → خروج
                self.state.black_exited.append(30)
                # التأكد من إزالته من القائمة النشطة إذا لم يُزال بعد
                if 30 in self.state.black_pieces:
                    self.state.black_pieces.remove(30)
            else:
                # الـ AI حرّك حجر آخر → حجر 30 يعود للـ 15
                nearest = self.find_nearest_empty_before_15(self.state.black_pieces)
                if nearest is not None:
                    # نحدث موقعه في القائمة الجديدة
                    for i, p in enumerate(self.state.black_pieces):
                        if p == 30:
                            self.state.black_pieces[i] = nearest
                            break

        # إنهاء الدور
        self.can_move = False
        self.state.switch_turn()

        print("=== AFTER AI MOVE (Expectiminimax) ===")
        print("TURN:", self.state.turn)
        print("WHITE PIECES:", sorted(self.state.white_pieces))
        print("BLACK PIECES:", sorted(self.state.black_pieces))
        print("=====================")

    # -------------------------------------------------
    # الحلقة الرئيسية
    # -------------------------------------------------
    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if self.state.turn == WHITE:
                    self.handle_player_turn(event)

            if self.state.turn == BLACK:
                self.handle_ai_turn()
                pygame.time.delay(400)

            
            self.renderer.draw_board()
            self.renderer.draw_score_boxes(self.state) # رسم عدادات الخروج
            self.renderer.draw_pieces(self.state)

            if self.can_move:
                self.renderer.highlight_moves(self.state, self.legal_moves)

            self.renderer.draw_toss_button()
            self.renderer.draw_info(
                f"Turn: {self.state.turn}", 
                current_roll=self.current_roll
            )
# ------------------- تحقق من نهاية اللعبة -------------------
            result = self.state.is_terminal()
            if result:
                # عرض الرسالة في وسط الشاشة
                font = pygame.font.SysFont(None, 72)
                text = font.render(result, True, (255, 0, 0))
                rect = text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
                self.renderer.screen.blit(text, rect)
                self.renderer.update()
                pygame.time.delay(3000)  # عرض الرسالة 3 ثواني
                self.running = False
                continue

            self.renderer.update()
            clock.tick(30)

        self.renderer.quit()
