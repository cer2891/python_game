import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Класс для управления снарядами выпущенными кораблем"""

    def __init__(self, ai_setting,screen,ship):
        """Создаем объект снарядов в текщей позиции корабля"""
        super(Bullet,self).__init__()
        self.screen = screen
        self.setting = ai_setting
        self.color = self.setting.bullet_color

        # Позиция снаряда в позиции (0,0) и назначение правильной позиции
        self.rect = pygame.Rect(0, 0, self.setting.bullet_width,
                                self.setting.bullet_height)
        self.rect.midtop = ship.rect.midtop

        # Позиция снаряда хранится в вещественном формате
        self.y = float(self.rect.y)

    def update(self):
        """ Перемещвет снаряд вверх по экрану"""
        # обновление позиции снаряда в вещественном формате
        self.y -= self.setting.bullet_speed
        # обновление позиции прямоугольника
        self.rect.y = self.y

    def draw_bullet(self):
        """Выыод снаряда на экран"""
        pygame.draw.rect(self.screen, self.color, self.rect)
