#""" main.py """
from connexion import *
from CTFAObjet import *
from donnees import *
from tkinter import *

class MainApp(Tk):
	
	def __init__(self, parent):
		"""initialisation de l'application"""
		#partie données
		f = fichierData(1)
		self.lesTags = Tags(f)
		self.lesFonctions = Fonctions(f, 'f', self.lesTags)
		self.lesLiensTT = liensTT(f, 'f', self.lesTags)
		self.lesDynasties = Dynasties(f)
	
		
		#partie fenêtres
		Tk.__init__(self, parent)
		self.parent = parent
		self.title("PyChronologie")
		self['bg'] = 'white'
		self.menus()
		self.espaceInstancie = 0
		
	def rechargeDepuisServeur(self):
		"""actualise les tags, liensTT, dynasties et fonction du serveur vers le fichier data"""
		self.lesTags = Tags(h, 's')
		self.lesFonctions = Fonctions(h, 's', self.lesTags)
		self.lesLiensTT = liensTT(h, 's', self.lesTags)
		self.lesDynasties = Dynasties(h, 's')
		print( "Téléchargement des données... ok")
		f = fichierData()
		self.lesTags.ecritFichier(f)
		self.lesFonctions.ecritFichier(f)
		self.lesLiensTT.ecritFichier(f)
		self.lesDynasties.ecritFichier(f)
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
		self.lesTags.afficherTout(self.espace)
		
	def afficheFonctions(self):
		self.creeEspace()
		self.lesFonctions.afficherTout(self.espace)
		
	def afficheDynasties(self):
		self.creeEspace()
		self.lesDynasties.afficherTout(self.espace)
	
	#commandes d'ajout
	
	def ajouteTags(self):
		tagvide = {"num":0}
		self.lesTags.afficheFormulaire(tagvide, self)
		
		
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