import pygame

class Ship():
    """Класс управления кораблем"""

    def __init__(self, ai_game,set):
        """Инициализируем корабль и задает его начальную позицию"""
        super(Ship,self).__init__()
        self.screen = ai_game
        self.settings = set
        self.screen_rect = ai_game.get_rect()

        # Загружаем изображение корабля и получает прямоугольник
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # Каждый новый корабль появляется у нижнего края экрана
        self.rect.midbottom = self.screen_rect.midbottom

        # Сохранение вещественной координаты центра корабля
        self.x = float(self.rect.x)

        # флаг перемещения
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Обновляем позицую корабля"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # обновление атрибута rect на основании self.x
        self.rect.x = self.x

    def blitme(self):
        """Рисует корабль в текущей позиции"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Размещаем корабль в центре нижней стороны"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x= float(self.rect.x)
