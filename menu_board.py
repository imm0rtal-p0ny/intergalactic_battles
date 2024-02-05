import pygame
from button import Button


class MenuBoard:
    def __init__(self, ai_game, m_type=False):
        self.settings = ai_game.settings
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.width = 600
        self.height = 400
        self.bg_color = (144, 247, 165)
        self.area = pygame.Surface((self.width, self.height))
        self.rect = self.area.get_rect()
        self.rect.center = self.screen_rect.center
        self.stats = ai_game.stats
        self.m_type = m_type
        self.update()

    def update(self):
        self._create_button()
        self._load_img()
        if self.m_type:
            self._create_pause_button()

    def _create_pause_button(self):
        bt_left = self.rect.center[0]
        bt_top = self.rect.top + 20
        self.bt_resume = Button(self, 'Resume', 200, 50, bt_top, bt_left - 205)
        self.bt_restart = Button(self, 'Restart', 200, 50, bt_top, bt_left + 5)

    def _create_button(self):
        bt_left = self.rect.center[0] - 100
        bt_top = self.rect.top + 20
        bt_bottom = self.rect.bottom - 20 - 50
        self.bt_play = Button(self, 'Play', 200, 50, bt_top, bt_left)
        self.update_button = []
        a = 4 * 20
        bt_width = (self.rect.width - a) // 3
        bt_height = 50
        for _ in range(3):
            if len(self.update_button) == 0:
                bt_left = self.rect.left + 20
            else:
                bt_left = self.update_button[-1].rect.right + 20
            bt = Button(self, 'Update', bt_width, bt_height, bt_bottom, bt_left)
            self.update_button.append(bt)
            self.add_func(_)

    def _load_img(self):
        cost_str = str(self.stats.count_up_money)
        self.font = pygame.font.SysFont(None, 48)
        self.text_color = (30, 30, 30)
        self.text_img = self.font.render(cost_str, True, self.text_color, self.bg_color)
        self.text_rect_list = []
        self.update_img = [
            pygame.image.load('images/count.png'),
            pygame.image.load('images/damage.png'),
            pygame.image.load('images/speed.png'),
        ]
        self.update_text = [
            self.font.render('Count', True, self.text_color, self.bg_color),
            self.font.render('Damage', True, self.text_color, self.bg_color),
            self.font.render('Speed', True, self.text_color, self.bg_color),
        ]
        self.img_money = pygame.image.load('images/money.png')
        self.update_image_rect = []
        self.update_text_rect = []
        self.img_money_rect = []
        for i in range(len(self.update_img)):
            self.update_image_rect.append(self.update_img[i].get_rect())
            self.update_text_rect.append(self.update_text[i].get_rect())
            self.img_money_rect.append(self.img_money.get_rect())
            self.text_rect_list.append(self.text_img.get_rect())
        for i in range(len(self.update_button)):
            center = self.update_button[i].rect
            bottom = center.top - 20
            self.img_money_rect[i].bottom = bottom
            self.img_money_rect[i].right = center.right
            self.text_rect_list[i].bottom = bottom
            self.text_rect_list[i].right = self.img_money_rect[i].left + 2
            self.text_rect_list[i].center = (self.text_rect_list[i].center[0], self.img_money_rect[i].center[1])
            self.update_text_rect[i].bottom = self.img_money_rect[i].top - 20
            self.update_text_rect[i].right = center.right
            self.update_text_rect[i].center = (center.center[0], self.update_text_rect[i].center[1])
            self.update_image_rect[i].bottom = self.update_text_rect[i].top - 20
            self.update_image_rect[i].right = center.right
            self.update_image_rect[i].center = (center.center[0], self.update_image_rect[i].center[1])

    def draw_area(self):
        self.area.fill(self.bg_color)
        self.screen.blit(self.area, self.rect)
        if self.m_type:
            self.bt_resume.draw_button()
            self.bt_restart.draw_button()
        else:
            self.bt_play.draw_button()
        for i in range(len(self.update_button)):
            self.update_button[i].draw_button()
            self.screen.fill(self.bg_color, self.text_rect_list[i])
            self.screen.fill(self.bg_color, self.img_money_rect[i])
            self.screen.fill(self.bg_color, self.update_text_rect[i])
            self.screen.fill(self.bg_color, self.update_image_rect[i])
            self.screen.blit(self.text_img, self.text_rect_list[i])
            self.screen.blit(self.img_money, self.img_money_rect[i])
            self.screen.blit(self.update_text[i], self.update_text_rect[i])
            self.screen.blit(self.update_img[i], self.update_image_rect[i])

    def add_func(self, num):
        if num == 0:
            self.update_button[num].bt_action = self.stats.bullet_time_up
        elif num == 1:
            self.update_button[num].bt_action = self.stats.bullet_damage_up
        elif num == 2:
            self.update_button[num].bt_action = self.stats.bullet_speed_up
