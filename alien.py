import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()
        self.rect.x = self.screen.get_rect().width - self.rect.width
        self.settings = ai_game.settings
        self.settings.bullet_speed_max = self.rect.width - 2
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.life = self.settings.alien_life

    def update(self):
        self.y += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.y = self.y

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.bottom >= screen_rect.bottom or self.rect.top <= 0:
            return True

    def check_life(self):
        self.life -= self.settings.bullet_damage
        if self.life <= 0:
            return True


