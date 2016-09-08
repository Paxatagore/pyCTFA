from CTFAObjet import CTFAObjet
from tkinter import *



class Tags(CTFAObjet):
	"""la gestion des tags"""
	objetNom = "tag"
	
	natures = ("Territoire", "Ville", "Régime", "Peuple", "Dynastie", "Musée", "Continent", "Etat", "Concepts", "Organisation", "Courant de pensée", "Mer", "Ile", "Astre", "Etat fédéré", "Ville et territoire")
	legende = ("Drapeau", "Nom", "Nature", "Pères", "Fils")
	
	#les données sont stockées dans donnees, qui est une liste
	#chaque élément de la liste est un dictionnaire

	#commandes de manipulation collective
	def menu(self):
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
		self.form(0)
		
	def afficheParNature(self):
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
		t["num"] = int(t["num"])
		t["nature"] = int(t["nature"])
		t["natureString"] = self.natures[t["nature"]]	#la nature
		
		def tagSplit(v):
			if (v  == ""):
				return []
			else:
				return v.split(",")
								
		#t["peres"] = tagSplitConvertit(t["peres"])
		#t["fils"] = tagSplitConvertit(t["fils"])
		t["motscles"] = tagSplit(t["motscles"])
		t["adjectifs"] = tagSplit(t["adjectifs"])
		t["listefils"] = []
		t["listeperes"] = []
		
					
	def affiche(self, t):
		"""affiche un tag"""
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
		Label(w, text=t["drapeau"]).grid(row=l, column=0,  sticky=W, padx=2, pady=2)
		Label(w, text=t["nom"]).grid(row=l, column=1,  sticky=W, padx=2, pady=2)
		Label(w, text=t["natureString"]).grid(row=l, column=2,  sticky=W, padx=2, pady=2)
		p = [self.getNom(x) for x in t["listeperes"]]
		peres = (", ").join(p)
		Label(w, text=peres[:34], width = 35).grid(row=l, column=3,  sticky=W, padx=2, pady=2)
		f = [self.getNom(x) for x in t["listefils"]]
		fils = (", ").join(f)
		Label(w, text=fils[:34], width = 35).grid(row=l, column=4,  sticky=W, padx=2, pady=2)
		
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
	
	# def Legende(self, widget):
		# l1 = Label(widget, text="Drapeau")
		# l1.grid(row=0, column=0)
		# l2 = Label(widget, text="Nom")
		# l2.grid(row=0, column=1)
		
		
class liensTT(CTFAObjet):
	objetNom = "lientt"
	
	def __init__(self, h, tags):
		self.tags = tags
		CTFAObjet.__init__(self, h)
		
	
	def corrigeUne(self, lien):
		#ajoute le lien dans les fils/père des tags
		tp = self.tags.getById(lien["tag1"])
		if tp:
			tp["listefils"].append(lien["tag2"])
		tf = self.tags.getById(lien["tag2"])
		if tf:
			tf["listeperes"].append(lien["tag1"])
		
	
if __name__ == '__main__':
	from connexion import *
	import re
	http = GestionnaireHTTP()
	lesTags = Tags()
	lesLiensTT = liensTT()
	lesTags.menu()
	