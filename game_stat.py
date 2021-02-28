
class GameStats():
    """Отслеживание статистики для игры"""

    def __init__(self,setting):
        """Инициализируем статистику"""
        self.setting = setting
        # Игра запускается в неактивном состоянии
        self.game_active = False
        # Рекорд не должен сбрасыватся
        self.high_score = 0
        self.reset_stats()

    def reset_stats(self):
        """Инициализируем статистику, изменяющую в ходе игры"""
        self.ship_left = self.setting.ship_limit
        self.score = 0
        self.level = 1