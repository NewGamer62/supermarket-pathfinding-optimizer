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

import os, json
from shutil import copy

# --------------- #
# --- Classes --- #
# --------------- #

class Supermarche() :
    
    # --- Constructeur --- #
    
    # !!! NON FINI !!!
    
    def __init__(self, nomDossier : str = None) :
        
        self.__plan = "plan.jpg"
        self.__listeProduits : list[str] = []
        self.__quadrillage : list[list[list[str]]] = [[[] for j in range (10)] for i in range(10)] ; self.__quadrillage[0][0] = ["entrée"]
        
    # !!! NON FINI !!!
        
    # --- Manipulation fichiers --- #
    
    def lireDossier(self, nomDossier : str) -> None :
        
        '''Récupère toutes les informations contenues dans un dossier de supermarché.\n
Paramètres :
    - nomDossier : str -> nom du dossier à créer'''
        
        # Gestion des exceptions
        assert(isinstance(nomDossier, str)), "Le chemin du dossier à lire doit être une chaine de caractères"
        assert(os.path.exists(nomDossier)), "Le dossier à lire n'existe pas"
        
        # Récuperation des données
        self.setPlan(nomDossier + "/plan.jpg")
        self.lireListeProduits(nomDossier + "/liste_produits.json")
        self.lireQuadrillage(nomDossier + "/quadrillage.json")
        
        
    
    def ecrireDossier(self, nomDossier : str) -> None :
        
        '''Crée un dossier comportant toutes les informations du supermarché (plan utilisé, liste de produits et quadrillage)\n
Paramètres :
    - nomDossier : str -> nom du dossier à créer'''
        
        # Gestion des exceptions
        assert(isinstance(nomDossier, str)), "Le chemin du dossier à écrire doit être une chaine de caractères"
        
        # Création du dossier (s'il n'existe pas)
        if (not os.path.exists(nomDossier)) : os.makedirs(nomDossier)
        
        # Écriture des fichiers
        copy(self.getPlan(), nomDossier + "/plan.jpg")
        self.ecrireListeProduits(nomDossier + "/liste_produits.json")
        self.ecrireQuadrillage(nomDossier + "/quadrillage.json")
    
    # --- Manipulation plan --- #
    
    def getPlan(self) -> str :
        
        '''Retourne le plan de supermarché utilisé'''
        
        return self.__plan
    
    def setPlan(self, planChemin : str) -> None :
        
        '''Modifie le plan de supermarché utilisé'''
        
        assert(isinstance(planChemin, str)), "Le chemin du plan à utiliser doit être une chaine de caractères"
        assert(os.path.exists(planChemin)), "Le plan à utiliser n'existe pas"
        self.__plan = planChemin
        
    # --- Manipulation liste produits --- #
    
    def getListeProduits(self) -> list[str] :
        
        '''Retourne la liste de produits utilisée par le supermarché'''
        
        return self.__listeProduits
    
    
    
    def lireListeProduits(self, nomJSON : str) -> None :
        
        '''Récupère la liste de produits contenue dans un fichier JSON\n
Paramètres :
    - nomJSON : str -> nom (ou chemin) du fichier JSON à lire'''
        
        assert(isinstance(nomJSON, str)), "Le chemin du fichier à lire doit être une chaine de caractères"
        assert(nomJSON[len(nomJSON) - 5:] == ".json"), "Le fichier à lire n'est pas un fichier JSON"
        assert(os.path.exists(nomJSON)), "Le fichier à lire n'existe pas"
        
        # Lecture fichier JSON
        with open(nomJSON, encoding = 'utf-8') as fichier : listeJSON = json.load(fichier)
    
        # Récupération liste produits
        self.setListeProduits(listeJSON["liste produits"])
        
        
    
    def ecrireListeProduits(self, nomJSON : str) -> None :
        
        '''Enregistre la liste de produits sous forme de fichier JSON\n
Paramètres :
    -nomJSON : str -> nom (ou chemin) du fichier JSON à enregistrer'''
        
        assert(isinstance(nomJSON, str)), "Le chemin du fichier à écrire doit être une chaine de caractères"
        assert(nomJSON[len(nomJSON) - 5:] == ".json"), "Le fichier à écrire n'est pas un fichier JSON"
        
        with open(nomJSON, 'w') as fichier : json.dump({'liste produits' : self.getListeProduits()}, fichier, ensure_ascii = False)
        
        
        
    def produitEstDansListe(self, produit : str) -> bool :
        
        '''Retourne true si un produit est présent dans la liste de produits du supermarché, sinon retourne false'''
        
        assert(isinstance(produit, str)), "Le produit doit être une chaine de caractères"
        
        return(produit in self.getListeProduits())
    
    
    
    def setListeProduits(self, listeProduits : list[str]) -> None :
        
        '''Modifie la liste de produits utilisée par le supermarché'''
        
        assert(isinstance(listeProduits, list)), "La nouvelle liste de produits doit être une liste de chaines de caractères"
        for produit in listeProduits :
            assert(isinstance(produit, str)), "La nouvelle liste de produits doit être une liste de chaines de caractères"
        
        self.__listeProduits = listeProduits
    
    
    
    def ajouterProduit(self, produit : str) -> None :
        
        '''Ajoute un produit à la liste de produits du supermarché'''
        
        assert(isinstance(produit, str)), "Le produit doit être une chaine de caractères"
        assert(not self.produitEstDansListe(produit)), "Le produit à ajouter ne doit pas déjà être présent dans la liste"
        
        self.__listeProduits.append(produit)
    
    
        
    def supprimerProduit(self, produit : str) -> None :
        
        '''Supprime un produit de la liste de produits du supermarché'''
        
        assert(isinstance(produit, str)), "Le produit doit être une chaine de caractères"
        assert(self.produitEstDansListe(produit)), "Il est impossible de supprimer un produit déjà absent de la liste"
        
        self.__listeProduits.remove(produit)
        
        
        
    # --- Manipulation quadrillage --- #
    
    def getQuadrillage(self) -> list[list[list[str]]] :
        
        '''Retourne le quadrillage du supermarché'''
        
        return self.__quadrillage
    
    
    
    def lireQuadrillage(self, nomJSON : str) -> None :
        
        '''Récupère le quadrillage contenu dans un fichier JSON\n
Paramètres :
    - nomJSON : str -> nom (ou chemin) du fichier JSON à lire'''
    
        assert(isinstance(nomJSON, str)), "Le chemin du fichier à lire doit être une chaine de caractères"
        assert(nomJSON[len(nomJSON) - 5:] == ".json"), "Le fichier à lire n'est pas un fichier JSON"
        assert(os.path.exists(nomJSON)), "Le fichier à lire n'existe pas"
        
        # Lecture fichier JSON
        with open(nomJSON, encoding = 'utf-8') as fichier : listeJSON = json.load(fichier)

        # Récupération liste produits
        self.setQuadrillage(listeJSON["quadrillage"])
    
    
    
    def ecrireQuadrillage(self, nomJSON : str) -> None :
        
        '''Enregistre le quadrillage sous forme de fichier JSON\n
Paramètres :
    -nomJSON : str -> nom (ou chemin) du fichier JSON à enregistrer'''
        
        assert(isinstance(nomJSON, str)), "Le chemin du fichier à écrire doit être une chaine de caractères"
        assert(nomJSON[len(nomJSON) - 5:] == ".json"), "Le fichier à écrire n'est pas un fichier JSON"
        
        with open(nomJSON, 'w') as fichier : json.dump({'quadrillage' : self.getQuadrillage()}, fichier, ensure_ascii = False)
    
    
    
    def setQuadrillage(self, quadrillage : list[list[list[str]]]) -> None :
        
        '''Modifie le quadrillage du supermarché'''
        
        assert(isinstance(quadrillage, list)), "Le nouveau quadrillage doit être une liste de listes de listes de chaines de caratères"
        for ligne in quadrillage :
            assert(isinstance(ligne, list)), "Le nouveau quadrillage doit être une liste de listes de listes de chaines de caratères"
            for colonne in ligne :
                assert(isinstance(colonne, list)), "Le nouveau quadrillage doit être une liste de listes de listes de chaines de caratères"
                for texte in colonne :
                    assert(isinstance(texte, str)), "Le nouveau quadrillage doit être une liste de listes de listes de chaines de caratères"
        
        self.__quadrillage = quadrillage
    
# ------------ #
# --- Main --- #
# ------------ #

if __name__ == "__main__" :
    
    print("test")