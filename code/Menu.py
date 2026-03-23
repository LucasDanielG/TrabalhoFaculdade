import pygame.image
from pygame import Surface, Rect
from pygame.ftfont import Font
import sys

from code.Const import MENU_OPTION, COLOR_WHITE, WIN_WIDTH, COLOR_BLUE


class Menu:
    def __init__(self, window):
        self.window = window
        self.surf = pygame.image.load('./Assets/imagem_menux.png')
        self.rect = self.surf.get_rect(left=0, top=0)

    def run(self):
        menu_option = 0
        pygame.mixer_music.load('./Assets/jogo_musica.mp3')
        pygame.mixer_music.play(-1)

        while True:
            # Desenha o fundo
            self.window.blit(source=self.surf, dest=self.rect)

            # Desenha as opções do Menu
            for i in range(len(MENU_OPTION)):
                if i == menu_option:
                    self.menu_text(20, MENU_OPTION[i], COLOR_BLUE, ((WIN_WIDTH / 2), 360 + 30 * i))
                else:
                    self.menu_text(20, MENU_OPTION[i], COLOR_WHITE, ((WIN_WIDTH / 2), 360 + 30 * i))

            pygame.display.flip()

            # Processamento de eventos (Teclado)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        if menu_option < len(MENU_OPTION) - 1:
                            menu_option += 1
                        else:
                            menu_option = 0

                    if event.key == pygame.K_UP:
                        if menu_option > 0:
                            menu_option -= 1
                        else:
                            menu_option = len(MENU_OPTION) - 1

                    if event.key == pygame.K_RETURN:
                        # Pega a opção, remove espaços e coloca tudo em MAIÚSCULO
                        opcao_limpa = MENU_OPTION[menu_option].strip().upper()

                        # LOG DE TESTE: Isso vai aparecer no seu terminal (telinha preta embaixo)
                        print(f"DEBUG: Você apertou Enter em: '{opcao_limpa}'")

                        # Verifica se a palavra CREDIT existe na opção
                        if "CREDIT" in opcao_limpa:
                            print("DEBUG: Entrando na tela de créditos...")
                            from code.Credits import Credits
                            tela_creditos = Credits(self.window)
                            tela_creditos.run()
                        else:
                            return MENU_OPTION[menu_option]
    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)