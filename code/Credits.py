import pygame
import sys
from code.Const import WIN_WIDTH, WIN_HEIGHT


class Credits:
    def __init__(self, window):
        self.window = window
        # Carregamos a nova imagem (salve o novo arquivo como 'feedback_creditos.png')
        from code.Const import resource_path
        self.bg_image = pygame.image.load(resource_path('./Assets/creditos.png')).convert()
        self.bg_image = pygame.transform.scale(self.bg_image, (WIN_WIDTH, WIN_HEIGHT))

    def run(self):
        while True:
            # 1. Desenha a imagem inteira na tela
            self.window.blit(self.bg_image, (0, 0))

            # 2. Processa os eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return  # Sai do loop dos créditos e volta para o menu

            # 3. Atualiza a tela
            pygame.display.flip()