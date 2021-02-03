import pygame
from menu import *
from zmija import Zmija
from hrana import Hrana
from prepreka import Prepreka
from settings2 import Settings
import sys


class Game():
    def __init__(self):

        #inicira pygame i postavlja naziv i ikonu prozora
        pygame.init()
        pygame.display.set_caption("TSI pySnake")
        self.icon = pygame.image.load("icon.png")
        pygame.display.set_icon(self.icon)


        self.unosImena = True
        self.ime = ""

        #kreira objekt settings koji u sebi ima predefinisane postavke za prvi mod igre
        self.settings = Settings()

        #inicijacija clock-a za diktiranje takta igrice
        self.clock = pygame.time.Clock()

        #varijable koje prate koji je screen upaljen
        self.running, self.playing, self.loading = True, False, False

        #kontrole za menu
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        
        #definicija širine i visine ekrana
        self.DISPLAY_W, self.DISPLAY_H = self.settings.stranica, self.settings.stranica
        
        #kreira surface po kojem se igrica "crta"
        self.display = pygame.Surface((self.DISPLAY_W,self.DISPLAY_H))
        self.window = pygame.display.set_mode(((self.DISPLAY_W,self.DISPLAY_H)))
        
        #self.font_name = '8-BIT WONDER.TTF'
        self.font_name = pygame.font.get_default_font()

        #varijabla koja određuje mod igre
        self.skala=0

        #postavljanje boja u posebne varijable
        self.BLACK, self.WHITE = self.settings.paletaBoja[0], self.settings.paletaBoja[4]
        self.COLOR1, self.COLOR2, self.COLOR3 = self.settings.paletaBoja[1], self.settings.paletaBoja[2], self.settings.paletaBoja[3]
        
        #boolean varijabla koja definiše da li je zvuk uključen ili nije
        self.zvuk = self.settings.zvuk

        #kreira svaki od pod-menia posebno
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.score = ScoreMenu(self)
        self.gamemode = GameModeMenu(self)

        #inicijalno postavlja trenutni menu na main_menu
        self.curr_menu = self.main_menu

        #highscoru dodaje vrijednost praznog niza
        self.highscore = []

        #definiše se font za obavijesti koji će se koristiti za pauzu i kraj igrice
        self.myfont = pygame.font.SysFont(self.settings.font, self.settings.fontSize, bold=True)
        self.obavijestFont = pygame.font.SysFont(self.settings.font, self.settings.fontSize+20, bold=True)

    #funkcija za učitavanje high-score-a iz fajla
    def read_highscore(self):
        #dok je otvoren demotest, čitaj iz njega i storaj podatke kao tuple u x sa delimiterom " "
        with open("demofile.txt", "r") as f:
            for line in f:
                x = line.split(" ")
                #y postaje tuple x time da se od x[1] otkida "\n"
                y = (x[0], int(x[1][:-1]))
                #u niz highscore se zatim appendaju obje vrijednosti kao tuple
                self.highscore.append(y)
        #potrebno je zatvoriti file
        f.close()


    #metoda koja iscrtava šahovnicu (po kojoj se zmija kreće) na screen
    def drawGrid(self):
        for y in range(0, int(self.settings.kvadrata)): #definisati ove dvije petlje da crtaju baklavu umjesto kvadrata
            for x in range(0, int(self.settings.kvadrata)):                
                #ukoliko je zbir koordinata kvadratića djeljiv sa 2 crta kvadratić jedne boje, ako nije, druge boje
                if (x+y)%2 == 0:
                    r = pygame.Rect((x*self.settings.stranicaKvadrata, y*self.settings.stranicaKvadrata), (self.settings.stranicaKvadrata, self.settings.stranicaKvadrata))
                    pygame.draw.rect(self.display, self.settings.paletaBoja[0], r)
                else:
                    rr = pygame.Rect((x*self.settings.stranicaKvadrata, y*self.settings.stranicaKvadrata), (self.settings.stranicaKvadrata, self.settings.stranicaKvadrata))
                    pygame.draw.rect(self.display, self.settings.paletaBoja[1], rr)


    #početni dio igrice za unos imena
    def name_input(self):
       

        while self.unosImena:

            #čeka unos nekog inputa
            for event in pygame.event.get():
                #ukoliko je input click na X, gasi igricu
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                #ukoliko je input unos sa tastature
                if event.type == pygame.KEYDOWN:
                    #provjerava kakve je prirode taj unos
                    if event.key == pygame.K_RETURN:
                        #ukoliko je enter, tako što ga mijenja na False i program iskače iz ove while petlje
                        self.unosImena = False
                    if event.key == pygame.K_BACKSPACE:
                        #ukoliko je unos backspace, ime postaje ono što je bilo prije unosa prethodnog stringa
                        self.ime = self.ime[:-1]
                    else:
                        #svi ostli inputi sa tastature se dodaju varijabli ime
                        self.ime += event.unicode

            #funkcija fill boji podlogu display-a u boju proslijeđenu RGB tripletom
            self.display.fill(self.BLACK)

            #draw text funkcije ispod ispisuju instrukcije na ekran i dosadašnju vrijednost varijable ime 
            self.draw_text("unesi ime", 40, 100, 100)
            self.draw_text(self.ime, 40, 300, 100)
            self.draw_text("nakon unosa imena pritisni enter", 15, 300, 400)

            #funkcija blit_screen je ovdje potrebna da napravi adekvatan update trenutnog stanja ekrana
            self.blit_screen()

            #clock.tick(60) odradi 1 otkucaj frekvencije 60Hz prije nego što krene na sljedeći korak
            self.clock.tick(60)
        


    def pauza(self):

        #ukoliko je u postavkama zvuk aktiviran, zvuk će se prvo ugasiti i play-at će se zvuk za početak pauze
        if self.zvuk:    
            pygame.mixer.music.pause()

            pygame.mixer.music.load("pauzaPocetak.wav")
            pygame.mixer.music.play(0,0.0)


        #rendera se tekst nad obavijestFontom
        text = self.obavijestFont.render("PAUZA", 1, self.settings.paletaBoja[4])

        #ispiše se renderani text
        self.window.blit(text, self.settings.pozicijaPauze)

        #display se update-uje nakon ispisa "pauza"
        pygame.display.update()
        
        #sada ova while petlja čeka neki input
        while True:
            for event in pygame.event.get():

                #ukoliko je input click na X, gasi se sve
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    self.running = False

                #ukoliko je input stisak na SPACE, pokreće se muzika za kraj pauze i nastavlja se puštati popratna muzika za igru (ukoliko je u postavkama odabrana muzika)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.zvuk:    
                            pygame.mixer.music.load("pauzaKraj.wav")
                            pygame.mixer.music.play(0,0.0)
                            pygame.mixer.music.load("music"+str(self.settings.skala)+".wav")
                            pygame.mixer.music.play(-1,0.0)
                        
                        #funkcija prestaje za izvršavanjem i ne vraća ništa
                        return


    #jako slično pauzi
    def kraj_igre(self):
        
        #zaustalvlja se zvuk ukoliko je aktivan u postavkama,
        if self.zvuk:
            pygame.mixer.music.stop()
            pygame.mixer.music.load("krajIgre.wav")
            pygame.mixer.music.play(0,0.0)

        #rendera se i ispisuje tekst "KRAJ IGRE" na ekranu
        text = self.obavijestFont.render("KRAJ IGRE", 1, self.settings.paletaBoja[4])
        self.window.blit(text, self.settings.pozicijaKrajIgre)
        pygame.display.update()

        #sačeka se jedna sekunda prije prelaska na sljedeći korak u kodu
        self.clock.tick(1)

        #trenutni meni se postavlja na Score meni
        self.curr_menu = self.score

        #postavlja se prikaz menia na True (potrebno za while petlju koja prikazuje menije)
        self.curr_menu.running = True

        #playing stavlja na False budući da više ne "igramo"
        self.playing = False

        #u varijablu highscore se dodaje uneseno ime i ostvareni score
        self.highscore.append((self.ime, self.zmija.skor))

        #highscore se zatim sortira
        self.highscore.sort(key=lambda tup: tup[1], reverse=True)

        #pisanje skora u file

        #otvara se txt file-a sa score-om za rewrite
        f = open("demofile.txt", "w")

        #za svaki tuple (ime, skor) u nizu highscore upisuje se ime, skor konvertovan u string i novi red u txt file za score
        for i in self.highscore:
        
            f.write(i[0]+" "+str(i[1])+"\n")

        #potrebno je zatvoriti file nakon upisa
        f.close()



    #funkcija u kojoj je definisana logika igrice
    def game_loop(self):

        """
        while self.playing:
            self.check_events()
            if self.START_KEY:
                self.playing= False
            self.display.fill(self.BLACK)
            self.draw_text('Thanks for Playing', 20, self.DISPLAY_W/2, self.DISPLAY_H/2)
            self.window.blit(self.display, (0,0))
            pygame.display.update()
            self.reset_keys()

        """

        #kreira se novi objekt zmija koji je tipa Zmija iz file-a zmija.py
        self.zmija = Zmija(self.settings)

        #isto vrijedi i za hranu
        self.hrana = Hrana(self.settings)

        #ukoliko je izabran mod igranja u kojem je u settingsima prepreke = True
        #kreiraju se nova tri objekta tipa Prepreka (jako slični tipu Hrana)
        if self.settings.prepreke:

            self.prepreka = Prepreka(self.settings)
            self.prepreka2 = Prepreka(self.settings)
            self.prepreka3 = Prepreka(self.settings)
            
            #služi kao step counter ponovne randomizacije prepreka
            brojacZaPrepreke=0

        #svaki od objekata zmija, prepreka, hrana uzima kao atribut trenutne vrijednosti postavki igrice

        #ukoliko je u postavkama uključen zvuk igrica čita adekvatan file sa muzikom i pušta ga sa beskonačnim repeatom
        if self.zvuk:
            music="music"+str(self.settings.skala)+".wav"
            pygame.mixer.music.load(music)
            pygame.mixer.music.play(-1,0.0)

        brzina=self.settings.brzina

        #playing je indikator da je igrica u toku
        while self.playing:

            #postavlja takt na vrijednost brzine iz postavki koja služi kao frekvencija pokreta koje zmija napravi
            self.clock.tick(brzina)

            #nakon 5 zmijinih koraka brojacZaPrepreke se resetuje
            if self.settings.prepreke:
                brojacZaPrepreke+=1
                brojacZaPrepreke%=5

            #funkcija handle_keys reaguje na unos sa tastature i vraća true ukoliko je stisnut SPACE (što je komanda za aktivaciju pauze)
            if self.zmija.handle_keys():
                self.pauza()

            #funkcija zmija ide ažurira pozicije zmije (u ovom slučaju samo ako nije došlo do aktivacije pauze) i vraća True ukoliko je
            #ispunjen uslov za kraj igre
            elif self.zmija.ide():
                self.kraj_igre()

            #poziva se funkcija za iscratanje pozadinske šahovnice
            self.drawGrid()

            #ukoliko su u postavkama uključene prepreke randomiziraju se pozicije prepreka nakon svakog petog koraka zmije
            if self.settings.prepreke:

                if brojacZaPrepreke==0:
                    self.prepreka.randomize_position()
                    self.prepreka2.randomize_position()
                    self.prepreka3.randomize_position()

                    #nek se predlažu nove koordinate prepreka sve dok su nove koordinate prepreka unutar zmijinog tijela ili hrane
                    #ovim će se while-ovi napustiti čim prepreke dobiju zadovoljavajuće nove koordinate
                    #napomena: moguće je da dvije prepreke dobiju apsolutno iste koordinate i to je ok
                    #u tom sluačaju će u narednih 5 koraka zmije postojati jedna prepreka manje
                    while self.prepreka.position in self.zmija.pozicije or self.prepreka.position==self.hrana.position:
                        self.prepreka.randomize_position()
                    while self.prepreka2.position in self.zmija.pozicije or self.prepreka2.position==self.hrana.position:
                        self.prepreka2.randomize_position()   
                    while self.prepreka3.position in self.zmija.pozicije or self.prepreka3.position==self.hrana.position:
                        self.prepreka3.randomize_position()


                #ukoliko se glava zmije nakon kretanja pojavi na poziciji bilo koje od prepreka igra završava
                if self.zmija.pozicijaGlave() == self.prepreka.position or self.zmija.pozicijaGlave() == self.prepreka2.position or self.zmija.pozicijaGlave() == self.prepreka3.position:
                    self.kraj_igre()

            #ukoliko se pozicija glave zmije nađe na poziciji hrane, zmija jede
            if self.zmija.pozicijaGlave() == self.hrana.position:
                
                self.zmija.duzina += 1 #povečava dužinu zmije
                self.zmija.skor += 1 #povečava skor
                

                #u slučaju da je zmijaUbrzava == True u postavkama, tada se frekvencija koraka zmije povečava za 2 svakim "jedenjem"
                if self.settings.zmijaUbrzava:
                    brzina += 2 
                
                #u slučaju da je u postavkama mijenjaSmijer == True, tada zmija mijenja smijer nakon svakog "jedenja"
                #nastavi kretanje u kontra pravcu u kojem se je zadnji pršljen posljednji put kretao
                if self.settings.mijenjaSmijer:
                    if self.zmija.duzina==2:
                        if self.zmija.smjer==self.settings.gore:
                            smjer=self.settings.dole
                        if self.zmija.smjer==self.settings.dole:
                            smjer=self.settings.gore
                        if self.zmija.smjer==self.settings.lijevo:
                            smjer=self.settings.desno
                        if self.zmija.smjer==self.settings.desno:
                            smjer=self.settings.lijevo
                        self.zmija.smjer=smjer
                        self.zmija.skrece(self.zmija.smjer)
                    if self.zmija.duzina>2:
                        self.zmija.mijenjaSmijer()

                #ovaj while spriječaa da se nova hrana pojavi unutar tijela zmije
                while self.hrana.position in self.zmija.pozicije:
                    self.hrana.randomize_position()

            #iscrtavaju se zmija i hrana
            self.zmija.draw(self.display)
            self.hrana.draw(self.display)

            #ukoliko su prepreke uključene i one se iscrtavaju
            if self.settings.prepreke:
                self.prepreka.draw(self.display)
                self.prepreka2.draw(self.display)
                self.prepreka3.draw(self.display)

            #blit je potreban da se sve iscrtano rendera
            self.window.blit(self.display, (0,0))

            #rendera se tekst koji prikazuje ime i skor na vrhu ekrana
            text = self.myfont.render(self.ime+"  {0}".format(self.zmija.skor), 1, self.settings.paletaBoja[4]) 
            self.window.blit(text, self.settings.pozicijaSkora)

            #prikaz u ekranu se ažurira prethodno renderanim prikazima
            pygame.display.update()

            #uslov za kraj igre ukoliko zmija sama sebe ugrize za rep, tj ukoliko je pozicija glave jednaka bilo kojoj poziciji ostalih "pršljenova"
            if self.zmija.pozicijaGlave() in self.zmija.pozicije[1:]:
                self.kraj_igre()


    #definisane kontrole za meni
    def check_events(self):
        for event in pygame.event.get():
            #ukoliko se stisne na X, gasi se sve
            if event.type == pygame.QUIT:
                self.running, self.playing, self.loading = False, False, False
                self.curr_menu.run_display = False
                pygame.quit()
                sys.exit()

            #ukoliko je unos enter, backspace, down ili up, postavlja vrijednost True na odgovarajuću varijablu
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True

    #pomočna funkcija koja iscrtava pixel art zmiju definisanu u settings
    def crtajZmijaAnimaciju(self):
        #a postaje matrica čije su vrijednosti u rasponu 0-4
        a = self.settings.pixelZmija
        #petlja ispod iscrtava kvadrat po kvadrat bojom koja je reprezentovana vrijednošću odgovarajućeg elementa matrice
        for y in range(len(a)):
            for x in range(len(a[0])):
                r = pygame.Rect((y*self.settings.stranicaKvadrata, x*self.settings.stranicaKvadrata), (self.settings.stranicaKvadrata, self.settings.stranicaKvadrata))
                pygame.draw.rect(self.display, self.settings.paletaBoja[a[x][y]], r)

    #iscrtava 4 nova kvadrata na pozicijama očiju zmije
    #rezultat je ista zmija samo sa "zatvorenim očima"
    def zmijaZatvaraOci(self):
        r = pygame.Rect((7*self.settings.stranicaKvadrata, 2*self.settings.stranicaKvadrata), (self.settings.stranicaKvadrata, self.settings.stranicaKvadrata))
        pygame.draw.rect(self.display, self.settings.paletaBoja[2], r)
        rr = pygame.Rect((6*self.settings.stranicaKvadrata, 3*self.settings.stranicaKvadrata), (self.settings.stranicaKvadrata, self.settings.stranicaKvadrata))
        pygame.draw.rect(self.display, self.settings.paletaBoja[4], rr)
        r = pygame.Rect((11*self.settings.stranicaKvadrata, 2*self.settings.stranicaKvadrata), (self.settings.stranicaKvadrata, self.settings.stranicaKvadrata))
        pygame.draw.rect(self.display, self.settings.paletaBoja[2], r)
        rr = pygame.Rect((10*self.settings.stranicaKvadrata, 3*self.settings.stranicaKvadrata), (self.settings.stranicaKvadrata, self.settings.stranicaKvadrata))
        pygame.draw.rect(self.display, self.settings.paletaBoja[4], rr)

    #iscrtava dva nova kvadrata preko jednog od zatvorenih očiju zmije i time se dobija efekt da je zmija otvorila oko
    def zmijaOtvaraOci(self):
        r = pygame.Rect((7*self.settings.stranicaKvadrata, 2*self.settings.stranicaKvadrata), (self.settings.stranicaKvadrata, self.settings.stranicaKvadrata))
        pygame.draw.rect(self.display, self.settings.paletaBoja[4], r)
        rr = pygame.Rect((6*self.settings.stranicaKvadrata, 3*self.settings.stranicaKvadrata), (self.settings.stranicaKvadrata, self.settings.stranicaKvadrata))
        pygame.draw.rect(self.display, self.settings.paletaBoja[2], rr)

    #ova funkcija koristi iznad definisane funkcije da napravi laoding screen animaciju i pri tome pušta loading screen melodiju
    def loading_screen(self):
        if self.zvuk:
            pygame.mixer.music.load("ideZmija.wav")
            pygame.mixer.music.play(-1,0.0)

        #sačeka jednu sekundu, boji pozadinu bojom koja odgovara pozadini u animaciji zmije
        #ovo je bitno u slučaju modova igre sa "većom rezolucijom"
        #tada zmija ne popuni cijeli prozor, već samo manji kvadrat unutar prozora
        self.clock.tick(1)    
        self.display.fill(self.settings.paletaBoja[0])
        self.crtajZmijaAnimaciju()
        self.window.blit(self.display, (self.settings.animacijaPozicija,self.settings.animacijaPozicija))
        pygame.display.update()
        
        #nakon četvrtine sekunde iscrtava nove kvadrate iznad postojeće slike
        self.clock.tick(4)
        self.zmijaZatvaraOci()
        self.window.blit(self.display, (self.settings.animacijaPozicija,self.settings.animacijaPozicija))
        pygame.display.update()

        #iscrtava "zadnji" frame animacije sa odgovarajućim vremenskim intervalima između
        self.clock.tick(1)
        self.zmijaOtvaraOci()
        self.window.blit(self.display, (self.settings.animacijaPozicija,self.settings.animacijaPozicija))
        pygame.display.update()
        self.clock.tick(2)
        
        #ukoliko je uključen zvuk u postavkama, ovdje zaustavlja puštanje loading screen muzike        
        if self.zvuk:
            pygame.mixer.music.stop()

        #budući da nakon loading screena ulazimo u game loop, sada se playing postavlja na True
        self.playing = True

    #vraća sve vrijednosti za navigaciju kroz meni na false
    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    #rendera tekst u zavisnosti od stringa, veličine i pozicije, jako korisna funkcija
    def draw_text(self, text, size, x, y ):
        font = pygame.font.Font(self.font_name,size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface,text_rect)
    
    """    
    def draw_text2(self, text, size, x, y ):
        font = pygame.font.Font(self.font_name,size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        #self.display.blit(text_surface,text_rect)
        self.window.blit(text_surface,text_rect)
    """

    #iscrtava renderane stvari u prozoru i ažurira izgled prozora
    def blit_screen(self):
        self.window.blit(self.display, (0, 0))
        pygame.display.update()