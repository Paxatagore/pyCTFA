import urllib.request, json
from tkinter import *
import pickle
from getpass import getpass

class GestionnaireHTTP():
	"""gestionnaire de connexion au serveur"""
	
	def __init__(self):
		"""init"""
		self.opener = self.manager()
		
	def manager(self):
		"""Créer un password manager"""
		password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
		top_level_url = "www.steppe.fr"
		login = input("Login : ")
		pwd = getpass("Password : ")
		password_mgr.add_password(None, top_level_url, login, pwd)
		handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
		return urllib.request.build_opener(handler)
		
	def envoieURL(self, url, data = "", method='POST'):
		"""Envoie une URL et renvoie le résultat décodé"""
		if data != "":
			#mode POST
			data = data.encode('ascii')
			r = self.opener.open("https://www.steppe.fr/matthieu/CTFA/" + url, data)
			r = r.read()
			r = r.decode("utf8")
			return json.loads(r)
		else:
			r = self.opener.open("https://www.steppe.fr/matthieu/CTFA/" + url)
			r = r.read()
			r = r.decode("utf8")
			return json.loads(r)


#fonctions de formulaire (à écrire en mode Tkinter)

class Form():
	"""fonction de gestion d'un formulaire console"""
	"""gère un objet provisoire (dictionnaire), auquel on ajoute au fur et à mesure les valeurs obtenues"""
	
	def __init__(self, typeObjet, objet):
		"""instancie un formulaire console"""
		self.objetprovisoire = {}
		self.objet = objet
		self.objetprovisoire["num"] = objet["num"]
		self.objetprovisoire["objet"] = typeObjet
		
	def Hidden(self, parametres):
		"""Ajoute des paramètres cachés"""
		for cle in parametres:
			self.objetprovisoire[cle]= parametres[cle]
		
	def Input(self, nom, champ = ""):
		"""identique à un champ input"""
		if champ == "":
			champ = nom
		if not(champ in self.objet):
			self.objet[champ] = ""
		provisoire = input(nom + " [" + self.objet[champ] + "] :")
		if provisoire:
			self.objetprovisoire[champ] = provisoire
		else:
			self.objetprovisoire[champ] = self.objet[champ]
		
	def InputMultiple(self, nom, champ="", ensemble=""):
		"""identique à un champs input permettant d'entrer plusieurs valeurs successives et/ou d'en retirer"""
		if champ == "":
			champ = nom
		if not(champ in self.objet):
			self.objet[champ] = ""
		print (nom + " : " + ", ".join(ensemble))
		provisoire = list(ensemble)	
		add = -1
		while add != "":
			add = input("Ajout d'un élément (laisser vide pour supprimer, -elt pour supprimer un élément : ")
			if (len(add) > 0):
				if  (add[0] == "-"):
					#il s'agit en fait de supprimer un élément
					eltaSupprier = add[1:]
					#on cherche d'abord si l'élément existe en tant que tel
					if eltaSupprier in provisoire:
						#il existe
						provisoire.remove(eltaSupprier)
						print( "Je supprime " + eltaSupprier + " de la liste")
					#chercher à défaut l'élément le plus approchant
				else:
					#on ajoute l'élément
					provisoire.append(add)
		print("Après modifications éventuelles, la liste est : ", ", ".join(provisoire))
		self.objetprovisoire[champ] = provisoire
		return provisoire
	
	def Radio(self, nom, champ, ensemble):
		"""identique à un choix radio (un seul choix parmi une liste)"""
		if champ == "":
			champ = nom
		if not(champ in self.objet):
			self.objet[champ] = 0
		rt = input(nom + " : " + ensemble[self.objet[champ]] + " (O/n) ? ")
		if (rt.lower() != "o" and rt != ""):
			c = 0
			for n in ensemble:
				print (str(c) + " - " + n)
				c += 1
			rt = -1 
			while rt < 0 or rt > (len(ensemble)-1):
				rt = input(nom + " : ")
				if (rt != ""):
					self.objetprovisoire[champ] = int(rt)
					print( "Vous avez choisi : " + ensemble[self.objetprovisoire[champ]])
					return self.objetprovisoire[champ]
		#sinon (validation du choix initial ou choix invalide dans la liste)
		self.objetprovisoire[champ] = self.objet[champ]
		
	def Send(self):
		"""envoie le formulaire"""
		data = urllib.parse.urlencode(self.objetprovisoire)
		print(data)
		self.objet = http('REST/index.php', data)
		return self.objet

class fichierData():
	"""gère le fichier de données (data.db), qui contient une sauvegarde locale des tags, liensTT, fonctions et dynasties"""

	def __init__(self, mode=0):
		"""ouvre le fichier de data en lecture ou écriture (mode 0/1)"""
		if mode==0:
			self.fichier = open("data.db", 'wb')
		else:
			self.fichier = open("data.db", 'rb')
		
	def ecritObjet(self, o):
		"""écrit un objet dans le fichier de data"""
		return pickle.dump(o, self.fichier)
	
	def litObjet(self):
		"""lit le prochain objet qui doit venir"""
		return pickle.load(self.fichier)
	
	def ferme(self):
		"""ferme le fichier de data"""
		self.fichier.close()
		
if __name__ == '__main__':
	"""à écrire"""