import pygame.font


class Button:
    def __init__(self, menu_board, msg, width, height, top, left):
        self.screen = menu_board.screen
        self.screen_rect = self.screen.get_rect()
        self.width = width
        self.height = height
        self.button_color = (0, 250, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.top = top
        self.rect.left = left
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def bt_action(self):
        pass

