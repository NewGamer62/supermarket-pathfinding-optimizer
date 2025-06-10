# --------------- #
# --- Modules --- #
# --------------- #

from datetime import datetime, date

# --------------- #
# --- Classes --- #
# --------------- #

class Informations() :
    
    # --- Constructeur --- #
    
    def __init__(self) :
        
        self.__nom : str = "Projet sans Nom"
        self.__auteur : str = "Auteur Inconnu"
        self.__dateCreation : date = datetime.now().date()
        
        self.__nomSupermarche : str = "Supermarché Inconnu"
        self.__adresseSupermarche : str = "Adresse Inconnue"
        
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
    
    # --- Setters --- #

    def setNom(self, nom : str) -> None :
        
        '''Modifie le nom du projet.\n
Paramètres :
    - nom : str -> Nouveau nom du projet\n
Contraintes :
    - Le nouveau nom doit être une chaine de caractères'''
    
        assert(isinstance(nom, str)), "Le nom doit être une chaine de caractères"
        self.__nom = nom
        
    def setAuteur(self, auteur : str) -> None :
        
        '''Modifie l'auteur du projet.\n
Paramètres :
    - auteur : str -> Nouvel auteur du projet\n
Contraintes :
    - Le nom du nouvel auteur doit être une chaine de caractères'''
    
        assert(isinstance(auteur, str)), "Le nom de l'auteur doit être une chaine de caractères"
        self.__auteur = auteur
        
    def setDateCreation(self, dateCreation : date) -> None :
        
        '''Modifie la date de création du projet.\n
Paramètres :
    - dateCreation : date -> Nouvelle date de création du projet\n
Contraintes :
    - La nouvelle date de création doit être une date'''
    
        assert(isinstance(dateCreation, date)), "La date de création doit être une date"
        self.__dateCreation = dateCreation
        
    def setNomSupermarche(self, nom : str) -> None :
        
        '''Modifie le nom du supermarché du projet.\n
Paramètres :
    - nom : str -> Nouveau nom du supermarché du projet\n
Contraintes :
    - Le nouveau nom du supermarché doit être une chaine de caractères'''
    
        assert(isinstance(nom, str)), "Le nom du supermarché doit être une chaine de caractères"
        self.__nomSupermarche = nom
        
    def setAdresseSupermarche(self, adresse : str) -> None :
        
        '''Modifie l'adresse du supermarché du projet.\n
Paramètres :
    - adresse : str -> Nouvelle adresse du supermarché du projet\n
Contraintes :
    - La nouvelle adresse du supermarché doit être une chaine de caractères'''
    
        assert(isinstance(adresse, str)), "L'adresse du supermarché doit être une chaine de caractères"
        self.__nomSupermarche = adresse
    
    # --- Affichage --- #
    
    def __str__(self) -> str :
        
        '''Retourne toutes les informations contenues dans l'objet sous forme de chaine de caractères.
Méthode appelée lorsque l'utilisateur veut afficher l'objet à l'aide de print.'''

        return "Projet nommé " + self.__nom + ", crée par " + self.__auteur + " le " + str(self.__dateCreation) + " et basé sur le supermarché " + self.__nomSupermarche + " localisé à " + self.__adresseSupermarche
        
# ------------ #
# --- Main --- #
# ------------ #

if __name__ == "__main__" :
    
    a = Informations()
    print(a.getDateCreation())
    a.setDateCreation(date(2025, 5, 5))
    print(a.getDateCreation())