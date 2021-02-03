#import settings
import pygame
import sys

class Zmija():
    #pri kreiranju objekta tipa Zmija potrebno je proslijediti generalne postavke igrice
    def __init__(self, settings):
        self.settings = settings #zmijine postavke postaju naslijeđene postavke
        self.pozicije = [((self.settings.stranica/2), (self.settings.stranica/2))] #zmija se incijalno postavlja na centar ekrana
        self.duzina = len(self.pozicije) #dužina zmije postaje dužina niza pozicije (ovo će uvijek biti 1 inicjalno, nema potrebe za ovako kompleksan način dodjeljivanja vrijednosti varijabli)
        self.smjer = settings.desno #inicijalni smjer kretanja je desno
        self.boja = settings.paletaBoja[2] #boja je triplet RGB vrijednosti na poziciji 2 iz proslijeđene palete boja (koja je niz od 5 RGB tripleta)
        self.skor = 0 #inicijalni skor je 0

    #vraća poziciju glave zmije
    def pozicijaGlave(self):
        return self.pozicije[0]

    #usmjerava zmiju u proslijeđenom smjeru (point)
    #jasnije o tome šta se dešava u funkciji handle_keys
    def skrece(self, point):
        #ukoliko se zmija usmjeri u kontra smjeru u kojem je išla i ukoliko zmija ima "rep" (ukoliko joj je dužina>1) ništa se ne dešava
        #point je jedan od 4 definisana smjera unutar settings
        if self.duzina > 1 and (point[0]*-1, point[1]*-1) == self.smjer:
            return
        #ukoliko je proslijeđeni smjer validan, smjer kretanja postaje proslijeđeni smjer
        else:
            self.smjer = point

    #usmjerava zmiju u smjeru kontra onog u kojem bi se kretao zadnji pršljen
    def mijenjaSmijer(self):
        #okreće pozicije zmije
        self.pozicije.reverse()
        #definiše novi smjer tako što oduzima koordinate zadnjeg i predzadnjeg (nakon reversa prvog i drugog pršljena)
        self.smjer=int((self.pozicije[0][0]-self.pozicije[1][0])/self.settings.stranicaKvadrata), int((self.pozicije[0][1]-self.pozicije[1][1])/self.settings.stranicaKvadrata)
        #funkcijom skreće usmjerava zmiju shodno
        self.skrece(self.smjer)

    #funkcija ide ažurira nove koordinate zmije nakon svakog koraka
    #i vraća True ukoliko je ispunjen uslov za kraj igre
    def ide(self):
        #privremeno zadržava vrijednosti pozicije glave i smjera
        cur = self.pozicijaGlave()
        x,y = self.smjer
        
        #u slučaju da u postavkama nisu definisani rubovi (teleporti) zmija može ispasti iz ekrana i ovo rezultira krajem igre
        if not self.settings.rubovi:
            #kreira se novi pršljen u sljedećem koraku kretanja zmije
            new = (((cur[0]+(x*self.settings.stranicaKvadrata))), (cur[1]+(y*self.settings.stranicaKvadrata)))
           
            #ukoliko je novi pršljen van ekrana rezultat je kraj igre
            if new[0]>self.settings.stranica-1 or new[1]>self.settings.stranica-1 or new[0]<0 or new[1]<0:
                return True
        
        #u slučaju da rubovi (teleporti) jesu uključeni i novi pršljen (nova glava zmije) napusti ekran, tada se novi pršljen (glava zmije) treba pojaviti sa druge strane ekrana
        else:
            new = (((cur[0]+(x*self.settings.stranicaKvadrata))%self.settings.stranica), (cur[1]+(y*self.settings.stranicaKvadrata))%self.settings.stranica)



        #ukoliko je novi pršljen unutar zmijinog tijela
        if len(self.pozicije) > 2 and new in self.pozicije[2:]:
            return True #kraj igre
        #ukoliko nije, novi pršljen se dodaje na nultu poziciju pršljena zmije
        else:
            self.pozicije.insert(0,new)

            #briše se zadnji pršljen
            if len(self.pozicije) > self.duzina:
                self.pozicije.pop()
            
            return False #nije kraj igre

    #iscrtava zmiju na ekranu pršljen po pršljen
    def draw(self, surface):
        for p in self.pozicije:
            r = pygame.Rect((p[0], p[1]), (self.settings.stranicaKvadrata, self.settings.stranicaKvadrata))
            pygame.draw.rect(surface, self.boja, r) #unutrašnjost kvadrata
            pygame.draw.rect(surface, self.settings.paletaBoja[3], r, self.settings.debljinaLinija) #outline kvadrata

    #funkcija koja djeluje zavisno od inputa
    def handle_keys(self):
        for event in pygame.event.get():
            #ukoliko je input click na X, gasi se igrica
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                #ukoliko je input stisak jedne od ispod definisanih tipki zmija se usmjerava funkcijom skreće i vraća False 
                if event.key == pygame.K_UP:
                    self.skrece(self.settings.gore)
                    return False #ovo znači da se ne pali pauza (isto vrijedi za ostala 3 smjera)
                elif event.key == pygame.K_DOWN:
                    self.skrece(self.settings.dole)
                    return False
                elif event.key == pygame.K_LEFT:
                    self.skrece(self.settings.lijevo)
                    return False
                elif event.key == pygame.K_RIGHT:
                    self.skrece(self.settings.desno)
                    return False
                elif event.key == pygame.K_SPACE:
                    return True #ovo znači da će se pauza upaliti