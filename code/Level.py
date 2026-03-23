from code.Entity import Entity


class Level:
    def __init__(self,  window, name, menu_option):
        self.window = window
        self.name = name
        self.menu_option = menu_option
        self.entity_list = list[Entity] = []


    def run(self, ):
        pass