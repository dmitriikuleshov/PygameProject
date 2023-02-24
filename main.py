import sys
import pygame
import json
from settings import *
from level1 import Level1


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
        self.pos = (pygame.display.get_surface().get_width() / 2 - self.image.get_width() / 2, 60)
        self.rect = self.image.get_rect(topleft=self.pos)

        self.font = pygame.font.Font("assets/font.ttf", 30)
        self.text = self.font.render(self.text, True, "#b68f40")

        self.image.fill(self.main_color)
        self.image.blit(self.text,
                        (self.image.get_width() / 2 - self.text.get_width() / 2,
                         self.image.get_height() / 2 - self.text.get_height() / 2)
                        )

    def set_pos_y(self, topleft_y):
        self.pos = (pygame.display.get_surface().get_width() / 2 - self.image.get_width() / 2 - 200, topleft_y)
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
        self.screen = pygame.display.set_mode((900, 600))
        pygame.display.set_caption('ТЫСЯЧА ЧЕРТЕЙ')
        self.clock = pygame.time.Clock()

        # resizable window
        self.virtual_surface = pygame.Surface(SIZE)
        self.current_size = self.screen.get_size()
        self.level = Level1(self, self.virtual_surface)

        # main menu
        self.background_image = pygame.image.load('assets/background.png')
        self.font = pygame.font.Font("assets/font.ttf", 50)
        self.main_menu_text = self.font.render("MAIN MENU", True, "#b68f40")
        self.main_menu_text_pos = (self.screen.get_width() / 2 - self.main_menu_text.get_width() / 2, 20)

        # buttons group
        self.buttons_group = pygame.sprite.Group()

        # play button
        self.play_button = ButtonSprite(self.buttons_group, text='PLAY', size=(300, 100),
                                        main_color=pygame.Color((0, 0, 16)),
                                        hover_color=pygame.Color((0, 200, 0)))
        self.play_button.set_pos_y(200)
        # quit button
        self.quit_button = ButtonSprite(self.buttons_group, text='QUIT', main_color=pygame.Color((0, 0, 16)),
                                        hover_color=pygame.Color((200, 0, 0)))
        self.quit_button.set_pos_y(360)

        self.start_sound = pygame.mixer.Sound('data2/sounds/Start/start.wav')

        # score
        self.score_label = self.font.render("SCORE", True, "orange")
        self.score_label_pos = (575, 150)
        self.score_texts = []
        self.update_score_list()

    @staticmethod
    def terminate():
        pygame.quit()
        sys.exit()

    def play(self):
        self.start_sound.play()
        self.level.start_bg_music()
        self.screen = pygame.display.set_mode((900, 600), pygame.RESIZABLE)
        self.level = Level1(self, self.virtual_surface)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.VIDEORESIZE:
                    self.current_size = event.size
            self.virtual_surface.fill(pygame.Color(63, 56, 81))
            self.level.run()

            scaled_surface = pygame.transform.scale(self.virtual_surface, self.current_size)
            self.screen.blit(scaled_surface, (0, 0))
            pygame.display.flip()
            self.clock.tick(FPS)

    def update_score_list(self):
        self.score_texts.clear()
        with open("coin_counters.json", mode="r") as json_file:
            try:
                coin_counters_list = json.load(json_file)
                coin_counters_list.reverse()
            except Exception:
                coin_counters_list = ["0"]
            for ind, score in enumerate(coin_counters_list):
                text = self.font.render(score, True, "yellow")
                text_pos = (675, 225 + 75 * ind)
                self.score_texts.append((text, text_pos))

    def main_menu(self):
        self.update_score_list()
        self.screen = pygame.display.set_mode((900, 600))
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

            self.screen.blit(self.background_image, (0, 0))
            self.screen.blit(self.main_menu_text, self.main_menu_text_pos)
            self.screen.blit(self.score_label, self.score_label_pos)
            for elem in self.score_texts:
                text = elem[0]
                pos = elem[1]
                self.screen.blit(text, pos)
            self.buttons_group.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.main_menu()
