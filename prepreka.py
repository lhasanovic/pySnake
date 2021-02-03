import random
import pygame

#sve (osim boje) je isto kao Hrana
class Prepreka():
    def __init__(self, settings):
        self.settings = settings
        self.position = (0,0)
        self.boja = self.settings.paletaBoja[2]
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, self.settings.kvadrata-1)*self.settings.stranicaKvadrata, random.randint(0, self.settings.kvadrata-1)*self.settings.stranicaKvadrata)


    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (self.settings.stranicaKvadrata, self.settings.stranicaKvadrata))
        pygame.draw.rect(surface, self.boja, r)
        pygame.draw.rect(surface, self.settings.paletaBoja[4], r, self.settings.debljinaLinija)