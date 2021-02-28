import pygame.font
from pygame.sprite import Group

from files.ship import Ship


class Scoreboard():
    """ Класс для вывода игровой информации"""

    def __init__(self, screen, setting, stats, ship):
        """ Инициализация атрибутов подсчета очков"""
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.settings = setting
        self.stats = stats
        self.ship = ship

        # Настройка шрифта для вывода счета
        self.text_color = (255, 0, 0)
        self.font = pygame.font.SysFont(None, 48)
        # подготовка исходного изображения
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()


    def prep_ships(self):
        """Сообщает количество оставшихся кораблей"""
        self.ships = Group()
        for ship_number in range(self.stats.ship_left):
            ship = Ship(self.screen,self.settings)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            # self.ships.add(ship)


    def prep_level(self):
        """ Преобразует уровень в графическое изображение"""
        level_str = "Уровень "+str(self.stats.level)
        self.level_image = self.font.render(level_str, True,
                                            self.text_color,
                                            self.settings.bg_color)

        # Вывод счета в правой верхней части экрана
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10


    def prep_score(self):
        """ Преобразует текущий счет в графическое изображение"""
        rounded_score = round(self.stats.score, -1)
        score_str ="Очки: "+"{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True,
                                            self.text_color,
                                            self.settings.bg_color)

        # Вывод счета в правой верхней части экрана
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """ Преобразует рекорд в графическое изображение"""
        high_score = round(self.stats.high_score, -1)
        high_score_str ="Рекорд "+ "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True,
                                            self.text_color,
                                            self.settings.bg_color)

        # Вывод счета в правой верхней части экрана
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.screen_rect.top

    def show_score(self):
        """ Вывод счет на экран"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ship.draw(self.screen)


    def check_high_score(self):
        """ Проверяет, появился ли новый рекорд"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()
