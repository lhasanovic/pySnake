import pygame

class Menu():
    def __init__(self, game):
        #za kreiranje Oojekta tipa Meni bilo koje od vrste menija potrebno je proslijediti objekt tipa Game
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 #definišu se koordinate za sredinu ekrana
        self.run_display = True #varijabla potrebna za provjeru da li meni treba biti upaljen
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 100
        self.running = True

    #rendera zvjezdicu (kao kursor) na koordinatama koje odgovaraju kursoru
    def draw_cursor(self):
        self.game.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y) 

    #ažurira ekran nakon izmjena
    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0)) 
        pygame.display.update()
        self.game.reset_keys()

#glavni izbornik
class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        #inicjalno se kursor postavlja na Start (Igraj)
        self.state = "Start"
        #zatim se definišu koordinate za ispis naziva svakog od pod-menija
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 50
        self.scorex, self.scorey = self.mid_w, self.mid_h + 70
        self.gamemodex, self.gamemodey = self.mid_w, self.mid_h + 90
        #koordinate za ispis kursora se postavljaju lijevo od koordinata za Start
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    #metoda za ispis glavnog izbornika
    def display_menu(self):
        self.run_display = True
        #dok nije izabran drugi izbornik (ili dok igrica nije pokrenuta)
        #neka se ispišu svi nazivi pod-menija na odgovarajućim pozicijama
        #istovremeno nek se čeka na input za pomjeranje kursora ili gašenje prozora
        #i neka se sve ponovo ispiše sa novom pozicijom kursora
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Glavni izbornik', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text("Igraj", 20, self.startx, self.starty)
            self.game.draw_text("Postavke", 20, self.optionsx, self.optionsy)
            self.game.draw_text("High Score", 20, self.scorex, self.scorey)
            self.game.draw_text("Mod igre", 20, self.gamemodex, self.gamemodey)

            self.draw_cursor()
            self.blit_screen()

    #ukoliko je stisnuta tipka dole, trenutno "stanje" menija i koordinate kursora se mijenjaju na opciju ispod
    #ukoliko nema opcije ispod, kursor i stanje se vraćaju na prvo "Start" stanje
    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.scorex + self.offset, self.scorey)
                self.state = 'Score'
            elif self.state == 'Score':
                self.cursor_rect.midtop = (self.gamemodex + self.offset, self.gamemodey)
                self.state = 'Game Mode'
            elif self.state == 'Game Mode':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'

        #ukoliko je stisnuta tipka gore, dešava se isto kao za tipku dole samo obratnim redoslijedom
        elif self.game.UP_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.gamemodex + self.offset, self.gamemodey)
                self.state = 'Game Mode'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
            elif self.state == 'Score':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Game Mode':
                self.cursor_rect.midtop = (self.scorex + self.offset, self.scorey)
                self.state = 'Score'

    #povjerava na koji pod-meni pokazuje kursor u vrijeme stiska na Enter
    #i shodno postavlja trenutni prikaz menija na onaj koji je odabran
    #takođe postavlja run_display na False kako bi prikaz glavnog izbornika mogao iskočiti iz while petlje
    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.loading = True
            elif self.state == 'Options':
                self.game.curr_menu = self.game.options
            elif self.state == 'Score':
                self.game.curr_menu = self.game.score
            elif self.state == 'Game Mode':
                self.game.curr_menu = self.game.gamemode
            self.run_display = False

#analogno MainMenu
class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Zvuk'
        #ukoliko je u postavkama uključen zvuk, prikaz u meniju će biti isto postavljen na ON
        if self.game.zvuk:
            self.zvukState = "ON"
        else:
            self.zvukState = "OFF"

        #volx i voly su koordinate za ispis opcije Zvuk
        self.volx, self.voly = self.mid_w, self.mid_h + 20
        #controlsx i controlsy su koordinate za placeholder opciju u postavkama
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 40
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

    #radi na isti način kao display_menu za MainMenu
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.game.draw_text('Postavke', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30)
            self.game.draw_text("Zvuk", 15, self.volx, self.voly)
            self.game.draw_text(self.zvukState, 12, self.volx+90, self.voly)
            self.game.draw_text("PlaceHolder", 15, self.controlsx, self.controlsy)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        #ukoliko je stisnuta tipka back space, run display se postavlja na False kako bi prikaz ovog menija iskočio iz while petlje
        #i prikaz trenutnog menija se postavlja ponovo na Glavni izbornik
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        
        #ukoliko su stisnute tipke gore ili dole, kursor prilagođava svoju poziciju i "stanje"
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            if self.state == 'Zvuk':
                self.state = 'PlaceHolder'
                self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
            elif self.state == 'PlaceHolder':
                self.state = 'Zvuk'
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
        
        #ukoliko je stisnut Enter dok kursor prikazuje na "Zvuk", tada se mijenja boolean vrijednost zvuk u objektu Game koja indicira da li je zvuk upaljen ili nije
        elif self.game.START_KEY:
            if self.state == 'Zvuk':
                if self.game.zvuk:
                    self.game.zvuk = False
                    self.zvukState = "OFF"
                else:
                    self.game.zvuk = True
                    self.zvukState = "ON"

#slično prethodnim menijima
class GameModeMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Mod 1'
        self.selectedState = "Selektovan mod 1"
        self.mod1x, self.mod1y = self.mid_w, self.mid_h + 20
        self.mod2x, self.mod2y = self.mid_w, self.mid_h + 40
        self.mod3x, self.mod3y = self.mid_w, self.mid_h + 60
        
        #za svaki mod je definisan i opis moda koji se prikazuje u zavinosti od toga na kojem je stanju kursor
        self.opis1 = "zmija mijenja smjer kad jede"
        self.opis2 = "rubovi su teleporti + postoje prepreke"
        self.opis3 = "zmija ubrzava kad jede"

        self.opis = self.opis1

        self.cursor_rect.midtop = (self.mod1x + self.offset, self.mod1y)

    #ispisuje koji je mod trenutno selektovan kao naslov menija
    #ispisuje opis moda na koji trenutno pokazuje kursor u footeru
    #i ispisuje 3 moda za izbor
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text(self.opis, 16, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 200)
            self.game.draw_text(self.selectedState, 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30)
            self.game.draw_text("Mod 1", 15, self.mod1x, self.mod1y)
            self.game.draw_text("Mod 2", 15, self.mod2x, self.mod2y)
            self.game.draw_text("Mod 3", 15, self.mod3x, self.mod3y)
            self.draw_cursor()
            self.blit_screen()

    #provjerava koje je prirode input sa tastature
    def check_input(self):
        #ako je u pitanju backspace, vraća se na glavni izbornik
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False

        #ukoliko su u pitanju UP ili DOWN
        #tada se kursor kreće shodno i usput se adaptuje koji će opis biti ispisan u footer-u
        elif self.game.DOWN_KEY:
            if self.state == 'Mod 1':
                self.state = 'Mod 2'
                self.opis = self.opis2
                self.cursor_rect.midtop = (self.mod2x + self.offset, self.mod2y)
            elif self.state == 'Mod 2':
                self.state = 'Mod 3'
                self.opis = self.opis3
                self.cursor_rect.midtop = (self.mod3x + self.offset, self.mod3y)
            elif self.state == 'Mod 3':
                self.state = 'Mod 1'
                self.opis = self.opis1
                self.cursor_rect.midtop = (self.mod1x + self.offset, self.mod1y)


        elif self.game.UP_KEY:
            if self.state == 'Mod 1':
                self.state = 'Mod 3'
                self.opis = self.opis3
                self.cursor_rect.midtop = (self.mod3x + self.offset, self.mod3y)
            elif self.state == 'Mod 2':
                self.state = 'Mod 1'
                self.opis = self.opis1
                self.cursor_rect.midtop = (self.mod1x + self.offset, self.mod1y)
            elif self.state == 'Mod 3':
                self.state = 'Mod 2'
                self.opis = self.opis2
                self.cursor_rect.midtop = (self.mod2x + self.offset, self.mod2y)

        #ukoliko je stisnut enter onda se mijenjaju postavke igrice u zavisnosti od moda koji je odabran
        #takođe se boje svih izbornika prilagođavaju bojama iz odabranih postavki
        elif self.game.START_KEY:
            if self.state == 'Mod 1':
                self.game.settings.promijeni_settings(0)
                self.selectedState = "Selektovan mod 1"
                
            elif self.state == 'Mod 2':
                self.game.settings.promijeni_settings(1)
                self.selectedState = "Selektovan mod 2"

            elif self.state == 'Mod 3':
                self.game.settings.promijeni_settings(2)
                self.selectedState = "Selektovan mod 3"

            self.game.BLACK, self.game.WHITE = self.game.settings.paletaBoja[0], self.game.settings.paletaBoja[4]
            self.game.COLOR1, self.game.COLOR2, self.game.COLOR3 = self.game.settings.paletaBoja[1], self.game.settings.paletaBoja[2], self.game.settings.paletaBoja[3]   
            



#najjednostavniji meni
#jedino što prima kao input su enter ili back space
#u slučaju stiska enter ili backspace, prikaz se "vraća" na glavni izbornik

class ScoreMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    #jedino ispisuje top 5 imena dosadašnjih igraća i njihov ostvareni score
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.main_menu.running = True
                self.game.loading = False
                self.game.curr_menu = self.game.main_menu
                
                self.run_display = False
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Score', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 100)
            self.game.draw_text(self.game.highscore[0][0], 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text(self.game.highscore[1][0], 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2)
            self.game.draw_text(self.game.highscore[2][0], 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 20)
            self.game.draw_text(self.game.highscore[3][0], 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 40)
            self.game.draw_text(self.game.highscore[4][0], 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 60)

            self.game.draw_text(str(self.game.highscore[0][1]), 15, self.game.DISPLAY_W / 2 + 50, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text(str(self.game.highscore[1][1]), 15, self.game.DISPLAY_W / 2 + 50, self.game.DISPLAY_H / 2)
            self.game.draw_text(str(self.game.highscore[2][1]), 15, self.game.DISPLAY_W / 2 + 50, self.game.DISPLAY_H / 2 + 20)
            self.game.draw_text(str(self.game.highscore[3][1]), 15, self.game.DISPLAY_W / 2 + 50, self.game.DISPLAY_H / 2 + 40)
            self.game.draw_text(str(self.game.highscore[4][1]), 15, self.game.DISPLAY_W / 2 + 50, self.game.DISPLAY_H / 2 + 60)

            self.blit_screen()
