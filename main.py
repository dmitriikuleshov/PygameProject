import sys
import pygame
from settings import *


class ButtonSprite(pygame.sprite.Sprite):
    def __init__(self, group_single,
                 text, size=(250, 100),
                 main_color=pygame.Color('black'),
                 hover_color=pygame.Color('green')
                 ):
        super().__init__(group_single)

        self.main_color = main_color
        self.hover_color = hover_color
        self.text = text

        self.image = pygame.Surface(size)
        self.pos = (WIDTH / 2 - self.image.get_width() / 2, 60)
        self.rect = self.image.get_rect(topleft=self.pos)

        self.font = pygame.font.Font("assets/font.ttf", 30)
        self.text = self.font.render(self.text, True, "#b68f40")

        self.image.fill(self.main_color)
        self.image.blit(self.text,
                        (self.image.get_width() / 2 - self.text.get_width() / 2,
                         self.image.get_height() / 2 - self.text.get_height() / 2)
                        )

    def set_pos_y(self, topleft_y):
        self.pos = (WIDTH / 2 - self.image.get_width() / 2, topleft_y)
        self.rect = self.image.get_rect(topleft=self.pos)

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            return True

    def check_hover(self, pos):
        if self.rect.collidepoint(pos):
            self.image.fill(self.hover_color)
            self.image.blit(self.text,
                            (self.image.get_width() / 2 - self.text.get_width() / 2,
                             self.image.get_height() / 2 - self.text.get_height() / 2)
                            )
            return True
        else:
            self.image.fill(self.main_color)
            self.image.blit(self.text,
                            (self.image.get_width() / 2 - self.text.get_width() / 2,
                             self.image.get_height() / 2 - self.text.get_height() / 2)
                            )
            return False


class Game:
    def __init__(self):
        # base setup
        pygame.init()
        self.screen = pygame.display.set_mode(SIZE, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
        pygame.display.set_caption('Game')
        self.clock = pygame.time.Clock()

        # resizable window
        self.virtual_surface = pygame.Surface(SIZE)
        self.current_size = self.screen.get_size()

        # main menu text
        self.font = pygame.font.Font("assets/font.ttf", 30)
        self.main_menu_text = self.font.render("MAIN MENU", True, "#b68f40")
        self.main_menu_text_pos = (WIDTH / 2 - self.main_menu_text.get_width() / 2, 10)

        # buttons group
        self.buttons_group = pygame.sprite.Group()

        # play button
        self.play_button = ButtonSprite(self.buttons_group, text='PLAY', main_color=pygame.Color((0, 0, 16)),
                                        hover_color=pygame.Color((0, 200, 0)))
        self.play_button_pos = (self.screen.get_width() / 2 - self.play_button.image.get_width() / 2, 60)

        # quit button
        self.quit_button = ButtonSprite(self.buttons_group, text='QUIT', main_color=pygame.Color((0, 0, 16)),
                                        hover_color=pygame.Color((200, 0, 0)))
        self.quit_button.set_pos_y(200)

    @staticmethod
    def terminate():
        pygame.quit()
        sys.exit()

    def play(self):
        ...

    def main_menu(self):
        self.screen = pygame.display.set_mode(SIZE)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.play_button.check_click(event.pos):
                        pygame.mouse.set_cursor(pygame.cursors.arrow)
                        self.play()
                    if self.quit_button.check_click(event.pos):
                        self.terminate()

            mouse_pos = pygame.mouse.get_pos()
            if self.play_button.check_hover(mouse_pos) or self.quit_button.check_hover(mouse_pos):
                pygame.mouse.set_cursor(pygame.cursors.diamond)
            else:
                pygame.mouse.set_cursor(pygame.cursors.arrow)

            self.screen.fill('grey')
            self.screen.blit(self.main_menu_text, self.main_menu_text_pos)
            self.buttons_group.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.main_menu()
