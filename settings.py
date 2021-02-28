class Setting():
    """Класс для хранения всех типов настроек игры Alien Invasion"""

    def __init__(self):
        """Иницилизация настройки игры"""
        # Параметры экрана
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)
        self.ship_speed = 2
        self.ship_limit = 1

        # Параметры снаряда

        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 255, 255)
        self.bullets_allowed = 3

        # темп ускорения игры
        self.speed_scale = 1.1
        # Темп роста стоимости пришельцев
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """ Инициализируем динамичкские настройки"""
        # fleet_direction = 1 обозначает движение вправо, а -1 влево
        self.fleet_direction = 1

        self.bullet_speed = 2
        # параметры пришельцев
        self.alien_speed = 1
        self.fleet_drop_speed = 10

        # Подсчет очков
        self.alien_points = 50

    def increase_speed(self):
        """ Увеличивает настройки скорости"""
        self.ship_speed *= self.speed_scale
        self.bullet_speed *= self.speed_scale
        self.fleet_drop_speed *= self.speed_scale

        # увеличивыем стоимость пришельцев
        self.alien_points = int(self.alien_points *
                                self.score_scale)
        # print(self.alien_points)
