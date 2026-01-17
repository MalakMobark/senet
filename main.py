"""
نقطة تشغيل لعبة Senet
"""

from game import Game

if __name__ == '__main__':
    # يمكن تعديل العمق حسب الرغبة (كلما زاد العمق زادت قوة الذكاء)
    game = Game(depth=2)
    game.run()
