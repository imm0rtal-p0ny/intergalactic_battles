import sys
import pygame
from scoreboard import Scoreboard
from time import sleep
from game_stats import GameStats
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from menu_board import MenuBoard


class AlienInvasion:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.shoot_sound = pygame.mixer.Sound('sound/shot.mp3')
        self.bang_sound = pygame.mixer.Sound('sound/bang.mp3')
        self.pause_sound = pygame.mixer.Sound('sound/pause.mp3')
        self.play_sound = pygame.mixer.Sound('sound/play.mp3')
        self.game_sound = pygame.mixer.Sound('sound/music.mp3')
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption('AlienInvasion')
        self.stats = GameStats. load(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        self.last_bullet_spawn_time = pygame.time.get_ticks()
        self.sb = Scoreboard(self)
        self.menu_start = MenuBoard(self)
        self.menu_pause = MenuBoard(self, True)
        self.background_image = pygame.image.load('images/space.jpeg')
        self.background_image = pygame.transform.scale(self.background_image,
                                                       (self.settings.screen_width, self.settings.screen_height))

    def run_game(self):
        while True:
            self._check_events()
            self._update_screen()
            if self.stats.game_active and not self.stats.game_pause:
                self.ship.update()
                self._update_bullets()
                self._update_alien()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
               self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
               self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_button_event(mouse_pos)

    def _check_button_event(self, mouse_pos):
        if not self.stats.game_pause:
            self._check_play_button(mouse_pos)

        else:
            self._check_resume_button(mouse_pos)
            self._check_restart_button(mouse_pos)
        self._check_update_button(mouse_pos)

    def _check_update_button(self, mouse_pos):
        for bt in self.menu_start.update_button:
            if bt.rect.collidepoint(mouse_pos):
                bt.bt_action()
                self.menu_start.update()
                self.menu_pause.update()
                self.sb.prep_score()

    def _check_play_button(self, mouse_pos):
        button_clicked = self.menu_start.bt_play.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self._restart_game()
            self.play_sound.play()

    def _check_resume_button(self, mouse_pos):
        button_clicked = self.menu_pause.bt_resume.rect.collidepoint(mouse_pos)
        if button_clicked and self.stats.game_pause:
            self.stats.game_pause = False
            self.stats.game_active = True
            self.play_sound.play()
            pygame.mouse.set_visible(False)

    def _restart_game(self):
        self.settings.initialize_dynamic_settings()
        self.stats.reset_stats()
        self.stats.game_active = True
        self.stats.game_pause = False
        self.stats.game_over = False
        self.sb.prep_score()
        self.aliens.empty()
        self.bullets.empty()
        self._create_fleet()
        self.ship.center_ship()
        pygame.mouse.set_visible(False)

    def _check_restart_button(self, mouse_pos):
        button_clicked = self.menu_pause.bt_restart.rect.collidepoint(mouse_pos)
        if button_clicked and self.stats.game_pause:
            self._restart_game()
            self.play_sound.play()

    def _check_keydown_events(self, event):
        if event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_q:
            self.stats.save()
            sys.exit()
        elif event.key == pygame.K_SPACE:
            if self.stats.game_active:
                self.pause_sound.play()
                self.stats.game_active = False
                self.stats.game_pause = True
                pygame.mouse.set_visible(True)
            elif self.stats.game_over:
                self._restart_game()
                self.play_sound.play()
            else:
                self.stats.game_active = True
                self.stats.game_pause = False
                self.play_sound.play()
                pygame.mouse.set_visible(False)

    def _check_keyup_events(self, event):
        if event.key == pygame.K_DOWN:
            self.ship.moving_down = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False

    def _fire_bullet(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_bullet_spawn_time > self.settings.bullet_spawn_delay and self.stats.game_active:
            self.last_bullet_spawn_time = current_time
            new_bullet = Bullet(self)
            self.shoot_sound.play()
            self.bullets.add(new_bullet)

    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_y = self.settings.screen_height - (2 * alien_height)
        available_space_x = (self.settings.screen_width - 2 * alien_width) - 7 * alien_width - self.ship.rect.width
        number_aliens_y = available_space_y // (2 * alien_height)
        rows = available_space_x // (2 * alien_width)

        for row in range(rows):
            for alien_number_y in range(number_aliens_y):
                self._create_alien(alien_number_y, row)

    def _create_alien(self, alien_number_y, row):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.y = alien_height + 2 * alien_height * alien_number_y
        alien.x = (self.settings.screen_width - 2 * alien_width) - 2 * alien_width * row
        alien.rect.y = alien.y
        alien.rect.x = alien.x
        self.aliens.add(alien)

    def _update_screen(self):
        self.screen.blit(self.background_image, (0, 0))
        self._fire_bullet()
        self.ship.blitme()
        if self.stats.game_active:
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.sb.show_score()
        if not self.stats.game_active:
            self.menu_start.draw_area()
        if self.stats.game_pause:
            self.menu_pause.draw_area()
        pygame.display.flip()

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.right >= self.settings.screen_width:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, False, False)
        for b, a in collisions.items():
            if not b.is_super:
                self.bullets.remove_internal(b)
            for i in a:
                if i.check_life():
                    self.stats.add_score_money()
                    if i in self.aliens:
                        self.aliens.remove_internal(i)
                        self.bang_sound.play()
                        self.sb.prep_score()
        if not self.aliens:
            self.bullets.empty()
            self.settings.level_up()
            self._create_fleet()

    def _update_alien(self):
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        self._check_aliens_left()

    def _ship_hit(self):
        self.stats.ship_left -= 1
        if self.stats.ship_left > 0:
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            sleep(1)
        else:
            self.stats.game_active = False
            self.stats.game_pause = False
            self.stats.game_over = True
            pygame.mouse.set_visible(True)

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.x -= self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_aliens_left(self):
        for alien in self.aliens.sprites():
            if alien.rect.left <= 0:
                self._ship_hit()
                break


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
