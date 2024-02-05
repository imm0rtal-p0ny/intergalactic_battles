class Settings:

    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.ship_speed = 1.5
        self.ship_limit = 1
        self.bullet_speed = 0.1
        self.bullet_speed_max = 68
        self.bullet_width = 15
        self.bullet_height = 3
        self.bullet_color = (0, 250, 0)
        self.bullet_allowed = 10
        self.bullet_is_super = False
        self.bullet_damage = 0.1
        self.bullet_damage_up_scale = 0.1
        self.bullet_spawn_delay = 10000
        self.alien_speed = 0.5
        self.alien_life = 1
        self.fleet_drop_speed = 10
        # self.fleet_direction 1 - down, -1 up
        self.fleet_direction = 1
        self.speedup_scale = 1.3
        self.level_scale = 0.1
        self.level_time_scale = 100
        self.level_ship = 1
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed = 1.5
        self.alien_speed = 1.0
        self.fleet_direction = 1
        self.alien_life = 1

    def level_up(self):
        self.alien_speed *= self.speedup_scale
        self.alien_life *= self.speedup_scale


