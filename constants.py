# constants.py



BOARD_ROWS = 3

BOARD_COLS = 10

BOARD_SIZE = 30



# إضافة هذا السطر الذي يسبب المشكلة

PIECES_PER_PLAYER = 7 



# البيوت الخاصة

HOUSE_OF_REBIRTH = 15      

HOUSE_OF_HAPPINESS = 26    

HOUSE_OF_WATER = 27        

HOUSE_OF_THREE_TRUTHS = 28 

HOUSE_OF_RE_ATOUM = 29     

HOUSE_OF_HORUS = 30        



WHITE = "W"

BLACK = "B"



# ألوان الطابع الخشبي والمصري

WHITE_COLOR = (235, 219, 178) # كريمي فاتح للقطع

BLACK_COLOR = (40, 40, 40)    # أسود رخامي للقطع

BOARD_COLOR = (139, 69, 19)   # بني خشبي للرقعة

TILE_COLOR = (210, 180, 140)  # لون الخانات (رملي)

TILE_ALT_COLOR = (193, 154, 107) # لون خانات متبادل

HIGHLIGHT_COLOR = (255, 215, 0, 120) # ذهبي شفاف للتحديد



CELL_SIZE = 90 

WINDOW_WIDTH = BOARD_COLS * CELL_SIZE + 40

WINDOW_HEIGHT = BOARD_ROWS * CELL_SIZE + 350