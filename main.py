import sys
from pygame.sprite import Group
import pygame
from files.settings import Setting
from files.ship import Ship
from files.bullet import Bullet



class AlienInvasion:
    """Класс для управления ресурсами"""

    def __init__(self):
        """Инициализирует игру и создает игровые ресурсы"""
        pygame.init()

        # назначение цвета фона
        self.settings = Setting()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption(" Alien Invasion")

        self.ship = Ship(self.screen, self.settings)
        self.bullets = Group()

    def run_game(self):
        """Запуск основного цикла игры"""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_screen()

    def _update_bullets(self):
        """Обновляет позицци снарядов и уничтожвет старые"""
        self.bullets.update()
        # удаление снарядов, вышедших за край экрана
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _update_screen(self):
        # при каждом проходе цикла перерисовывается экран
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # отображение последнего прорисованного экрана
        pygame.display.flip()

    def _check_events(self):
        # отслеживание событий клавиатуры и мыши
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self._event_down(event)
            elif event.type == pygame.KEYUP:
                self._event_up(event)

    def _event_down(self, event):
        if event.key == pygame.K_SPACE:
            self._fire_bullet()
        if event.key == pygame.K_q:
            sys.exit()
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = True

    def _event_up(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Создание нового снаряда и включение его в группу bullets"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self.settings,self.screen,self.ship)
            self.bullets.add(new_bullet)

if __name__ == '__main__':
    # создаем экзепляр и запуск игры
    ai = AlienInvasion()
    ai.run_game()
