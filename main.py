import sys
from pygame.sprite import Group
import pygame
from random import randint
from files.settings import Setting
from files.ship import Ship
from files.bullet import Bullet
from files.alien import Alien
from files.star import Star



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
        self.aliens = Group()
        self.star = Group()

        self._create_fleet()


    def run_game(self):
        """Запуск основного цикла игры"""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._check_fleet_edges()
            self._update_aliens()
            self._update_screen()

    def _update_aliens(self):
        """ Обновляет позиции всех пришельцев во """
        self.aliens.update()

    def _check_fleet_edges(self):
        """ Реагирует на достижение пришельцем края экрана"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """  опускает весь флот и меняет направление"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _create_fleet(self):
        """ Создание флота вторжения"""
        # Создание пришельца и вычесление количество в ряду
        # Интервал между соседними пришельцами равен половине
        # пришельца
        alien = Alien(self.screen,self.settings)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // alien_width

        # Определяем количество рядов,помещающихся на экране
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (2 * alien_height) - ship_height)
        number_rows = available_space_y // int(1.5*alien_height)

        # создание флота вторжения
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                # создание пришельца и размещение его в ряду
                self._create_alien(alien_number,row_number)

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self.screen,self.settings)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height*row_number
        self.aliens.add(alien)

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

        self.aliens.draw(self.screen)
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
