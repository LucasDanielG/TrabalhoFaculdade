WIN_WIDTH = 800
WIN_HEIGHT = 533

COLOR_WHITE = (255, 255, 255)

MENU_OPTION = ('NOVO JOGO',
               'CREDITO',
               'EXIT')

COLOR_BLUE = (0, 0, 255)
COLOR_BLACK = (0, 0, 0)

import os
import sys

def resource_path(relative_path):
    """ Retorna o caminho absoluto para o recurso, para o PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)