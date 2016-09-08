from CTFAObjet import CTFAObjet
from tkinter import *

class Fonctions(CTFAObjet):
	"""la gestion des fonctions"""
	objetNom = "fonction"
	legende = ("Nom", "Occurences", "Tag associé")
	
	def __init__(self, h, tags):
		self.tags = tags
		CTFAObjet.__init__(self, h)
	
	def corrigeUne(self, f):
		"""corrige une fonction"""
		f["tag"] = self.tags.getById(f["lieuId"])["nom"]
	
	def afficheUn(self, t, w, l):
		Label(w, text=t["nom"], bg='white').grid(row=l, column=0, sticky=E)
		Label(w, text=t["occurence"], bg='white').grid(row=l, column=1, sticky=E)
		Label(w, text=t["tag"], bg='white').grid(row=l, column=2, sticky=E)
		
		
		
if __name__ == '__main__':
	import connexion
	http = GestionnaireHTTP()
	lesFonctions = Fonctions()
	