import pygame.image
from pygame import Surface, Rect
from pygame.ftfont import Font

from code.Const import MENU_OPTION, COLOR_WHITE, WIN_WIDTH


class Menu:
    def __init__(self, window):
        self.window = window
        self.surf = pygame.image.load('./Assets/imagem_menux.png')
        self.rect = self.surf.get_rect(left=0, top=0)

    def run(self, ):
        pygame.mixer_music.load('./Assets/jogo_musica.mp3')
        pygame.mixer_music.play(-1)
        while True:
             self.window.blit(source=self.surf, dest=self.rect)

             for i in range(len(MENU_OPTION)):
                 self.menu_text(20, MENU_OPTION[i], COLOR_WHITE, ((WIN_WIDTH / 2),360 + 30 * i))

             pygame.display.flip()

             for event in pygame.event.get():
                if event.type == pygame.QUIT:
                 print('quitting')
                 pygame.quit()  # window close
                 quit()  # pygame end



    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)
