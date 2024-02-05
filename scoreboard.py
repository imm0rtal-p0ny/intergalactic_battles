import pygame


class Scoreboard:
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.money_img = pygame.image.load('images/money.png')

        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        self.prep_score()

    def prep_score(self):
        score_str = str(f'Score: {self.stats.score}')
        money_str = str(self.stats.money)
        lvl_speed = self.stats.level_bullet_speed
        lvl_damage = self.stats.level_bullet_damage
        lvl_time = self.stats.level_bullet_time
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)
        self.money_image = self.font.render(money_str, True, self.text_color, self.settings.bg_color)
        self.score_rect = self.score_image.get_rect()
        self.money_rect = self.money_image.get_rect()
        self.money_img_rect = self.money_img.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.money_rect.right = self.screen_rect.right - 20
        self.money_img_rect.right = self.money_rect.left - 20
        self.score_rect.top = 20
        self.money_img_rect.top = self.score_rect.bottom + 20
        self.money_rect.center = (self.money_rect.center[0], self.money_img_rect.center[1])

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.money_image, self.money_rect)
        self.screen.blit(self.money_img, self.money_img_rect)

