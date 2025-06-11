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

    def __init__(self, nomDossier : str = None) :
        
        '''Initialise le supermarché.
Si un dossier a été fourni, l'initialisation se fait avec les informations du dossier.
Sinon, les arguments prennent leurs valeurs par défaut :\n
    - "plan.png" pour le chemin du plan utilisé
    - Une liste vide pour la liste de produits du supermarché
    - Un quadrillage cubique avec 10 cases de longueur, une entrée au coin supérieur gauche et une sortie juste à côté pour le quadrillage du supermarché.'''
        
        # Gestion des exceptions
        assert(isinstance(nomDossier, (str|None))), "Le chemin du dossier à lire doit être une chaine de caractères ou ne doit pas avoir de valeur"
        
        # Dossier fourni : lecture dossier
        if (nomDossier) : self.lireDossier(nomDossier)
        
        # Sinon : valeurs par défaut
        else :
            self.setPlan("plan.jpg")
            self.setListeProduits([])
            self.__quadrillage : list[list[list[str]]] = [[[] for j in range (10)] for i in range(10)] ; self.__quadrillage[0][0] = ["entrée"] ; self.__quadrillage[0][1] = ["caisse"]

    # --- Manipulation fichiers --- #
    
    def lireDossier(self, nomDossier : str) -> None :
        
        '''Récupère toutes les informations contenues dans un dossier de supermarché.\n
Paramètres :
    - nomDossier : str -> nom du dossier à créer'''
        
        # Gestion des exceptions
        assert(isinstance(nomDossier, str)), "Le chemin du dossier à lire doit être une chaine de caractères"
        assert(os.path.exists(nomDossier)), "Le dossier à lire n'existe pas"
        assert(os.path.exists(nomDossier + "/plan.jpg")), "Il manque des informations dans le dossier à lire"
        assert(os.path.exists(nomDossier + "/liste_produits.json")), "Il manque des informations dans le dossier à lire"
        assert(os.path.exists(nomDossier + "/quadrillage.json")), "Il manque des informations dans le dossier à lire"
        
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
        
        assert(not self.produitEstDansListe(produit)), "Le produit à ajouter ne doit pas déjà être présent dans la liste"
        
        self.__listeProduits.append(produit)
    
    
        
    def supprimerProduit(self, produit : str) -> None :
        
        '''Supprime un produit de la liste de produits du supermarché'''
        
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
        
    
    def getLongueur(self) -> int :
        
        '''Retourne la longueur du quadrillage'''
        
        return len(self.getQuadrillage()[0])
    
    def getHauteur(self) -> int :
        
        '''Retourne la hauteur du quadrillage'''
        
        return len(self.getQuadrillage())
    
    def getTaille(self) -> tuple :
        
        '''Retourne un tuple comportant la longueur et la hauteur du quadrillage'''
        
        return(self.getLongueur(), self.getHauteur())
    
    # !!!! A ÉCRIRE !!!!
    # !!!! A ÉCRIRE !!!!
    
    #def setLongueur(self, longueur : int) -> None :
    #    
    #    '''Modifie la longueur du quadrillage'''
    #    
    #    assert(isinstance(longueur, int)), "La longueur du quadrillage doit être un entier supérieur à 1"
    #    assert(longueur >= 2), "La longueur du quadrillage doit être un entier supérieur à 1"
    
    #setHauteur
    #setTaille
           
    # !!!! A ÉCRIRE !!!!
    # !!!! A ÉCRIRE !!!!
    
    def xValide(self, x : int) -> bool :
        
        '''Retourne true si x est un entier compris entre les bornes du quadrillage et false dans le cas contraire.'''
        
        return(isinstance(x, int) and x >= 0 and x < self.getLongueur())
    
    
    def yValide(self, y : int) -> bool :
        
        '''Retourne true si y est un entier compris entre les bornes du quadrillage et false dans le cas contraire.'''
        
        return(isinstance(y, int) and y >= 0 and y < self.getHauteur())
    
    
    def coordonneesValides(self, x : int, y : int) -> bool :
        
        '''Retourne true si les deux coordonnées x et y sont valides et false dans le cas contraire'''
        
        return(self.xValide(x) and self.yValide(y))

    
    def getCase(self, x : int, y : int) -> list[str]:
        
        '''Retourne la case du quadrillage présente aux coordonnées x et y entrées en argument.'''
        
        assert(self.coordonneesValides(x, y)), "Les coordonnées entrées sont invalides"
        
        return self.getQuadrillage()[y][x]


    
    def getTypeCase(self, x : int, y : int) -> str :
        
        '''Retourne le type de la case désignée par x et y.
Voici les différents types de case pour référence :\n
    - entrée -> lorsque la case est une entrée
    - caisse -> lorsque la case est une caisse
    - mur -> lorsque la case est un mur
    - produits -> lorsque la case contient une liste de courses
    - sol -> lorsque la case ne contient rien'''
        
        # Si la case est vide
        if (self.getCase(x,y) == []) :
            
            return "sol"
        
        # Si la case contient une liste de produits
        elif (len(self.getCase(x,y)) > 1 or not self.getCase(x, y)[0] in ["entrée", "caisse", "mur"]) :
            
            return "produits"
        
        # Si la case est une entrée, une caisse ou un mur
        else :
            
            return self.getCase(x,y)[0]
        
        
        
    def produitEstDansCase(self, x : int, y : int, produit : str) -> None :
        
        '''Retourne true si un produit est présent dans la liste de produits de la case désignée, sinon retourne false'''
        
        assert(isinstance(produit, str)), "Le produit doit être une chaine de caractères"
        assert(self.getTypeCase(x, y) == "produit"), "La case à vérifier doit être une case comportant des produits"
        
        return(produit in self.getCase(x, y))
    
        
        
    def setCase(self, x : int, y : int, case : (str|list[str])) -> None :
        
        '''Modifie la case désignée par les coordonnées x et y.\n
Paramètres :
    - x : int -> Abscisse x de la case à modifier
    - y : int -> Ordonnée y de la case à modifier
    - case : (str|list[str]) -> Paramètre qui définit la nouvelle case. Ce dernier peut prendre ces valeurs :\n
        - Une liste de chaines de caractères -> transforme la case en case comportant des produits. Sa liste de produits est la même que celle entrée en paramètre.
        - "sol" ou "" -> transforme la case en case vide
        - "entrée" -> transforme la case en entrée
        - "caisse" -> transforme la case en caisse
        - "mur" -> transforme la case en mur'''
        
        # Gestion exceptions
        
        assert(isinstance(case, (str|list[str]))), "Le contenu de la case doit être un chaine de caractères ou une liste de chaines de caractères"
        if isinstance(case, str) : assert(case in ["entrée", "caisse", "mur", "sol", ""]), "Le contenu de la case est invalide"
        else : 
            for produit in case : assert(isinstance(produit, str)), "Chaque produit de la liste doit être une chaine de caractères"
        
        # Script 
        
        # Cas où la case devient une liste de produits
        if isinstance(case, list[str]) : self.__quadrillage[y][x] = case
        
        # Cas où la case devient vide
        elif (case in ["sol", ""]) : self.__quadrillage[y][x] = []
        
        # Cas où la case devient un mur, une entrée ou une caisse
        else : self.__quadrillage[y][x] = [case]
        
        
         
    def ajouterProduitCase(self, x : int, y : int, produit : str) -> None :
        
        '''Ajoute un produit à la liste de produits de la case désignée par x et y'''
        
        assert(not self.produitEstDansCase(x, y, produit)), "Le produit à ajouter ne doit pas déjà être présent dans la liste"
        
        self.__quadrillage[y][x].append(produit)
        
    
    def supprimerProduitCase(self, x : int, y : int, produit : str) -> None :
        
        '''Supprime un produit de la liste de produits de la case désignée par x et y'''
        
        assert(self.produitEstDansCase(x, y, produit)), "Il est impossible de supprimer un produit déjà absent de la liste"
        
        self.__quadrillage[y][x].remove(produit)
            
# ------------ #
# --- Main --- #
# ------------ #

if __name__ == "__main__" :
    
    test = Supermarche()
    print(test.produitEstDansCase(-1, 1, "test"))