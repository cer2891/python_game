import  pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """ Класс представляющий одного пришельца"""

    def __init__(self, screen):
        """ Инициализирует пришельца и задает его начальную позицию"""
        super.__init__()
        self.screen = screen

        # Загрузка изображения пришельца и начальное значение атрибута rect
        self.image= pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Каждый новый пришелец появляется в левом верхнем углу экрана
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Сохранение точной горизонтальной позиции пришельца
        self.x = float(self.rect.x)
