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

import os
from modeleSupermarche import Supermarche
from modeleInformations import Informations

# --------------- #
# --- Classes --- #
# --------------- #

class Projet() :
    
    """Un projet complet. Cette classe comprend :\n
    - informations : Informations -> les informations générales du projet
    - supermarche : Supermarche -> le supermarché utilisé par le projet\n
    En plus de la manipulation directe des informations et du supermarché du projet, l'utilisateur peut :
        - Lire un projet à partir d'un dossier*
        - Enregistrer le projet dans un dossier*
    * -> -> Le dossier en question a pour syntaxe :
        - informations.json -> les informations générales du projet
        - supermarche -> un dossier comportant les informations sur le supermarché du projet (voir classe Supermarche)"""
    
    # --- Constructeur --- #
    
    def __init__(self, nomDossier : str = None) :
        
        '''Initialise le projet complet.
Si un dossier a été fourni, l'initialisation se fait avec les informations du dossier.
Sinon, les informations sont initialisées par défaut par défaut (voir chacune des classes pour plus d'informations)'''

        assert(isinstance(nomDossier, (str|None))), "Le chemin du dossier à lire doit être une chaine de caractères ou ne doit pas avoir de valeur"
        
        # Valeurs par défaut
        self.informations = Informations()
        self.supermarche = Supermarche()
        
        if (nomDossier) : self.lireDossier(nomDossier) # Dossier fourni : lecture dossier
        
    # --- Manipulation fichiers --- #
    
    def lireDossier(self, nomDossier : str) -> None :
        
        '''Récupère toutes les informations contenues dans un dossier de projet.\n
Paramètres :
    - nomDossier : str -> nom du dossier à créer'''
        
        # Gestion des exceptions
        assert(isinstance(nomDossier, str)), "Le chemin du dossier à lire doit être une chaine de caractères"
        assert(os.path.exists(nomDossier)), "Le dossier à lire n'existe pas"
        
        # Récuperation des données
        self.informations.lireFichier(nomDossier + "/informations.json")
        self.supermarche.lireDossier(nomDossier + "/supermarche")
    
        
    def ecrireDossier(self, nomDossier : str) -> None :
        
        '''Crée un dossier comportant toutes les informations du projet et du supermarché\n
Paramètres :
    - nomDossier : str -> nom du dossier à créer'''
        
        # Gestion des exceptions
        assert(isinstance(nomDossier, str)), "Le chemin du dossier à écrire doit être une chaine de caractères"
        
        # Création du dossier (s'il n'existe pas)
        if (not os.path.exists(nomDossier)) : os.makedirs(nomDossier)
        
        # Écriture des fichiers
        self.informations.ecrireFichier(nomDossier + "/informations.json")
        self.supermarche.ecrireDossier(nomDossier + "/supermarche")    
        
# ------------ #
# --- Main --- #
# ------------ #

if __name__ == "__main__" :
    
    test = Projet()