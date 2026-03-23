from abc import ABC


class Entity(ABC):


    def __init__(self):
        self.name = None
        self.surf = None
        self.rect = None


    def run(self, ):
        pass