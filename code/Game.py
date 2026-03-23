
import pygame
from code.Menu import Menu

class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((800, 600))

    def run(self, ):
        while True:
            menu = Menu(self.window)
            menu.run()
            pass

            #for event in pygame.event.get():
                #if event.type == pygame.QUIT:
                    #print('quitting')
                    #pygame.quit()  # window close
                    #quit()  # pygame end
