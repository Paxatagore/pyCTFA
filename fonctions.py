from CTFAObjet import CTFAObjet
from tkinter import *

class Fonctions(CTFAObjet):
	"""la gestion des fonctions"""
	objetNom = "fonction"
	legende = ("Nom", "Occurences", "Tag associé")
	
	def __init__(self, h, mode, tags):
		"""initialisation"""
		self.tags = tags
		CTFAObjet.__init__(self, h, mode)
	
	def corrigeUne(self, f):
		"""corrige une fonction"""
		#la correction consiste à créer un attribut "tag", qui est le nom correspond au tag lié à la fonction (lieuId est un numéro)
		f["tag"] = self.tags.getById(f["lieuId"])["nom"]
	
	def afficheUn(self, t, w, l):
		"""affiche une fonction"""
		Label(w, text=t["nom"], relief=GROOVE).grid(row=l, column=0, sticky=W, padx=2, pady=2)
		Label(w, text=t["occurence"], relief=GROOVE).grid(row=l, column=1, sticky=W, padx=2, pady=2)
		Label(w, text=t["tag"], relief=GROOVE).grid(row=l, column=2, sticky=W, padx=2, pady=2)
		
		
		
if __name__ == '__main__':
	#à écrire