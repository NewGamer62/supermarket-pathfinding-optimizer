# Formation : BUT 1ʳᵉ année | 2024-2025
# Ressource : SAE S2 - Algo et Graphes
# Professeur : M. Conoir
# Noms :  AMEDRO Louis (TPD)
#         HERBAUX Jules (TPD)
#         GAILLARD Noa (TPC)
#         MINNEBO Valentin (TPA)

# --------------- #
# --- Modules --- #
# --------------- #

import json, os, sys
from datetime import datetime, date

# --------------- #
# --- Classes --- #
# --------------- #

class Informations() :
    
    ''' Liste d'informations concernant un projet.
Ces informations sont :\n
    - nom : str -> nom du projet
    - auteur : str -> nom de l'auteur du projet
    - dateCreation : date -> date de création du projet
    - nomSupermarche : str -> nom du supermarché du projet
    - adresseSupermarche : str -> adresse du supermarché du projet\n
L'utilisateur peut :
    - Lire les informations d'un fichier JSON
    - Récupérer les information
    - Modifier les informations
    - Enregistrer les informations sous format JSON'''
    
    # --- Constructeur --- #
    
    def __init__(self, nomJSON : str = None) :
        
        '''Initialise les informations.
Si un fichier JSON est fourni, l'initialisation se fait avec les informations du fichier.
Sinon, elles prennent leurs valeurs par défaut :\n
    - "Projet sans Nom" pour le nom du projet
    - "Auteur Inconnu" pour le nom de l'auteur
    - La date actuelle pour la date de création
    - "Supermarché Inconnué pour le nom du supermarché
    - "Adresse Inconnue" pour l'adresse du supermarché'''
    
        # Gestion des exceptions
        assert(isinstance(nomJSON, (str|None))), "Le chemin du fichier à lire doit être une chaine de caractères ou ne doit pas avoir de valeur"
        
        # fichier JSON fourni : lecture fichier
        if (nomJSON) : self.lireFichier(nomJSON)
        
        # sinon : valeurs par défaut  
        else : self.setInfos("Projet sans Nom", "Auteur Inconnu", datetime.now().date(), "Supermarché Inconnu", "Adresse Inconnue")
          
        
        
    # --- Manipulation fichiers --- #
    
    def lireFichier(self, nomJSON : str) -> None :
        
        '''Récupère les informations contenues dans un fichier JSON\n
Paramètres :
    - nomJSON : str -> nom (ou chemin) du fichier JSON à lire'''

        assert(isinstance(nomJSON, str)), "Le chemin du fichier à lire doit être une chaine de caractères"
        assert(nomJSON[len(nomJSON) - 5:] == ".json"), "Le fichier à lire n'est pas un fichier JSON"
        assert(os.path.exists(nomJSON)), "Le fichier à lire n'existe pas"
        
        # Lecture fichier JSON
        with open(nomJSON, encoding = 'utf-8') as fichier : infosJSON = json.load(fichier)
        
        # Récupération informations
        self.setInfos(infosJSON['nom'], infosJSON['auteur'], datetime.strptime(infosJSON['date création'], '%Y-%m-%d').date(), infosJSON['nom supermarché'], infosJSON['adresse supermarché'])
    
    
    
    def ecrireFichier(self, nomJSON : str) -> None :
        
        '''Enregistre les informations sous format JSON\n
Paramètres :
    - nomJSON : str -> nom (ou chemin) du fichier JSON à enregistrer'''
    
        # --- Gestion exceptions --- #
        
        assert(isinstance(nomJSON, str)), "Le chemin du fichier à écrire doit être une chaine de caractères"
        assert(nomJSON[len(nomJSON) - 5:] == ".json"), "Le fichier à écrire n'est pas un fichier JSON"
    
        # --- Variables locales --- #
        
        infos : dict = self.getInfos() # Liste des informations de l'objet
        infos['date création'] = str(infos['date création']) # Conversion date création en chaine de caractères (pour écriture JSON)
        
        # --- Script --- #
        
        # Écriture fichier 
        with open(nomJSON, 'w', encoding = 'utf-8') as fichier : json.dump(infos, fichier, ensure_ascii = False)
               
    # --- Getters --- #
    
    def getNom(self) -> str :
        
        '''Retourne le nom du projet.'''
        
        return self.__nom
     
    def getAuteur(self) -> str :
        
        '''Retourne le nom de l'auteur du projet.'''
        
        return self.__auteur
    
    def getDateCreation(self) -> date :
        
        '''Retourne la date de création du projet.'''
        
        return self.__dateCreation
    
    def getNomSupermarche(self) -> str :
        
        '''Retourne le nom du supermarché du projet.'''
        
        return self.__nomSupermarche
    
    def getAdresseSupermarche(self) -> str :
        
        '''Retourne l'adresse du supermarché du projet.'''
        
        return self.__adresseSupermarche
    
    def getInfos(self) -> dict :
        
        ''' Retourne un dictionnaire contenant toutes les informations du projet.'''
        
        return {
            "nom" : self.getNom(), 
            "auteur" : self.getAuteur(), 
            "date création" : self.getDateCreation(),
            "nom supermarché" : self.getNomSupermarche(),
            "adresse supermarché" : self.getAdresseSupermarche()
            }
    
    # --- Setters --- #

    def setNom(self, nom : str) -> None :
        
        '''Modifie le nom du projet.'''
        
        assert(isinstance(nom, str)), "Le nom doit être une chaine de caractères"
        self.__nom = nom  
        
    def setAuteur(self, auteur : str) -> None :
        
        '''Modifie l'auteur du projet.'''
        
        assert(isinstance(auteur, str)), "Le nom de l'auteur doit être une chaine de caractères"
        self.__auteur = auteur
        
    def setDateCreation(self, dateCreation : date) -> None :
        
        '''Modifie la date de création du projet.'''
        
        assert(isinstance(dateCreation, date)), "La date de création doit être une date"
        self.__dateCreation = dateCreation
        
    def setNomSupermarche(self, nom : str) -> None :
        
        '''Modifie le nom du supermarché du projet.'''
        
        assert(isinstance(nom, str)), "Le nom du supermarché doit être une chaine de caractères"
        self.__nomSupermarche = nom
        
    def setAdresseSupermarche(self, adresse : str) -> None :
        
        '''Modifie l'adresse du supermarché du projet.'''
    
        assert(isinstance(adresse, str)), "L'adresse du supermarché doit être une chaine de caractères"
        self.__adresseSupermarche = adresse
        
    def setInfos(self, nom : str, auteur : str, dateCreation : date, nomSupermarche : str, adresseSupermarche : str) -> None :
        
        '''Modifie chacune des informations du projet.'''
        
        self.setNom(nom)
        self.setAuteur(auteur)
        self.setDateCreation(dateCreation)
        self.setNomSupermarche(nomSupermarche)
        self.setAdresseSupermarche(adresseSupermarche)
    
    # --- Affichage --- #
    
    def __str__(self) -> str :
        
        '''Retourne toutes les informations contenues dans l'objet sous forme de chaine de caractères.
Méthode appelée lorsque l'utilisateur veut afficher l'objet à l'aide de print.'''

        return "Projet nommé " + self.getNom() + ", crée par " + self.getAuteur() + " le " + str(self.getDateCreation()) + " et basé sur le supermarché " + self.getNomSupermarche() + " localisé à " + self.getAdresseSupermarche()
        
# ------------ #
# --- Main --- #
# ------------ #

# Test de la classe Informations
# Les tests se divisent en deux parties : les tests principaux et les tests d'exceptions
# Les tests principaux testent la classe dans des conditions normales de fonctionnement
# Les tests d'exceptions testent les cas où des erreurs sont rencontrées
# Par défaut, aucun test d'exception ne se lance : il faut entrer un numéro de 0 à 7 en argument dans le terminal pour en lancer un seul

if __name__ == "__main__" :
    
    # --- Tests principaux --- #
    
    # Initialisation d'informations sans fichier JSON
    infos1 : Informations = Informations()
    print("infos1 = ", infos1, "\n")
    
    # Récupération de toutes les infos avec getInfos = test de tous les getters
    print("infos1.getInfos() = ", infos1.getInfos(), "\n")
    
    # Modification de toutes les infos avec setInfos = test de tous les setters
    infos1.setInfos("infos1", "main", date(2025, 6, 1), "supermarcheTest", "adresseTest")
    print("infos1 = ", infos1, "\n")
    
    # Enregistrement de toutes les infos de infos1 sous format JSON
    infos1.ecrireFichier("test.json")
    
    # Initialisation d'informations avec fichier JSON = test de la méthode lireFichier
    infos2 : Informations = Informations("test.json")
    print("infos2 = ", infos1, "\n")
    
    # Affichage de tous les docstrings de la classe
    print("Informations :\n", Informations.__doc__, "\n")
    print("__init__ :\n", Informations.__init__.__doc__, "\n")
    print("lireFichier :\n", Informations.lireFichier.__doc__, "\n")
    print("ecrireFichier :\n", Informations.ecrireFichier.__doc__, "\n")
    print("getNom :\n", Informations.getNom.__doc__, "\n")
    print("getAuteur :\n", Informations.getAuteur.__doc__, "\n")
    print("getDateCreation :\n", Informations.getDateCreation.__doc__, "\n")
    print("getNomSupermarche :\n", Informations.getNomSupermarche.__doc__, "\n")
    print("getAdresseSupermarche :\n", Informations.getAdresseSupermarche.__doc__, "\n")
    print("getInfos :\n", Informations.getInfos.__doc__, "\n")
    print("setNom :\n", Informations.setNom.__doc__, "\n")
    print("setAuteur :\n", Informations.setAuteur.__doc__, "\n")
    print("setDateCreation :\n", Informations.setDateCreation.__doc__, "\n")
    print("setNomSupermarche :\n", Informations.setNomSupermarche.__doc__, "\n")
    print("setAdresseSupermarche :\n", Informations.setAdresseSupermarche.__doc__, "\n")
    print("setInfos :\n", Informations.setInfos.__doc__, "\n")
    print("__str__ :\n", Informations.__str__.__doc__, "\n")
    
    # --- Tests exceptions --- #
    
    if (len(sys.argv) >= 2) :
    
        if (sys.argv[1] == "0") : # 0 = lecture de fichier non JSON
            
            infos1.lireFichier("test.txt")
            
        elif (sys.argv[1] == "1") : # 1 = lecture de fichier inexistant
            
            infos1.lireFichier("test1.json")
            
        elif (sys.argv[1] == "2") : # 2 = écriture de fichier non JSON
            
            infos1.ecrireFichier("test.txt")
            
        elif (sys.argv[1] == "3") : # 3 = modification nom sans chaine de caractères
            
            infos1.setNom(1)
            
        elif (sys.argv[1] == "4") : # 4 = modification auteur sans chaine de caractères
            
            infos1.setAuteur(1)
            
        elif (sys.argv[1] == "5") : # 5 = modification date création sans date
            
            infos1.setDateCreation(1)
            
        elif (sys.argv[1] == "6") : # 6 = modification nom supermarché sans chaine de caractères
        
            infos1.setNomSupermarche(1)
            
        elif (sys.argv[1] == "7") : # 7 = modification adresse sans chaine de caractères
            
            infos1.setAdresseSupermarche(1)