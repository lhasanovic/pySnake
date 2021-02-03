class Settings():
	def __init__(self):
		self.skala=0
		self.paletaBoja = ((194, 192, 148), (169, 165, 135), (220, 149, 150), (57, 0, 64), (115, 0, 113))
		

		self.animacijaPozicija=0

		self.zvuk = False

		"""
		OVO DEFINISATI DOBRO
		self.brzinaZmije = 5+20*self.skala
		self.zmijaUbrzava = True
		self.ubrzavanje = 4*self.skala
		self.rubovi = True
		"""

		self.brzina = 5


		
		self.prepreke = False
		self.zmijaUbrzava = False
		self.rubovi = False
		self.mijenjaSmijer = True
		self.viseHrane = False

		self.font = "8-BIT WONDER.TTF"
		self.fontSize = 26
		self.pozicijaSkora = (245, 35)
		self.pozicijaPauze = (221, 240)
		self.pozicijaKrajIgre = (200, 240)
		self.debljinaLinija = 3


		#izvedene vrijednosti
		self.stranicaKvadrata = int(32*(3/4)**self.skala)
		self.kvadrata = int(18*(4/3)**self.skala)
		self.stranica = self.kvadrata*self.stranicaKvadrata #mozda hard lockati na 576?

		#postulati
		self.gore = (0,-1)
		self.dole = (0,1)
		self.lijevo = (-1,0)
		self.desno = (1,0)

		self.pixelZmija = [[0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 3, 2, 2, 2, 2, 2, 3, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 3, 2, 4, 2, 2, 2, 4, 2, 3, 0, 0, 0, 0],
		[0, 0, 0, 0, 3, 2, 2, 4, 2, 2, 2, 4, 2, 3, 0, 0, 0, 0],
		[0, 0, 0, 0, 3, 2, 1, 1, 2, 2, 2, 1, 1, 2, 3, 0, 0, 0],
		[0, 0, 0, 0, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 0, 0, 0],
		[0, 0, 0, 0, 3, 2, 2, 3, 3, 2, 3, 3, 3, 3, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 3, 2, 1, 1, 3, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 3, 3, 3, 2, 1, 1, 3, 3, 3, 3, 3, 0, 0, 0, 0],
		[0, 0, 3, 2, 2, 2, 3, 2, 1, 1, 3, 2, 2, 2, 3, 0, 0, 0],
		[0, 3, 2, 2, 3, 3, 2, 2, 1, 1, 3, 2, 2, 2, 2, 3, 0, 0],
		[0, 3, 2, 2, 2, 2, 2, 2, 1, 1, 1, 3, 2, 2, 2, 3, 0, 0],
		[0, 3, 2, 2, 2, 1, 1, 1, 1, 1, 3, 2, 2, 1, 1, 3, 0, 0],
		[0, 0, 3, 3, 1, 1, 1, 1, 1, 3, 2, 1, 1, 3, 3, 0, 0, 0],
		[0, 0, 0, 0, 3, 3, 3, 3, 3, 2, 1, 3, 3, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 3, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 3, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0]]


	def promijeni_settings(self, skala):
		self.skala=skala
		if skala==0:
			self.paletaBoja = ((194, 192, 148), (169, 165, 135), (220, 149, 150), (57, 0, 64), (115, 0, 113))
			self.animacijaPozicija=0
			self.rubovi = False
			self.mijenjaSmijer = True
			self.zmijaUbrzava = False
			self.prepreke = False
			self.brzina = 5

		if skala==1:
			self.paletaBoja = ((0, 57, 68), (0, 108, 103), (241, 148, 179), (254, 177, 1), (255, 235, 198))
			self.animacijaPozicija=75
			self.rubovi = True
			self.mijenjaSmijer = False
			self.zmijaUbrzava = False
			self.prepreke = True
			self.brzina = 15

		if skala==2:
			self.paletaBoja = ((179, 0, 27), (38, 38, 38), (37, 92, 153), (126, 163, 204), (204, 173, 143))
			self.animacijaPozicija=130
			
			self.rubovi = False
			self.mijenjaSmijer = False
			self.zmijaUbrzava = True
			self.prepreke = False
			self.brzina = 5


		self.stranicaKvadrata = int(32*(3/4)**skala)
		self.kvadrata = int(18*(4/3)**skala)
		self.stranica = self.kvadrata*self.stranicaKvadrata