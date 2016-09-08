from CTFAObjet import *

class Dynasties(CTFAObjet):
	"""la gestion des dynasties"""
	objetNom = "dynastie"
	legende = ("armes", "nom", "couleur", "Personnes")
	
	def afficheUn(self, t, w, l):
		Label(w, text=t["armoirie"]).grid(row=l, column=0, sticky=E)
		Label(w, text=t["nom"]).grid(row=l, column=1, sticky=E)
		Label(w, text=t["couleur"]).grid(row=l, column=2, sticky=E)
		Label(w, text=t["occurence"]).grid(row=l, column=3, sticky=E)
		
if __name__ == '__main__':
	from connexion import *
	h = GestionnaireHTTP()
	lesDynasties = Dynasties(h)