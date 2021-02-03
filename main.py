#BITNO
#ukoliko se u postavkama Zvuk prebaci na ON
#potrebno je u root folder dodati sljedeće file-ove:

#krajIgre.wav
#music0.wav
#music1.wav
#music2.wav
#pauzaKraj.wav
#pauzaPocetak.wav
#potrebno je instalirati  pygame i numpy biblioteke, tako što odemo na terminal na našem računaru i upišemo 'pip3 install --user --upgrade pip', 'pip3 install --user pygame' i 'pip3 install --user numpy' 

from game import Game
import menu
#import settings

#dodati upustva za instalaciju svih biblioteka za dokumentaciju
#upustvo za muzicke fileove

#kreira se novi objekt g tipa Game definisan u file-u game.py
g = Game()

#nad g se poziva funkcija read_highscore() koja učitava podatke iz datoteke sa dosadašnjih imenima i odgovarajućim skorovima
g.read_highscore()

#pokreće se funkcija name input koja iscrtava unos imena i pohranjuje uneseno ime
g.name_input()

#petlja koja drži igru upaljenom i omogućava ponovno igranje nakon završetka igre
while g.running:

	#ukoliko je vrijednost running trenutnog menija True, bit će taj menu prikazan
	while g.curr_menu.running:
	    g.curr_menu.display_menu()

	    #ukoliko se unutar prikaza menija promijeni vrijednost loadinga u True, tada treba prestati prikaz trenutnog menija i igrica treba preći na loading screen i zatim na samo igranje
	    if g.loading == True:
	    	g.curr_menu.running = False

	#loading screen je samo animacija zmije koja namiguje u bojama trenutnog moda igranja
	g.loading_screen()

	#game loop je glavna funkcija za igranje i u njoj je definisana sva logika kretanja zmije i odgovarajući prikaz na ekranu (u zavisnoti od izabranog moda igre)
	g.game_loop()
