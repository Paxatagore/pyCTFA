from CTFAObjet import *

class Dynasties(CTFAObjet):
	"""la gestion des dynasties"""
	objetNom = "dynastie"
	legende = ("armes", "nom", "couleur", "Personnes")
	
	def afficheUn(self, t, w, l):
		"""affiche une dynastie"""
		Label(w, text=t["armoirie"]).grid(row=l, column=0,  sticky=W, padx=2, pady=2)
		Label(w, text=t["nom"]).grid(row=l, column=1,  sticky=W, padx=2, pady=2)
		Label(w, text=t["couleur"]).grid(row=l, column=2,  sticky=W, padx=2, pady=2)
		Label(w, text=t["occurence"]).grid(row=l, column=3,  sticky=W, padx=2, pady=2)
		
if __name__ == '__main__':
	#à écrire