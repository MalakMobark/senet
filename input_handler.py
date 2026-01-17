from constants import CELL_SIZE

class InputHandler:
    @staticmethod
    def get_clicked_cell(mouse_pos):
        """
        تحويل موقع النقر إلى (row, col) مع مراعاة الإزاحة الجديدة
        """
        x, y = mouse_pos
        
        # هذه هي الإزاحات (offsets) التي وضعناها في ملف الـ renderer الجديد
        offset_x = 20
        offset_y = 100
        
        # خصم الإزاحة من موقع الماوس
        adjusted_x = x - offset_x
        adjusted_y = y - offset_y
        
        # التحقق إذا كانت النقرة خارج حدود الرقعة
        if adjusted_x < 0 or adjusted_y < 0:
            return None, None
            
        col = adjusted_x // CELL_SIZE
        row = adjusted_y // CELL_SIZE
        
        # التأكد أن الصف والعمود ضمن حدود المصفوفة (3x10)
        if 0 <= row < 3 and 0 <= col < 10:
            return int(row), int(col)
            
        return None, None

    @staticmethod
    def cell_to_position(row, col):
        if row is None or col is None:
            return None
        if row == 0:
            return col + 1
        elif row == 1:
            return 20 - col
        elif row == 2:
            return 21 + col
        return None