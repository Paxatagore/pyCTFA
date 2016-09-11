#""" main.py """


from connexion import *
from CTFAObjet import *
from fonctions import *
from tags import *
from dynasties import *
from tkinter import *

class MainApp(Tk):
	
	def __init__(self, parent):
		"""initialisation de l'application"""
		#partie données
		f = fichierData(1)
		lesTags = Tags(f)
		lesFonctions = Fonctions(f, 'f', lesTags)
		lesLiensTT = liensTT(f, 'f', lesTags)
		lesDynasties = Dynasties(f)
	
		
		#partie fenêtres
		Tk.__init__(self, parent)
		self.parent = parent
		self.title("PyChronologie")
		self['bg'] = 'white'
		self.menus()
		self.espaceInstancie = 0
		
	def rechargeDepuisServeur(self):
		"""actualise les tags, liensTT, dynasties et fonction du serveur vers le fichier data"""
		lesTags = Tags(h, 's')
		lesFonctions = Fonctions(h, 's', lesTags)
		lesLiensTT = liensTT(h, 's', lesTags)
		lesDynasties = Dynasties(h, 's')
		print( "Téléchargement des données... ok")
		f = fichierData()
		lesTags.ecritFichier(f)
		lesFonctions.ecritFichier(f)
		lesLiensTT.ecritFichier(f)
		lesDynasties.ecritFichier(f)
		f.ferme()
		print("écriture des données...ok")
	
	#partie menus
	
	def menus(self):
		"""instancie les menus"""
		menu = Menu(self)
		menu1 = Menu(menu, tearoff=0)
		menu1.add_command(label="Tags", command = self.afficheTags)
		menu1.add_command(label="Fonctions", command = self.afficheFonctions)
		menu1.add_command(label="Dynasties", command = self.afficheDynasties)
		menu1.add_command(label="Actualiser", command=self.rechargeDepuisServeur)
		menu.add_cascade(label="Afficher", menu=menu1)
		menu2 = Menu(menu, tearoff=0)
		menu2.add_command(label="Tags", command = self.ajouteTags)
		menu2.add_command(label="Fonctions", command = self.ajouteFonctions)
		menu2.add_command(label="Dynasties", command = self.ajouteDynasties)
		menu.add_cascade(label="Ajouter", menu=menu2)
		self.config(menu=menu)
	
	#commandes d'affichage
	
	def afficheTags(self):
		self.creeEspace()
		lesTags.afficherTout(self.espace)
		
	def afficheFonctions(self):
		self.creeEspace()
		lesFonctions.afficherTout(self.espace)
		
	def afficheDynasties(self):
		self.creeEspace()
		lesDynasties.afficherTout(self.espace)
	
	#commandes d'ajout
	
	def ajouteTags(self):
		pass
		
	def ajouteFonctions(self):
		pass
		
	def ajouteDynasties(self):
		pass
	
	#gestion de l'affichage
	
	def creeEspace(self):
		"""crée un frame pour l'affichage "principal" """
		if self.espaceInstancie > 0:
			self.espace.destroy()
		self.espace = Frame(self, borderwidth=2)
		self.espace.pack()
		self.espaceInstancie = 1
	
		
if __name__ == "__main__":
	h = GestionnaireHTTP()
	app = MainApp(None)
	app.mainloop()