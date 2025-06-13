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

import os, json, filepile as fp
from shutil import copy

# --------------- #
# --- Classes --- #
# --------------- #

class Supermarche() :
    
    """Modélisation d'un supermarché. Ce dernier comprend :\n
    - plan : str -> une image représentant le plan du supermarché
    - listeProduits : list[str] -> la liste de produits vendus par le supermarché
    - quadrillage : list[list[list[str]]] -> le supermarché divisé en cases
Dans le quadrillage, chaque case peut être vide ou alors elle peut être une entrée, une caisse, un mur ou même contenir des produits.\n
L'utilisateur peut :
    - Lire les informations d'un supermarché à partir d'un dossier*
    - Récupérer/modifier le plan du supermarché
    - Récupérer/modifier la liste de produits du supermarché
    - Récupérer/modifier le quadrillage du supermarché (ex : modifier longueur ou hauteur)
    - Récupérer/modifier des cases précises du quadrillage
    - Obtenir le chemin le plus optimal à suivre pour récupérer les produits d'un supermarché et atteindre la caisse
    - Enregistrer les informations du supermarché dans un dossier*\n
* -> Le dossier en question a pour syntaxe :
    - plan.jpg -> le plan du supermarché
    - liste_produits.json : la liste de produits vendus par le supermarché
    - quadrillage.json : le quadrillage du supermarché"""
    
    # --- Constructeur --- #

    def __init__(self, nomDossier : str = None) :
        
        '''Initialise le supermarché.
Si un dossier a été fourni, l'initialisation se fait avec les informations du dossier.
Sinon, les arguments prennent leurs valeurs par défaut :\n
    - "plan.png" pour le chemin du plan utilisé
    - Une liste vide pour la liste de produits du supermarché
    - Un quadrillage vide cubique avec 10 cases de longueur pour le quadrillage du supermarché.'''
        
        # Gestion des exceptions
        assert(isinstance(nomDossier, (str|None))), "Le chemin du dossier à lire doit être une chaine de caractères ou ne doit pas avoir de valeur"
        
        # Dossier fourni : lecture dossier
        if (nomDossier) : self.lireDossier(nomDossier)
        
        # Sinon : valeurs par défaut
        else :
            self.setPlan("plan.jpg")
            self.setListeProduits([])
            self.__quadrillage : list[list[list[str]]] = [[[] for j in range (10)] for i in range(10)]

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
        plan_src = os.path.abspath(self.getPlan())
        plan_dst = os.path.abspath(nomDossier + "/plan.jpg")
        if plan_src != plan_dst:
            copy(plan_src, plan_dst)
            
        self.ecrireListeProduits(nomDossier + "/liste_produits.json")
        self.ecrireQuadrillage(nomDossier + "/quadrillage.json")
    
    # --- Manipulation plan --- #
    
    def getPlan(self) -> str :
        
        '''Retourne le plan de supermarché utilisé'''
        
        return self.__plan
    
    def setPlan(self, planChemin : str) -> None :
        
        '''Modifie le plan de supermarché utilisé'''
        
        assert(isinstance(planChemin, str)), "Le chemin du plan à utiliser doit être une chaine de caractères"
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
        
        #assert(isinstance(produit, str)), "Le produit doit être une chaine de caractères"
        
        return(produit in self.getListeProduits())
    
    
    
    def setListeProduits(self, listeProduits : list[str]) -> None :
        
        '''Modifie la liste de produits utilisée par le supermarché'''
        
        assert(isinstance(listeProduits, list)), "La nouvelle liste de produits doit être une liste de chaines de caractères"
        for produit in listeProduits :
            assert(isinstance(produit, str)), "La nouvelle liste de produits doit être une liste de chaines de caractères"
        
        self.__listeProduits = listeProduits
    
    
    
    def ajouterProduit(self, produit : str) -> None :
        
        '''Ajoute un produit à la liste de produits du supermarché'''
        
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
        
        quadrillage = self.getQuadrillage()
        if not quadrillage or len(quadrillage) == 0 : return 0
        return len(quadrillage[-1])
    
    def getLongueur(self) -> int :
        
        '''Retourne la longueur du quadrillage'''
        
        return len(self.getQuadrillage()[-1])
    
    def getHauteur(self) -> int :
        
        '''Retourne la hauteur du quadrillage'''
        
        return len(self.getQuadrillage())
    
    def getTaille(self) -> tuple :
        
        '''Retourne un tuple comportant la longueur et la hauteur du quadrillage'''
        
        return(self.getLongueur(), self.getHauteur())
    
    
    def setLongueur(self, longueur : int) -> None :
        
        '''Modifie la longueur du quadrillage.
Si la longueur augmente, alors de nouvelles cases vides sont ajoutées.
Dans le cas contraires, des cases déjà existantes seront supprimées.'''
        
        assert(isinstance(longueur, int)), "La longueur du quadrillage doit être un entier supérieur à 1"
        assert(longueur >= 2), "La longueur du quadrillage doit être un entier supérieur à 1"
        
        for y in range(self.getHauteur()) :
        
            # Augmentation de la longueur du quadrillage
            if (longueur > self.getLongueur()) :
                    
                self.__quadrillage[y] = self.__quadrillage[y] + [[] for i in range(longueur - self.getLongueur())]
            
            # Réduction de la longueur du quadrillage
            elif (longueur < self.getLongueur()) :
                
                for i in range(self.getLongueur() - longueur) : self.__quadrillage[y].pop(-1)
                
                
                
    def setHauteur(self, hauteur : int) -> None :
        
        '''Modifie la hauteur du quadrillage.
Si la hauteur augmente, alors de nouvelles cases vides sont ajoutées.
Dans le cas contraires, des cases déjà existantes seront supprimées.'''
        
        assert(isinstance(hauteur, int)), "La hauteur du quadrillage doit être un entier supérieur à 1"
        assert(hauteur >= 2), "La hauteur du quadrillage doit être un entier supérieur à 1"
        
        # Augmentation de la hauteur du quadrillage
        if (hauteur > self.getHauteur()) :
                
            self.__quadrillage = self.__quadrillage + [[[] for i in range(self.getLongueur())] for j in range(hauteur - self.getHauteur())]
        
        # Réduction de la hauteur du quadrillage
        elif (hauteur < self.getHauteur()) :
            
            for i in range(self.getHauteur() - hauteur) : self.__quadrillage.pop(-1)
        
        
    
    def setTaille(self, longueur : int, hauteur : int) -> None :
        
        """Modifie la taille du quadrillage.\n
Paramètres :
    - longueur : int -> Nouvelle longueur du quadrillage
    - hauteur : int -> Nouvelle hauteur du quadrillage"""
        
        self.setLongueur(longueur)
        self.setHauteur(hauteur)
    
    
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
            
            return "produit"
        
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
        
        assert(isinstance(case, (str|list))), "Le contenu de la case doit être un chaine de caractères ou une liste de chaines de caractères"
        if isinstance(case, str) : assert(case in ["entrée", "caisse", "mur", "sol", ""]), "Le contenu de la case est invalide"
        else : 
            for produit in case : assert(isinstance(produit, str)), "Chaque produit de la liste doit être une chaine de caractères"
        
        # Script 
        
        # Cas où la case devient une liste de produits
        if isinstance(case, list) : self.__quadrillage[y][x] = case
        
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
        
        
        
    def getEntrees(self) -> list[tuple] :
        
        '''Retourne la liste des coordonnées de toutes les entrées du supermarché'''
        
        # Variables locales
        listeCases : list[tuple] = []
        
        # Script
        for y in range(len(self.getQuadrillage())) :

            for x in range(len(self.getQuadrillage()[y])) :
                
                if (self.getTypeCase(x,y) == "entrée") :
                    
                    listeCases.append((x,y))
                    
        return listeCases
    
    
    
    def getCaisses(self) -> list[tuple] :
        
        '''Retourne la liste des coordonnées de toutes les caisses du supermarché'''
        
        # Variables locales
        listeCases : list[tuple] = []
        
        # Script
        for y in range(len(self.getQuadrillage())) :

            for x in range(len(self.getQuadrillage()[y])) :
                
                if (self.getTypeCase(x,y) == "caisse") :
                    
                    listeCases.append((x,y))
                    
        return listeCases
    
    
    def getMurs(self) -> list[tuple] :
        
        '''Retourne la liste des coordonnées de tous les murs du supermarché'''
        
        # Variables locales
        listeCases : list[tuple] = []
        
        # Script
        for y in range(len(self.getQuadrillage())) :

            for x in range(len(self.getQuadrillage()[y])) :
                
                if (self.getTypeCase(x,y) == "mur") :
                    
                    listeCases.append((x,y))
                    
        return listeCases

    
    
    def getCasesAvecProduits(self) -> list[tuple] :
        
        '''Retourne la liste des coordonnées de toutes les cases avec des produits du supermarché'''
        
        # Variables locales
        listeCases : list[tuple] = []
        
        # Script
        for y in range(len(self.getQuadrillage())) :

            for x in range(len(self.getQuadrillage()[y])) :
                
                if (self.getTypeCase(x,y) == "produit") :
                    
                    listeCases.append((x,y))
                    
        return listeCases
    
    
    
    def getCasesVides(self) -> list[tuple] :
        
        '''Retourne la liste des coordonnées de toutes les cases vides du supermarché'''
        
        # Variables locales
        listeCases : list[tuple] = []
        
        # Script
        for y in range(len(self.getQuadrillage())) :

            for x in range(len(self.getQuadrillage()[y])) :
                
                if (self.getTypeCase(x,y) == "sol") :
                    
                    listeCases.append((x,y))
                    
        return listeCases
    
    
    
    def getCasesAlentours(self, x : int, y : int) -> list[tuple] :
        
        """Retourne la liste des coordonnées de toutes les cases présentes autour de la case désignée par x et y."""
        
        assert(self.coordonneesValides(x, y)), "Les coordonnées entrées sont invalides"
        
        # Variables locales
        listeCases : list[tuple] = []
        
        # Script
        for j in range(y-1, y+2) :
            
            for i in range(x-1, x+2) :
                
                if (self.coordonneesValides(i, j) and not (i == x and j == y)) : 
                    
                    listeCases.append((i, j))
                
        return listeCases
    
    
    
    def getDijkstra(self, x : int, y : int) -> dict :
        
        """Retourne un dictionnaire comportant les coordonnées de toutes les cases atteignables à partir de la case désignée par x et y.
Pour chaque case, le dictionnaire comporte également la case permettant de l'atteindre ainsi que la distance avec la case de départ.\n
Pour rappel, dans un quadrillage :
    - Les murs sont infranchissables
    - Les cases comportant des produits et les caisses peuvent être accédées mais ne permettent pas d'accéder à d'autres cases 
    - Tout le reste est franchissable sans difficulté"""
        
        # --- Variables locales --- #
        
        dijkstra : dict = {(x, y) : (None, 0)} # Dictionnaire de toutes les cases atteignables
        
        # Variables utilisées pour l'algorithme de Dijkstra (file de cases à parcourir + case à parcourir)
        file : fp.File = fp.File(self.getLongueur() * self.getHauteur()) ; file.enfiler((x,y)) 
        caseParcourue : tuple
        
        # --- Script --- #
        
        # Algorithme de Dijsktra
        while (file.est_vide() == False) :
            
            caseParcourue = file.defiler()
            
            # Les cases comportant des produits et les caisses peuvent être accédées mais ne permettent pas d'accéder à d'autres cases
            if (self.getTypeCase(caseParcourue[0], caseParcourue[1]) not in ["produit", "caisse"]) :
            
                for case in self.getCasesAlentours(caseParcourue[0], caseParcourue[1]) :
                    
                    # Les murs sont infranchissables
                    if (self.getTypeCase(case[0], case[1]) != "mur" and (case not in dijkstra.keys() or dijkstra[case][1] > dijkstra[caseParcourue][1] + 1)) :
                        
                        dijkstra[case] = (caseParcourue, dijkstra[caseParcourue][1] + 1)
                        file.enfiler(case)
                    
        dijkstra.pop((x,y))
        return dijkstra
    
    
    
    def entreeEstAccessible(self, x : int, y : int) -> bool :
        
        """Retourne true si une entrée est accessible à partir de la case désignée par x et y. Retourne false dans le cas contraire."""
        
        assert(self.getTypeCase(x,y) != "mur"), "La case sélectionnée est un mur"
        assert(self.getTypeCase(x,y) != "caisse"), "La case sélectionnée est une caisse"
        assert(self.getTypeCase(x,y) != "produit"), "La case sélectionnée est une case contenant des produits"
        
        # --- Variables locales --- #
        
        i : int = 0 # Gestion boucle
        casesAtteignables : list[tuple] = list(self.getDijkstra(x,y).keys()) # Liste des cases atteignables à partir de la case de départ
        
        # --- Script --- #
        
        if (self.getTypeCase(x,y) == "entrée") : return True # Cas où la case de départ elle-même est une entrée = entrée accessible
        
        else : # Sinon : recherche d'une entrée accessible
            
            while (i < len(casesAtteignables) and not casesAtteignables[i] in self.getEntrees()) : i += 1
        
        return i < len(casesAtteignables)
    
    
    
    def caisseEstAccessible(self, x : int, y : int) -> bool :
        
        """Retourne true si une caisse est accessible à partir de la case désignée par x et y. Retourne false dans le cas contraire."""
        
        assert(self.getTypeCase(x,y) != "mur"), "La case sélectionnée est un mur"
        assert(self.getTypeCase(x,y) != "produit"), "La case sélectionnée est une case contenant des produits"
        
        # --- Variables locales --- #
        
        i : int = 0 # Gestion boucle
        casesAtteignables : list[tuple] = list(self.getDijkstra(x,y).keys()) # Liste des cases atteignables à partir de la case de départ
        
        # --- Script --- #
        
        if (self.getTypeCase(x,y) == "caisse") : return True # Cas où la case de départ elle-même est une caisse = caisse accessible
        
        else : # Sinon : recherche d'une caisse accessible
            
            while (i < len(casesAtteignables) and not casesAtteignables[i] in self.getCaisses()) : i += 1
            
        return i < len(casesAtteignables)
    
    
    
    def toutEstAccessible(self, x : int, y : int) -> bool :
        
        """Retourne true si une entrée et une caisse sont accessibles à partir de la case désignée par x et y. Retourne false dans le cas contraire."""
        
        return (self.entreeEstAccessible(x,y) and self.caisseEstAccessible(x,y))
    
    
    def produitEstAccessible(self, x : int, y : int, produit : str) -> bool :
        
        """Retourne true si une case contenant un produit en particulier est accessible à partir de la case désignée par x et y. Retourne false dans le cas contraire."""
        
        assert(self.getTypeCase(x,y) != "mur"), "La case sélectionnée est un mur"
        assert(self.getTypeCase(x,y) != "caisse"), "La case sélectionnée est une caisse"
        
        # --- Variables locales --- #
        
        i : int = 0 # Gestion boucle
        casesAtteignables : list[tuple] = list(self.getDijkstra(x,y).keys()) # Liste des cases atteignables à partir de la case de départ
        
        # --- Script --- #
        
        # Cas où la case de départ elle-même contient le produit recherché = produit accessible
        if (self.getTypeCase(x,y) == "produit" and self.produitEstDansCase(x,y,produit)) : return True 
        
        else : # Sinon : recherche d'une case accessible contenant le produit

            while (i < len(casesAtteignables)) :
                
                if (casesAtteignables[i] in self.getCasesAvecProduits()) :
                    
                    if (self.produitEstDansCase(casesAtteignables[i][0], casesAtteignables[i][1], produit)) : return True
                    
                    else : i += 1
                    
                else : i += 1
            
            return False
    
    
    
    def chercherProduitsAccessibles(self, x : int, y : int, listeProduits : list[str]) -> bool :
        
        """Retourne une liste de produits accessibles (parmi les produits de la liste entrée en argument) à partir de la case désignée par x et y."""
        
        assert(isinstance(listeProduits, list)), "La liste de produits doit être une liste de chaines de caractères"
        
        # --- Variables locales --- #
        
        produitsAccessibles : list[str] = [] # Liste de produits accessibles
        
        # --- Script --- #
        
        for produit in listeProduits : # Pour chaque produit : recherche parmi les cases accessibles
            
            if (self.produitEstAccessible(x, y, produit)) : produitsAccessibles.append(produit) # Si produit présent : ajout dans la liste
            
        return produitsAccessibles
    
    
    
    def chercherProduitsInaccessibles(self, x : int, y : int, listeProduits : list[str]) -> bool :
        
        """Retourne une liste de produits inaccessibles (parmi les produits de la liste entrée en argument) à partir de la case désignée par x et y."""
        
        assert(isinstance(listeProduits, list)), "La liste de produits doit être une liste de chaines de caractères"
        
        # --- Variables locales --- #
        
        produitsInaccessibles : list[str] = [] # Liste de produits inaccessibles
        
        # --- Script --- #
        
        for produit in listeProduits : # Pour chaque produit : recherche parmi les cases accessibles
            
            if (not self.produitEstAccessible(x, y, produit)) : produitsInaccessibles.append(produit) # Si produit absent : ajout dans la liste
            
        return produitsInaccessibles



    def trierDijkstra(self, x : int, y : int, listeProduits : list[str]) -> dict :
        
        """Retourne un dictionnaire de cases accessibles trié de telle sorte à ne contenir que les cases importantes.
Ces dernières comprennent :
    - Une caisse du supermarché
    - Les cases à accéder pour obtenir les produits de la liste de course de l'utilisateur.
Pour que cette méthode fonctionne, il faut impérativement que la case de départ (désignée par x et y) soit une entrée du supermarché."""
        
        assert((x,y) in self.getEntrees()), "La case de départ doit être une entrée"
        assert(self.toutEstAccessible(x,y)), "Aucun chemin ne peut être établi"
        
        # --- Variables locales --- #
        
        nouveauDijkstra : dict = {} # Dictionnaire de cases accessibles trié
        
        # Liste de courses triée de telle sorte à ne contenir que les produits accessibles à partir de la case de départ
        nouvelleListe : list[str] = self.chercherProduitsAccessibles(x, y, listeProduits) 
        
        produit : int # Gestion boucles
        
        derniereCase : tuple # Avant dernière case à parcourir (la toute dernière étant une caisse) 
        derniereCaseDijkstra : list[tuple] # Liste de cases atteignables à partir de cette même avant dernière case
        
        # Piles comportant les valeurs stockées dans le dictionnaire trié (afin de les ranger dans l'ordre décroissant de distances)
        pileDijkstraCles : fp.Pile = fp.Pile(self.getLongueur() * self.getHauteur())
        pileDijkstraValeurs : fp.Pile = fp.Pile(self.getLongueur() * self.getHauteur())
        
        # --- Script --- #
        
        # Récupération de toutes les cases contenant des produits à accéder
        for case in self.getDijkstra(x,y).keys() :
            
            if self.getTypeCase(case[0], case[1]) == "produit" :

                produit = 0
                while (produit < len(nouvelleListe) and not self.produitEstDansCase(case[0], case[1], nouvelleListe[produit])) : produit += 1
                
                if (produit < len(nouvelleListe)) :
                     
                    pileDijkstraCles.empiler(case)
                    pileDijkstraValeurs.empiler(self.getDijkstra(x,y)[case])
   
                    # Si un produit a été accédé : il est retiré de la liste afin de ne pas récupérer d'autres cases inutiles
                    nouvelleListe.pop(produit)
        
        # Rangement de toutes les cases contenant des produits dans l'ordre décroissant de distances
        while (not pileDijkstraCles.est_vide()) :
            
            if (pileDijkstraCles.nombre_elements == 1) :
                
                derniereCase = pileDijkstraCles.depiler()            
                nouveauDijkstra[derniereCase] = pileDijkstraValeurs.depiler()
                derniereCase = nouveauDijkstra[derniereCase][0] # Récupération de l'avant dernière case à parcourir
            
            else : nouveauDijkstra[pileDijkstraCles.depiler()] = pileDijkstraValeurs.depiler()
            
        # Récupération de la caisse la plus proche de l'avant dernière case
        derniereCaseDijkstra = list(self.getDijkstra(derniereCase[0], derniereCase[1]).keys())
        produit = 0
        
        while (produit < len(derniereCaseDijkstra) and derniereCaseDijkstra[produit] not in self.getCaisses()) :
                
            produit += 1
            
            if (derniereCaseDijkstra[produit] in self.getCaisses()) : 
                
                nouveauDijkstra[derniereCaseDijkstra[produit]] = self.getDijkstra(x,y)[derniereCaseDijkstra[produit]]

        # Retour du dictionnaire trié
        return nouveauDijkstra
    
    
    
    def genererMorceauChemin(self, xDepart : int, yDepart : int, xArrivee : int, yArrivee : int) -> fp.Pile :
        
        """Retourne dans l'ordre la liste des cases à parcourir pour aller d'un point A (case de départ) à un point B (case d'arrivée)"""
        
        assert((xArrivee, yArrivee) in self.getDijkstra(xDepart, yDepart).keys()), "Aucun chemin ne peut être établi entre ces deux cases"
        
        # --- Variables locales --- #
        
        chemin : fp.Pile = fp.Pile(self.getLongueur() * self.getHauteur()) # Liste de cases à parcourir entre la case de départ et celle d'arrivée
        
        # Case permettant d'accéder à d'autres cases
        # Au départ : case permettant d'accéder à la case d'arrivée
        casePrecedente : tuple = (xArrivee, yArrivee)
        
        # --- Script --- #

        # Parcours à l'envers : de la case d'arrivée à la case de départ (d'où l'utilisation d'une pile)
        while (casePrecedente != (xDepart, yDepart)) :
            
            chemin.empiler(casePrecedente) ; casePrecedente = self.getDijkstra(xDepart, yDepart)[(casePrecedente[0], casePrecedente[1])][0]
    
        return chemin
    
    
    
    def genererChemin(self, x : int, y : int, listeProduits : list[str]) -> list :
        
        """Retourne le chemin complet à parcourir pour obtenir tous les produits d'une liste de courses à partir d'une entrée désignée par x et y."""
        
        assert (self.toutEstAccessible(x,y)), "Aucun chemin ne peut être établi"
        
        # --- Variables locales --- #
        
        chemin : list[tuple] = [(x,y)] # Chemin complet à parcourir
        # Cases importantes à parcourir
        dijkstra = self.trierDijkstra(x,y,self.chercherProduitsAccessibles(x, y, listeProduits)) 
        listeDijkstra = list(dijkstra.keys())
        
        pileCases : fp.Pile = fp.Pile(self.getLongueur() * self.getHauteur()) # Pile permettant de générer le chemin correctement
        
        caseArrivee : tuple # Case dont le chemin d'accès doit être généré
        
        # --- Script --- #
    
        while (listeDijkstra != []) :
            
            # Détermination du point B à atteindre
            if (listeDijkstra[0] in self.getCaisses() and len(listeDijkstra) > 1) : caseArrivee = listeDijkstra.pop(1)
            else : caseArrivee = listeDijkstra.pop(0)
            
            # Génération du chemin vers le point B
            if (chemin[-1] in self.getCasesAvecProduits()) :
                pileCases = self.genererMorceauChemin(chemin[-2][0], chemin[-2][1], caseArrivee[0], caseArrivee[1])
                pileCases.empiler(chemin[-2])
            else :
                pileCases = self.genererMorceauChemin(chemin[-1][0], chemin[-1][1], caseArrivee[0], caseArrivee[1])
            
            # Ajout du morceau de chemin dans le chemin final
            while (not pileCases.est_vide()) : chemin.append(pileCases.depiler())
            
        return chemin

            
# ------------ #
# --- Main --- #
# ------------ #

if __name__ == "__main__" :
    
    test = Supermarche()