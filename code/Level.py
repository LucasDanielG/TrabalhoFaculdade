import pygame
import sys
import random

from code.Const import WIN_WIDTH, WIN_HEIGHT, COLOR_WHITE, COLOR_BLACK


class Level:
    def __init__(self, window, name, menu_return):
        self.window = window
        self.name = name
        self.menu_return = menu_return

        # 1. Assets de Fundo
        self.bg_image = pygame.image.load('./Assets/campo_completo.png').convert()
        self.bg_image = pygame.transform.scale(self.bg_image, (WIN_WIDTH, WIN_HEIGHT))

        # 2. Área do Gol
        self.gol_area = pygame.Rect(200, 150, 400, 120)

        # 3. Assets da Bola
        self.bola_pos = [WIN_WIDTH // 2, WIN_HEIGHT - 100]
        self.bola_vel = [0, 0]
        self.chutada = False
        self.sprite_bola = pygame.image.load('./Assets/bola.png').convert_alpha()
        self.sprite_bola = pygame.transform.scale(self.sprite_bola, (24, 24))
        self.bola_rect = self.sprite_bola.get_rect()

        # 4. Assets do Goleiro
        tamanho_goleiro = (80, 100)
        self.sprite_goleiro_parado = pygame.image.load('./Assets/goleiro_pronto.png').convert_alpha()
        self.sprite_goleiro_parado = pygame.transform.scale(self.sprite_goleiro_parado, tamanho_goleiro)

        self.sprite_pulando_esq = pygame.image.load('./Assets/goleiro_pulo_esq.png').convert_alpha()
        self.sprite_pulando_esq = pygame.transform.scale(self.sprite_pulando_esq, (120, 100))
        self.sprite_pulando_dir = pygame.transform.flip(self.sprite_pulando_esq, True, False)

        self.goleiro_sprite_atual = self.sprite_goleiro_parado
        self.goleiro_rect = self.goleiro_sprite_atual.get_rect()
        self.goleiro_rect.centerx = self.gol_area.centerx
        self.goleiro_rect.bottom = 260

        self.goleiro_estado = "PARADO"
        self.goleiro_destino_x = self.goleiro_rect.x

        # 5. Placar e Feedbacks
        self.gols = 0
        self.defesas = 0
        self.fonte_placar = pygame.font.SysFont("Lucida Sans Typewriter", 30, bold=True)
        self.fonte_instrucoes = pygame.font.SysFont("Lucida Sans Typewriter", 20)
        self.mira_pos = [WIN_WIDTH // 2, 200]

        self.img_gol = pygame.image.load('./Assets/gol.jpg').convert_alpha()
        self.img_gol = pygame.transform.scale(self.img_gol, (500, 200))
        self.img_derrota = pygame.image.load('./Assets/perdeu_mane.png').convert_alpha()
        self.img_derrota = pygame.transform.scale(self.img_derrota, (500, 200))
        self.feedback_rect = self.img_gol.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2))

        # 6. Sons
        self.som_gol = pygame.mixer.Sound('./Assets/gol_torcida.mp3')
        self.som_derrota = pygame.mixer.Sound('./Assets/vaias.mp3')

    def run(self):
        pygame.mixer.music.set_volume(0.2)
        clock = pygame.time.Clock()

        while True:
            clock.tick(60)
            self.window.blit(self.bg_image, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.mixer.music.set_volume(1.0)
                        return

                    if event.key == pygame.K_SPACE and not self.chutada:
                        self.bola_vel[0] = (self.mira_pos[0] - self.bola_pos[0]) / 15
                        self.bola_vel[1] = (self.mira_pos[1] - self.bola_pos[1]) / 15
                        self.chutada = True

                        escolha = random.choice(["ESQ", "DIR", "CENTRO"])
                        if escolha == "ESQ":
                            self.goleiro_destino_x = self.gol_area.left + 20
                            self.goleiro_sprite_atual = self.sprite_pulando_esq
                        elif escolha == "DIR":
                            self.goleiro_destino_x = self.gol_area.right - 140
                            self.goleiro_sprite_atual = self.sprite_pulando_dir
                        else:
                            self.goleiro_destino_x = self.gol_area.centerx - 40
                            self.goleiro_sprite_atual = self.sprite_goleiro_parado
                        self.goleiro_estado = "MOVENDO"

            if not self.chutada:
                self.mira_pos = list(pygame.mouse.get_pos())
                pygame.draw.line(self.window, (0, 0, 0), self.bola_pos, self.mira_pos, 4)
                pygame.draw.line(self.window, (255, 255, 0), self.bola_pos, self.mira_pos, 2)

                inst_mouse = self.fonte_instrucoes.render("Mire com o MOUSE", True, (255, 255, 255))
                inst_space = self.fonte_instrucoes.render("ESPAÇO para chutar", True, (255, 255, 255))
                self.window.blit(inst_mouse, (WIN_WIDTH // 2 - inst_mouse.get_width() // 2, WIN_HEIGHT - 60))
                self.window.blit(inst_space, (WIN_WIDTH // 2 - inst_space.get_width() // 2, WIN_HEIGHT - 35))

            if self.goleiro_estado == "MOVENDO":
                if abs(self.goleiro_rect.x - self.goleiro_destino_x) > 5:
                    if self.goleiro_rect.x < self.goleiro_destino_x:
                        self.goleiro_rect.x += 15
                    else:
                        self.goleiro_rect.x -= 15
                self.goleiro_rect = self.goleiro_sprite_atual.get_rect(topleft=self.goleiro_rect.topleft)

            if self.chutada:
                self.bola_pos[0] += self.bola_vel[0]
                self.bola_pos[1] += self.bola_vel[1]
                self.bola_rect.center = (int(self.bola_pos[0]), int(self.bola_pos[1]))

                if self.goleiro_rect.colliderect(self.bola_rect):
                    self.defesas += 1
                    self.mostrar_feedback(self.img_derrota, self.som_derrota)

                elif self.bola_pos[1] < self.gol_area.top:
                    if self.gol_area.collidepoint(self.bola_pos[0], self.gol_area.top + 5):
                        self.gols += 1
                        self.mostrar_feedback(self.img_gol, self.som_gol)
                    else:
                        pygame.time.delay(500)
                        self.reset_game()

            self.window.blit(self.goleiro_sprite_atual, self.goleiro_rect)
            self.window.blit(self.sprite_bola, self.bola_rect)

            rect_placar = pygame.Rect(20, 20, 220, 95)
            pygame.draw.rect(self.window, (30, 30, 30), rect_placar, border_radius=12)
            pygame.draw.rect(self.window, (200, 200, 200), rect_placar, 2, border_radius=12)

            t_gols = self.fonte_placar.render(f"GOLS: {self.gols}", True, (255, 255, 0))
            t_defs = self.fonte_placar.render(f"DEFESAS: {self.defesas}", True, (255, 80, 80))
            self.window.blit(t_gols, (rect_placar.x + 15, rect_placar.y + 12))
            self.window.blit(t_defs, (rect_placar.x + 15, rect_placar.y + 52))

            pygame.display.flip()

    # ATENÇÃO: Verifique se estas funções abaixo têm exatamente 4 espaços de recuo
    def mostrar_feedback(self, imagem, som):
        som.play()
        self.window.blit(imagem, self.feedback_rect)
        pygame.display.flip()
        pygame.time.delay(3000)
        pygame.mixer.stop()
        self.reset_game()

    def reset_game(self):
        self.bola_pos = [WIN_WIDTH // 2, WIN_HEIGHT - 100]
        self.bola_vel = [0, 0]
        self.chutada = False
        self.goleiro_estado = "PARADO"
        self.goleiro_sprite_atual = self.sprite_goleiro_parado
        self.goleiro_rect = self.goleiro_sprite_atual.get_rect()
        self.goleiro_rect.centerx = self.gol_area.centerx
        self.goleiro_rect.bottom = 260
        self.bola_rect.center = (int(self.bola_pos[0]), int(self.bola_pos[1]))