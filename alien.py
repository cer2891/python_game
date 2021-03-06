import  pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """ Класс представляющий одного пришельца"""

    def __init__(self, screen , setting):
        """ Инициализирует пришельца и задает его начальную позицию"""
        super(Alien,self).__init__()
        self.screen = screen
        self.setting = setting

        # Загрузка изображения пришельца и начальное значение атрибута rect
        self.image = pygame.image.load('images/alien.png')
        self.rect = self.image.get_rect()

        # Каждый новый пришелец появляется в левом верхнем углу экрана
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Сохранение точной горизонтальной позиции пришельца
        self.x = float(self.rect.x)

    def update(self):
        """Перемещаем вправо пришельца"""
        self.x += (self.setting.alien_speed * self.setting.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        """ Возращает True, если пришелец находится
            у края экрана """
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True