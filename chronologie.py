#""" main.py """
from connexion import *
from tkinter import *
import tkinter.font

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
			
	def __handlerAfficheElement__(self, o):
		self.afficheFormulaire(o)
			
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
	
	def afficheFormulaire(self, o, master=None):
		"""affiche le formulaire sur l'objet o"""
		master = app
		if (o["num"] == 0):
			self.f = formulaire(o, "Ajouter un " + self.objetNom, self, master)
		else:
			self.f = formulaire(o, "Modifier un " + self.objetNom, self, master)
		self.objetatraiter = o
		self.subform()
		self.f.bouton()
	
	def envoyerFormulaire(self):
		"""récupération du formulaire"""
		print("Récupération du formulaire")
		self.subform2()
		
class formulaire(tkinter.Toplevel):
	"""gestion d'un formulaire en tkinter"""
	
	def __init__(self, o, titre, objet, master=None):
		self.o = o
		self.objet = objet
		tkinter.Toplevel.__init__(self, master)
		fontLegende = tkinter.font.Font(weight="bold")
		Label(self, text = titre, font=fontLegende).grid(row=0, column=0, columnspan=2, padx=2, pady=2)
		Label(self, text="Num").grid(row=1, column=0,  sticky=W, padx=2, pady=2)
		Label(self, text=o["num"]).grid(row=1, column=1,  sticky=W, padx=2, pady=2)
		self.compteur = 2
	
	def ajouteRubrique(self, rubrique):
		Label(self, text = rubrique).grid(row=self.compteur, column=0, columnspan=2, padx=2, pady=2)
		self.compteur += 1
		
	def input(self, nom, champ):
		Label(self, text=nom).grid(row=self.compteur, column=0,  sticky=W, padx=2, pady=2)
		texte = tkinter.StringVar()
		if not(champ in self.o):
			self.o[champ] = ""
		texte.set(self.o[champ])
		Entry(self, textvariable=texte).grid(row=self.compteur, column=1,  sticky=W, padx=2, pady=2)
		self.compteur += 1
		return texte
	
	def bouton(self):
		Button(self, text="Envoyer", command=self.objet.envoyerFormulaire).grid(row=self.compteur, column=0,  sticky=E, padx=2, pady=2)
		Button(self, text="Annuler", command=self.quitter).grid(row=self.compteur, column=1,  sticky=E, padx=2, pady=2)
		self.compteur += 1
		return True
		
	def listbox(self, nom, liste):
		Label(self, text=nom).grid(row=self.compteur, column=0,  sticky=W, padx=2, pady=2)
		listvariable = tkinter.StringVar()
		listvariable.set(" ".join(liste))
		Listbox(self, height=1, listvariable=listvariable).grid(row=self.compteur, column=1,  sticky=W, padx=2, pady=2)
		self.compteur += 1
		return listvariable
	
	def quitter(self):
		"""termine le formulaire"""
		self.destroy()

class Tags(CTFAObjet):
	"""la gestion des tags"""
	objetNom = "tag"
	
	natures = ("Territoire", "Ville", "Régime", "Peuple", "Dynastie", "Musée", "Continent", "Etat", "Concepts", "Organisation", "Courant de pensée", "Mer", "Ile", "Astre", "Etat fédéré", "Ville et territoire")	#nature de tags
	legende = ("Drapeau", "Nom", "Nature", "Pères", "Fils")
	
	#les données sont stockées dans donnees, qui est une liste
	#chaque élément de la liste est un dictionnaire

	#commandes de manipulation collective
	def menu(self):
		"""A EFFACER"""
		print("Menu tags")
		fc = (exit, self.cherche, self.ajoute, self.afficheParNature)
		print("1 - Rechercher un tag")
		print("2 - Ajouter un nouveau tag")
		print("3 - Afficher par nature")
		print("0 - Retour en arrière")
		choix = input("Quel est votre choix ? ")
		choix = int(choix)
		fc[choix]()
	
	def cherche(self):
		"""A EFFACER"""
		"""chercher un tag"""
		name = input("Entrez le nom du tag à rechercher : ")
		for at in self.donnees:
			if at["nom"] == name:
				return self.affiche(at)
		r = re.compile(name)
		listeChoix = []
		for t in self.donnees:
			if re.search(r, t["nom"]):
				listeChoix.append(t)
		if len(listeChoix)>0:
			listeChoix.sort(key = lambda x:x["nom"])
			compteur = 1
			for c in listeChoix:
				print(compteur, " : ", c["nom"])
				compteur += 1
			choix = int(input("Quel tag voulez vous afficher ?"))
			self.affiche(listeChoix[choix-1])
		return False
		
	def ajoute(self):
		"""A EFFACER"""
		self.form(0)
		
	def afficheParNature(self):
		"""A EFFACER"""
		print("Affichage des tags par nature")
		lesChoix = [0]
		for i, n in enumerate(self.natures):
			nombreTags = len([x for x in self.donnees if x["nature"] == i])
			print(i, " - ", n, " (", nombreTags, " tags)")
		print("0 - Retour")	
		choix = int(input("Quel est votre choix ?"))
		if choix == 0:
			return false
		self.affiche()
		
	def corrigeUne(self, t):
		"""corrige un tag"""
		t["num"] = int(t["num"])		#le numéro est converti de chaine en entier
		t["nature"] = int(t["nature"])	#idem pour nature
		t["natureString"] = self.natures[t["nature"]]	#natureString est la valeur de chaîne de nature
		
		def tagSplit(v):
			"""transforme une liste d'éléments contenus dans une chaîne séparés par une virgule en un tableau"""
			if (v  == ""):
				return []
			else:
				return v.split(",")
								
		t["motscles"] = tagSplit(t["motscles"])
		t["adjectifs"] = tagSplit(t["adjectifs"])
		#prépare deux tableaux vide pour recevoir les liensTT (pères / fils)
		t["listefils"] = []
		t["listeperes"] = []
		
					
	def affiche(self, t):
		
		"""A EFFACER"""
		t = self.get(t)
		if t == False:
			return False
		print ("Affichage du tag #" + str(t["num"]))
		print ("Nom : " + t["nom"])
		print ("Autres noms : " + t["autrenom"])
		print ("URL : " + t["url"])
		print ("Drapeau : " + t["drapeau"])
		print ("Nature : " + t["natureString"])
		print ("Couleur : " + t["couleur"])
		print ("Mots clés : " + ", ".join(t["motscles"]))
		print ("Adjectifs : " + ", ".join(t["adjectifs"]))
		print ("Designation : " + t["designation"])
		p = [self.getNom(x) for x in t["peres"]]
		print ("Pères : " + (", ").join(p))
		f = [self.getNom(x) for x in t["fils"]]
		print ("Fils : " + (", ").join(f))
		print ("Occurences : " + t["occurence"])
		print ("Coordonnées : " + t["latitude"] + " - " + t["longitude"])
		
	def afficheUn(self, t, w, l):
		"""affiche un tag"""
		Label(w, text=t["drapeau"]).grid(row=l, column=0,  sticky=W, padx=2, pady=2)
		def handler(evt, self=self, o=t):
			return self.__handlerAfficheElement__(o)
		lab = Label(w, text=t["nom"])
		lab.bind("<Button-1>", handler)
		lab.grid(row=l, column=1,  sticky=W, padx=2, pady=2)
		Label(w, text=t["natureString"]).grid(row=l, column=2,  sticky=W, padx=2, pady=2)
		p = [self.getNom(x) for x in t["listeperes"]]
		peres = (", ").join(p)
		Label(w, text=peres[:34], width = 35).grid(row=l, column=3,  sticky=W, padx=2, pady=2)
		f = [self.getNom(x) for x in t["listefils"]]
		fils = (", ").join(f)
		Label(w, text=fils[:34], width = 35).grid(row=l, column=4,  sticky=W, padx=2, pady=2)
	
	#gestion des données (à placer dans CTFAObjet ?)
	
	def get(self, t):
		"""obtient un t (permet de passer indifferemment un num (en int ou en str) ou directement un tag (dictionnaire) """
		if isinstance(t, str):
			t = int(t)
		if isinstance(t, int):
			#t est un id => on recherche à quel tag cela correspond
			t = self.getById(t)
			if not t:
				print ("Ce tag n'existe pas.")
				return False
		if isinstance(t, dict):
			return t
			
	def getNom(self, t):
		"""obtient le nom du tag t"""
		t = self.get(t)
		if t == False:
			return ""
		else:
			return t["nom"]
				
	def getById(self, t):
		"""recherche un tag par son numéro"""
		t = int(t)
		for at in self.donnees:
			if at["num"] == t:
				return at
		return False
		
	def setById(self, num, t):
		"""recherche un tag par son numéro et le remplace par t (un dictionnaire)"""
		for at in self.donnees:
			if at["num"] == num:
				at = t
				return at 
		return False
	
	def form(self, t = 0):
		"""formulaire texte"""
		"""à remplacer par la version tk"""
		t = self.get(t)
		if t == False:
			t = {"num":0}
		prov = connexion.Form("tag", t)
		#partie formulaire
		prov.Input("Nom", "nom")
		prov.Input("URL", "url")
		prov.Input("Drapeau", "drapeau")
		prov.Input("Mots clés", "motscles")
		prov.Input("Autres noms", "autrenom")
		prov.Input("Adjectifs", "adjectifs")
		prov.Radio("Nature", "nature", self.natures)
		prov.Input("Latitude", "latitude")
		prov.Input("longitude", "longitude")
		tm = prov.Send()
		if t["num"] > 0:
			self.setById(t["num"], tm["tag"])
			print("Le changement a bien été enregistré.")
			return True
		else:
			lesTags.donnees.append(tm["tag"])
			print("Le nouvel enregistrement a bien été ajouté (#", tm["num"],")")
			return True
	
	def subform(self):
		self.f.ajouteRubrique("Description")
		self.fnom = self.f.input("Nom", "nom")
		self.furl = self.f.input("URL", "url")
		self.fdrapeau = self.f.input("Drapeau", "drapeau")
		self.fnature = self.f.listbox("nature", self.natures)
	# f.ligne("Nature", f.selectTableauSimple("nature", CTFA.typeTags)) ;
	
	def subform2(self):
		"""traitement du formulaire"""
		#rappel : objet à traiter : self.objetatraiter
		#formulaire : self.f
		print("Le nom est désormais ", self.fnom.get())
		print("L'url est désormais ", self.furl.get())
		print("Le drapeau est désormais", self.fdrapeau.get())
	
class liensTT(CTFAObjet):
	"""liensTT"""
	objetNom = "lientt"
	
	def __init__(self, h, mode, tags):
		self.tags = tags
		CTFAObjet.__init__(self, h, mode)
		
	
	def corrigeUne(self, lien):
		"""ajoute le lien dans les fils/père des tags"""
		tp = self.tags.getById(lien["tag1"])
		if tp:
			tp["listefils"].append(lien["tag2"])
		tf = self.tags.getById(lien["tag2"])
		if tf:
			tf["listeperes"].append(lien["tag1"])
		
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
		Label(w, text=t["nom"]).grid(row=l, column=0, sticky=W, padx=2, pady=2)
		Label(w, text=t["occurence"]).grid(row=l, column=1, sticky=W, padx=2, pady=2)
		Label(w, text=t["tag"]).grid(row=l, column=2, sticky=W, padx=2, pady=2)
		
class Dynasties(CTFAObjet):
	"""la gestion des dynasties"""
	objetNom = "dynastie"
	legende = ("Armes", "Nom", "Couleur", "Personnes")
	
	def afficheUn(self, t, w, l):
		"""affiche une dynastie"""
		Label(w, text=t["armoirie"]).grid(row=l, column=0,  sticky=W, padx=2, pady=2)
		Label(w, text=t["nom"]).grid(row=l, column=1,  sticky=W, padx=2, pady=2)
		Label(w, text=t["couleur"],  foreground='#'+t["couleur"]).grid(row=l, column=2,  sticky=W, padx=2, pady=2)
		Label(w, text=t["occurence"]).grid(row=l, column=3,  sticky=W, padx=2, pady=2)
				
if __name__ == "__main__":
	h = GestionnaireHTTP()
	app = MainApp(None)
	app.mainloop()