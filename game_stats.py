import csv
import os


class GameStats:
    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.settings.stats = self
        self.reset_stats()
        self.game_active = False
        self.game_pause = False
        self.money = 0
        self.count_up_money = 10
        self.level_bullet_speed = 0
        self.level_bullet_damage = 0
        self.level_bullet_time = 0
        self.game_over = False

    def reset_stats(self):
        self.score = 0

    def add_score_money(self):
        self.score += int((100 * self.settings.alien_life) // 1)
        self.money += int((1 * self.settings.alien_life) // 1)

    def bullet_speed_up(self):
        if self.money > self.count_up_money:
            if (speed := self.settings.bullet_speed + self.settings.level_scale) < self.settings.bullet_speed_max:
                self.money -= self.count_up_money
                self.settings.bullet_speed = speed
                self.level_bullet_speed += 1
                self.settings.level_ship += 1
                self.count_up_money = self.settings.level_ship * 10

    def bullet_time_up(self):
        if self.money > self.count_up_money:
            self.money -= self.count_up_money
            self.settings.bullet_spawn_delay -= self.settings.level_scale
            self.level_bullet_time += 1
            self.settings.level_ship += 1
            self.count_up_money = self.settings.level_ship * 10

    def bullet_damage_up(self):
        if self.money > self.count_up_money:
            self.money -= self.count_up_money
            self.settings.bullet_damage += self.settings.bullet_damage_up_scale
            self.level_bullet_time += 1
            self.settings.level_ship += 1
            self.count_up_money = self.settings.level_ship * 10

    def save(self, file_path='save/game_stats.csv'):
        with open(file_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['money', 'count_up_money', 'level_bullet_speed',
                                 'level_bullet_damage', 'level_bullet_time'])

            csv_writer.writerow([self.money, self.count_up_money,
                                 self.level_bullet_speed, self.level_bullet_damage, self.level_bullet_time])

    @staticmethod
    def load(ai_game, file_path='save/game_stats.csv'):
        self = GameStats(ai_game)
        if os.path.exists(file_path):
            with open(file_path, 'r') as csvfile:
                csv_reader = csv.reader(csvfile)
                headers = next(csv_reader)
                data = next(csv_reader)
                for header, value in zip(headers, data):
                    setattr(self, header, type(getattr(self, header))(value))
            self.settings.bullet_speed = self.level_bullet_speed * self.settings.level_scale + self.settings.bullet_speed
            self.settings.bullet_damage = self.level_bullet_damage * self.settings.level_scale + self.settings.bullet_damage
            self.settings.bullet_spawn_delay = self.settings.bullet_spawn_delay - self.level_bullet_time * self.settings.level_time_scale
            self.settings.level_ship = (self.level_bullet_time + self.level_bullet_damage + self.level_bullet_speed)
            self.count_up_money = self.settings.level_ship * 10
            print(self.settings.bullet_damage, self.settings.bullet_speed, self.settings.bullet_spawn_delay)

        return self
