from tkinter import *
import tkinter.font

class CTFAObjet():
	"""classe mère des objets qui pilotent des données"""
	objetNom = ""
	
	#les données sont stockées dans donnees, qui est une liste
	#chaque élément de la liste est un dictionnaire

	def __init__(self, v, mode='f'):
		"""fonction d'initialisation
		v est le vecteur : un fichier ou un gestionnaireHTML
		mode est le mode : f pour fichier, s pour serveur"""
		if mode=='f':
			#fichier
			self.chargeFichier(v)
		else:
			#serveur
			self.chargeServeur(v)
		self.charge = 1
				
	def chargeServeur(self, h):
		"""charge les données depuis le serveur, en utilisant l'objet h"""
		self.h = h
		d = self.h.envoieURL("REST/index.php?objet=" + self.objetNom)
		self.donnees = d[self.objetNom]
		self.nombre = len(self.donnees)
		print("Téléchargement des " + str(self.nombre) + " " + self.objetNom + "s .... OK.")
		for t in self.donnees:
			self.corrigeUne(t)		
	
	def chargeFichier(self, f):
		"""charge les données depuis le fichier f"""
		self.donnees = f.litObjet()
		self.nombre = len(self.donnees)
		print("Chargement des " + str(self.nombre) + " " + self.objetNom + "s .... OK.")
		#ici, on ne fait pas le self.corrigeUne sur chaque donnée, puisqu'il a déjà été fait une fois pour toute
	
	def corrigeUne(self, t):
		"""corrige une donnee"""
		return True
	
	def trie(self):
		"""tri les données par ordre alphabétique de nom"""
		self.donnees.sort(key = lambda x:x["nom"].lower())
		pl = ""
		self.listePL = []
		for i, d in enumerate(self.donnees):
			if (d["nom"][0].lower() != pl.lower()):
				pl = d["nom"][0].upper()
				self.listePL.append((i, pl))
		
	#fonctions d'affichage
	
	def afficherTout(self, tke, de=0, a=15):
		"""affiche la liste des éléments"""
		self.trie()
		self.tke = tke
		self.de = de
		self.a = a
		#on vide l'affichage
		lw = self.tke.grid_slaves()
		for w in lw:
			w.destroy()
		self.Legende(tke)
		compteur = 1
		for t in self.donnees[de:a]:
			self.afficheUn(t, tke, compteur)
			compteur += 1
		
		self.boutonsGaucheDroite(tke,de, a)
		
	def Legende(self, tke):
		"""affiche la légende (fonction destinée à être surchargée si besoin """
		compteur = 0
		fontLegende = tkinter.font.Font(weight="bold")
		for t in self.legende:
			Label(tke, text = t, font=fontLegende).grid(row=0, column=compteur, sticky=W, padx=2, pady=2)
			compteur += 1
			
	def boutonsGaucheDroite(self, tke,de, a):
		"""affiche un bouton de gauche et de droite et les boutons pour naviguer dans la liste"""
		f = Frame(self.tke)
		f.grid(row=17, column=0, columnspan=len(self.legende), sticky=N+S)
		boutong = Button(f, text="< < <", command = self.afficherPrecedent)
		boutong.pack(side=LEFT)
		for t in self.listePL:
			def handler(self=self, i=t[0]):
				return self.__handler__(i)
			Button(f, text=t[1], command = handler).pack(side=LEFT)
		
		boutond = Button(f, text="> > >", command = self.afficherSuivant)
		boutond.pack(side=LEFT)
		
	def __handler__(self, goto):
		"""handler de la fonction précédente"""
		self.de = goto
		self.a = goto+15
		self.afficherTout(self.tke, self.de, self.a)
	
	def afficherPrecedent(self):
		"""affiche la page de liste précédente"""
		if self.de > 0:
			self.de = self.de - 15
			if self.de<0:
				self.de = 0
			self.a = self.de + 15
			self.afficherTout(self.tke, self.de, self.a)
		
	def afficherSuivant(self):
		"""affiche la page de liste suivante"""
		print(self.a)
		if self.de < len(self.donnees):
			self.de = self.de + 15
			self.a = self.de + 15
			self.afficherTout(self.tke, self.de, self.a)
	
	#fonction de gestion des I/O vers le fichier / serveur
	
	def ecritFichier(self, fichier):
		"""sauvegarde les données dans le fichier f"""
		return fichier.ecritObjet(self.donnees)

		
if __name__ == '__main__':
	#à écrire