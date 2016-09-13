"""gestion des données stables"""

from CTFAObjet import CTFAObjet
from tkinter import *

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
		Label(w, text=t["nom"]).grid(row=l, column=1,  sticky=W, padx=2, pady=2)
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
				
		
if __name__ == '__main__':
	"""à écrire"""
	