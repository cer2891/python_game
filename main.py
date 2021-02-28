import sys
from pygame.sprite import Group
import pygame
from time import sleep

from files.settings import Setting
from files.ship import Ship
from files.bullet import Bullet
from files.alien import Alien
from files.game_stat import GameStats
from files.button import Button
from files.scoreboard import Scoreboard


class AlienInvasion:
    """Класс для управления ресурсами"""

    def __init__(self):
        """Инициализирует игру и создает игровые ресурсы"""
        pygame.init()

        # назначение цвета фона
        self.settings = Setting()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption(" Alien Invasion")

        # Создание экзепляра для хранения игровой статистики
        self.stats = GameStats(self.settings)

        self.ship = Ship(self.screen, self.settings)
        self.bullets = Group()
        self.aliens = Group()
        self.sb = Scoreboard(self.screen,self.settings,
                             self.stats,self.ship)

        self._create_fleet()
        self.play_button = Button(self.screen, "Play")

    def run_game(self):
        """Запуск основного цикла игры"""
        while True:
            self._check_events()
            self.ship.update()
            if self.stats.game_active:
                self._update_bullets()
                self._update_aliens()
                self._check_fleet_edges()
            self._update_screen()

    # Обработка столкновение корабля с пришельцем
    def _ship_hit(self):
        """Обработка столкновение корабля с пришельцем"""
        # Уменьшение ship_left
        if self.stats.ship_left > 0:
            self.stats.ship_left -= 1

            # очистка списков пришельцев и снарядов
            self.aliens.empty()
            self.bullets.empty()

            # Создание нового флота и размещение корабля в центре
            self._create_fleet()
            self.ship.center_ship()

            # пауза
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    # Реагирует на достижение пришельцем края экрана
    def _check_fleet_edges(self):
        """ Реагирует на достижение пришельцем края экрана"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    # опускает весь флот и меняет направление
    def _change_fleet_direction(self):
        """  опускает весь флот и меняет направление"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    # Создание флота вторжения
    def _create_fleet(self):
        """ Создание флота вторжения"""
        # Создание пришельца и вычесление количество в ряду
        # Интервал между соседними пришельцами равен половине
        # пришельца
        alien = Alien(self.screen, self.settings)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // alien_width

        # Определяем количество рядов,помещающихся на экране
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (2 * alien_height) - ship_height)
        number_rows = available_space_y // int(1.5 * alien_height)

        # создание флота вторжения
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                # создание пришельца и размещение его в ряду
                self._create_alien(alien_number, row_number)

    # Проверяет , добрались пришельцы до нижнего края экрана
    def _check_aliens_bottom(self):
        """Проверяет , добрались пришельцы до нижнего края экрана"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # происходит то же что и при столкновении с кораблем
                self._ship_hit()
                break

    # Создание пришельцев
    def _create_alien(self, alien_number, row_number):
        alien = Alien(self.screen, self.settings)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    # Обновляет позиции всех пришельцев
    def _update_aliens(self):
        """ Обновляет позиции всех пришельцев во """
        self.aliens.update()

        # Проверка коллизий "пришелец-корабль"
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # проверить ли добрались пришельцы до края экрана
        self._check_aliens_bottom()

    # проверка попаданий в пришельцев
    # при обнаружении попаданий удалить снаряд и пришельца
    def _check_bullet_alien_collisions(self):
        # проверка попаданий в пришельцев
        # при обнаружении попаданий удалить снаряд и пришельца
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens,
                                                True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # уничтожение существующих снарядов и создание нового флота
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            # print(self.settings.fleet_drop_speed)

            # увеличение уровня
            self.stats.level +=1
            self.sb.prep_level()

    # Обновляет позицци снарядов и уничтожвет старые
    def _update_bullets(self):
        """Обновляет позицци снарядов и уничтожвет старые"""
        self.bullets.update()
        # удаление снарядов, вышедших за край экрана
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    # Создание нового снаряда и включение его в группу bullets
    def _fire_bullet(self):
        """Создание нового снаряда и включение его в группу bullets"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self.settings, self.screen, self.ship)
            self.bullets.add(new_bullet)

    # при каждом проходе цикла перерисовывается экран
    def _update_screen(self):
        # при каждом проходе цикла перерисовывается экран
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)

        # Вывод информации о счете
        self.sb.show_score()
        # Кнопка Play отображается в том случаи,
        # если игра активна
        if not self.stats.game_active:
            self.play_button.draw_button()
        # отображение последнего прорисованного экрана
        pygame.display.flip()

    # отслеживание событий клавиатуры и мыши
    def _check_events(self):
        # отслеживание событий клавиатуры и мыши
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self._event_down(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(event,mouse_pos)
            elif event.type == pygame.KEYUP:
                self._event_up(event)

    # кнопку нажатие
    def _event_down(self, event):
        if event.key == pygame.K_SPACE:
            self._fire_bullet()
        if event.key == pygame.K_q:
            sys.exit()
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        if event.key == pygame.K_p and not self.stats.game_active:
            self._reset_game()

    # кнопку отпускание
    def _event_up(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    # Проверка нажатия кнопки Play
    def _check_play_button(self,event,mouse_pos):
        """Запускаем новую игру при нажатии Play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self._reset_game()

    def _reset_game(self):
        # Сброс игровой статистики
        self.stats.game_active = True
        self.stats.reset_stats()
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()
        # Очистка списков пришельцев и снарядов
        self.aliens.empty()
        self.bullets.empty()
        # создание нового флота и размещение корабля в
        # в центре
        self._create_fleet()
        self.ship.center_ship()
        # указатель мышки скрываем
        pygame.mouse.set_visible(False)
        self.settings.initialize_dynamic_settings()


if __name__ == '__main__':
    # создаем экзепляр и запуск игры
    ai = AlienInvasion()
    ai.run_game()
