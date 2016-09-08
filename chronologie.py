#""" main.py """


from connexion import *
from CTFAObjet import *
from fonctions import *
from tags import *
from dynasties import *
from tkinter import *

class MainApp(Tk):
	
	def __init__(self, parent):
		Tk.__init__(self, parent)
		self.parent = parent
		self.title = "PyChronologie"
		self['bg'] = 'white'
		self.menus()
		self.espaceInstancie = 0
	
	def menus(self):
		menu = Menu(self)
		menu1 = Menu(menu, tearoff=0)
		menu1.add_command(label="Tags", command = self.afficheTags)
		menu1.add_command(label="Fonctions", command = self.afficheFonctions)
		menu1.add_command(label="Dynasties", command = self.afficheDynasties)
		menu.add_cascade(label="Afficher", menu=menu1)
		menu2 = Menu(menu, tearoff=0)
		menu2.add_command(label="Tags", command = self.ajouteTags)
		menu2.add_command(label="Fonctions", command = self.ajouteFonctions)
		menu2.add_command(label="Dynasties", command = self.ajouteDynasties)
		menu.add_cascade(label="Ajouter", menu=menu2)
		self.config(menu=menu)
		
	def afficheTags(self):
		self.creeEspace()
		lesTags.afficherTout(self.espace)
		
	def afficheFonctions(self):
		self.creeEspace()
		lesFonctions.afficherTout(self.espace)
		
	def afficheDynasties(self):
		self.creeEspace()
		lesDynasties.afficherTout(self.espace)
		
	def ajouteTags(self):
		pass
		
	def ajouteFonctions(self):
		pass
		
	def ajouteDynasties(self):
		pass
	
	def creeEspace(self):
		"""crée un frame pour l'affichage "principal" """
		if self.espaceInstancie > 0:
			self.espace.destroy()
		self.espace = Frame(self, borderwidth=2)
		self.espace.pack()
		self.espaceInstancie = 1
	
		
if __name__ == "__main__":
	app = MainApp(None)
	h = GestionnaireHTTP()
	# lesTags = Tags(h)
	# lesFonctions = Fonctions(h, lesTags)
	# lesLiensTT = liensTT(h, lesTags)
	# lesDynasties = Dynasties(h)
	
	f = fichierData(1)
	lesTags = Tags(f)
	lesFonctions = Fonctions(f, lesTags)
	lesLiensTT = liensTT(f, lesTags)
	lesDynasties = Dynasties(f)
	
	# f = fichierData()
	# lesTags.ecritFichier(f)
	# lesFonctions.ecritFichier(f)
	# lesLiensTT.ecritFichier(f)
	# lesDynasties.ecritFichier(f)
	# f.ferme()
	
	app.mainloop()