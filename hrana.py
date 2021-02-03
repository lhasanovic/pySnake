import random
import pygame

class Hrana():
    #slično kao za kreiranje novog objekta tipa Zmija, potrebno je proslijediti postavke pri kreiranju novog objekta tipa Hrana
    def __init__(self, settings):
        self.settings = settings #nova hrana poprima proslijeđene postavke
        self.position = (0,0) #inicijalna pozicija hrane je 0,0
        self.boja = self.settings.paletaBoja[3] #definisana boja za hranu
        self.randomize_position() #zatim se pozicija randomizira

    def randomize_position(self):
        #prvo se randomiziraju x i y koordinate nove hrane u opsegu od 0 do dimenzijalnosti stranice ekrana u kvadratima (18, 24 ili 32) umanjene za 1
        #zatim se te koordinate pomnože sa stranicom kvadrata
        #ovako se dobiju koordinate u pixelima za iscrtavanje kvadrata na ekranu
        self.position = (random.randint(0, self.settings.kvadrata-1)*self.settings.stranicaKvadrata, random.randint(0, self.settings.kvadrata-1)*self.settings.stranicaKvadrata)


    def draw(self, surface):
        #rendera se kvadrat sa pozicijama u pikselima i odgovarajućim stranicama kvadrata iz settings-a
        r = pygame.Rect((self.position[0], self.position[1]), (self.settings.stranicaKvadrata, self.settings.stranicaKvadrata))
        #zatim se iscrtava kvadrat definisane boje za hranu
        pygame.draw.rect(surface, self.boja, r)
        #i odgovarajući outline
        pygame.draw.rect(surface, self.settings.paletaBoja[4], r, self.settings.debljinaLinija)