import pygame
import math
from constants import *
import random

class Renderer:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Senet - Ancient Egyptian Game")
        self.font = pygame.font.SysFont("Arial", 22, bold=True)
        self.title_font = pygame.font.SysFont("Times New Roman", 45, bold=True)
        self.toss_rect = None
        self.is_shaking = False

    def cell_to_position(self, row, col):
        if row == 0: return col + 1
        elif row == 1: return 20 - col
        elif row == 2: return 21 + col
        return None

    def _position_to_cell(self, pos):
        if 1 <= pos <= 10: return 0, pos - 1
        elif 11 <= pos <= 20: return 1, 20 - pos
        elif 21 <= pos <= 30: return 2, pos - 21
        return 0, 0

    def draw_board(self):
        self.screen.fill((54, 32, 20)) 
        title = self.title_font.render("SENET", True, (218, 165, 32))
        self.screen.blit(title, (WINDOW_WIDTH//2 - 70, 10))

        offset_y = 120 
        offset_x = 20

        for r in range(BOARD_ROWS):
            for c in range(BOARD_COLS):
                x = c * CELL_SIZE + offset_x
                y = r * CELL_SIZE + offset_y
                pos = self.cell_to_position(r, c)
                color = TILE_COLOR if (r + c) % 2 == 0 else TILE_ALT_COLOR
                pygame.draw.rect(self.screen, color, (x, y, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(self.screen, (80, 50, 20), (x, y, CELL_SIZE, CELL_SIZE), 2)
                self._draw_special_symbols(self.screen, pos, x, y)

    def _draw_special_symbols(self, surface, pos, x, y):
        center = (x + CELL_SIZE // 2, y + CELL_SIZE // 2)
        s = CELL_SIZE // 4
        gold = (184, 134, 11)
        if pos == 15: 
            pygame.draw.circle(surface, gold, (center[0], center[1]-s), s//2, 2)
            pygame.draw.line(surface, gold, (center[0], center[1]-s//2), (center[0], center[1]+s), 2)
            pygame.draw.line(surface, gold, (center[0]-s, center[1]), (center[0]+s, center[1]), 2)
        elif pos == 26: 
            pygame.draw.circle(surface, (200, 0, 0), center, s//1.5)
            for i in range(12):
                angle = i * (math.pi/6)
                ex, ey = center[0] + math.cos(angle)*s*1.6, center[1] + math.sin(angle)*s*1.6
                pygame.draw.line(surface, gold, center, (int(ex), int(ey)), 2)
        elif pos == 27: 
            for i in range(3):
                yw = y + 30 + i*15
                pygame.draw.lines(surface, (0, 105, 148), False, [(x+15, yw), (x+45, yw-10), (x+75, yw)], 3)
        elif pos == 28: 
            for i in range(3):
                lx = x + 30 + i*15
                pygame.draw.line(surface, gold, (lx, y+20), (lx, y+70), 3)
                pygame.draw.circle(surface, gold, (lx, y+20), 4)
        elif pos == 29: 
            for i in range(2):
                px = x + 35 + i*25
                pygame.draw.circle(surface, gold, (px, y+35), 7)
                pygame.draw.line(surface, gold, (px, y+42), (px, y+65), 3)
        elif pos == 30: 
            pygame.draw.ellipse(surface, (0,0,0), (x+15, y+30, 60, 30), 2)
            pygame.draw.circle(surface, (139, 69, 19), center, 8)

    def draw_score_boxes(self, state):
        # المربعات العلوية - وضعناها في أعلى الشاشة تماماً (Y=10)
        box_w, box_h = 180, 50
        
        # مربع اللاعب الأبيض (يسار)
        pygame.draw.rect(self.screen, (245, 222, 179), (20, 10, box_w, box_h), border_radius=10)
        pygame.draw.rect(self.screen, (218, 165, 32), (20, 10, box_w, box_h), 3, border_radius=10)
        w_txt = self.font.render(f"WHITE OUT: {len(state.white_exited)}", True, (0,0,0))
        self.screen.blit(w_txt, (35, 22))

        # مربع اللاعب الأسود (يمين)
        pygame.draw.rect(self.screen, (40, 40, 40), (WINDOW_WIDTH - 200, 10, box_w, box_h), border_radius=10)
        pygame.draw.rect(self.screen, (218, 165, 32), (WINDOW_WIDTH - 200, 10, box_w, box_h), 3, border_radius=10)
        b_txt = self.font.render(f"BLACK OUT: {len(state.black_exited)}", True, (255,255,255))
        self.screen.blit(b_txt, (WINDOW_WIDTH - 185, 22))

    def draw_pieces(self, state):
        offset_y, offset_x = 120, 20
        for pos in state.white_pieces:
            self._draw_circle_piece(pos, WHITE_COLOR, offset_x, offset_y)
        for pos in state.black_pieces:
            self._draw_circle_piece(pos, BLACK_COLOR, offset_x, offset_y)

    def _draw_circle_piece(self, pos, color, ox, oy):
        r, c = self._position_to_cell(pos)
        cx, cy = c*CELL_SIZE + ox + CELL_SIZE//2, r*CELL_SIZE + oy + CELL_SIZE//2
        radius = CELL_SIZE // 3
        pygame.draw.circle(self.screen, color, (cx, cy), radius)
        pygame.draw.circle(self.screen, (0,0,0), (cx, cy), radius, 2)

    def draw_info(self, text, current_roll=None, anim_frame=0):
        import math
        y_text = WINDOW_HEIGHT - 200
        txt_surf = self.font.render(text.upper(), True, (218, 165, 32))
        self.screen.blit(txt_surf, (WINDOW_WIDTH//2 - txt_surf.get_width()//2, y_text))

        if current_roll is not None:
            panel_x = WINDOW_WIDTH//2 - 100
            panel_y = y_text + 35
            pygame.draw.rect(self.screen, (80, 50, 20), (panel_x, panel_y, 200, 90), border_radius=10)
            
            num_light = 0 if current_roll == 5 else current_roll
            for i in range(4):
                stick_x = panel_x + 20 + i*45
                base_stick_y = panel_y + 10
                max_height = 70
                # --- منطق الفتلة الطولية ---
                if self.is_shaking:
                    # نستخدم دالة الكوساين لتغيير الطول من -70 لـ 70 (دوران)
                    # anim_frame بيخلي كل عصا تفتل بسرعة وتوقيت مختلف شوي
                    phase = anim_frame * 0.5 + i 
                    current_height = int(math.cos(phase) * max_height)
                    
                    # إذا الطول سالب يعني عم نشوف قفا العصا (لون داكن دائماً)
                    display_h = abs(current_height)
                    draw_y = base_stick_y + (max_height - display_h) // 2
                    color = (40, 20, 10) if current_height < 0 else (245, 222, 179)
                else:
                    # الوضع الثابت بعد الرمي
                    display_h = max_height
                    draw_y = base_stick_y
                    color = (245, 222, 179) if i < num_light else (40, 20, 10)

                # رسم العصا (تغيير الـ Height هو اللي بيعطي إيحاء الفتل)
                if display_h < 2: display_h = 2 # عشان ما تختفي تماماً
                pygame.draw.rect(self.screen, color, (stick_x, draw_y, 25, display_h), border_radius=5)
                pygame.draw.rect(self.screen, (0,0,0), (stick_x, draw_y, 25, display_h), 2, border_radius=5)
                
    def draw_toss_button(self):
        self.toss_rect = pygame.Rect(WINDOW_WIDTH//2 - 60, WINDOW_HEIGHT - 55, 120, 40)
        pygame.draw.rect(self.screen, (184, 134, 11), self.toss_rect, border_radius=8)
        btn_txt = self.font.render("TOSS", True, (255, 255, 255))
        self.screen.blit(btn_txt, (self.toss_rect.x + 32, self.toss_rect.y + 8))

    def highlight_moves(self, state, legal_moves_indices):
        my_pieces = state.white_pieces if state.turn == WHITE else state.black_pieces
        for idx in legal_moves_indices:
            pos = my_pieces[idx]
            r, c = self._position_to_cell(pos)
            x, y = c * CELL_SIZE + 20, r * CELL_SIZE + 120
            pygame.draw.rect(self.screen, (255, 215, 0), (x, y, CELL_SIZE, CELL_SIZE), 5)

    def update(self): pygame.display.flip()
    def quit(self): pygame.quit()