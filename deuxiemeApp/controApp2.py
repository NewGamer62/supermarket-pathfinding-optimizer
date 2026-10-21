# Formation : BUT 1ʳᵤ année | 2024-2025
# Ressource : SAE S2 - Algo et Graphes
# Professeur : M. Conoir
# Noms :  AMEDRO Louis (TPD)
#         HERBAUX Jules (TPD)
#         GAILLARD Noa (TPC)
#         MINNEBO Valentin (TPA)

# --------------- #
# --- Modules --- #
# --------------- #

from modele import Projet
import vueApp2 as vue
from PyQt6.QtCore import QObject

# --------------- #
# --- Classes --- #
# --------------- #

class Controleur(QObject) :
    
    """Contrôleur de l'application n°2."""
    
    # --- Constructeur --- #
    
    def __init__(self) :
        
        """Instancie l'application"""
        
        # Instanciation
        super().__init__()
        self.modele = Projet()
        self.vue = vue.ClientApp()
        
        # Connexions signaux
        self.vue.signalGeneratePath.connect(self.genererCheminDepuisListe)
        self.vue.signalGetFolder.connect(self.chargerSupermarcheDepuisDossier)
        
        # Affichage
        self.vue.show()
        
    # --- Manipulation fichiers --- #

    def chargerSupermarcheDepuisDossier(self, chemin: str) :
        
        """Permet de charger un projet déjà existant dans l'application.\n
Paramètres : 
    - chemin : str -> Chemin du dossier à charger"""
        
        try :
            self.modele = Projet(chemin)
            self.vue.setMap(chemin + "/supermarche/plan.jpg")
            
        except Exception as e : print(f"Erreur chargement dossier: {e}")
        
    # --- Autres méthodes --- #

    def genererCheminDepuisListe(self, liste : list) :
        
        """Génère le chemin optimal pour récupérer différents produits dans le supermarché puis affiche ce chemin dans l'application.
Affiche également les produits de la liste de courses impossibles à obtenir.\n
Paramètres :
    - liste : list -> liste de produits à récupérer dans le supermarché."""

        if self.modele.supermarche.getEntrees() :

            entreePrincipale = self.modele.supermarche.getEntrees()[0]
            
            # Affichage produits impossibles à obtenir
            self.vue.missingItemsBox.setText("-".join(self.modele.supermarche.chercherProduitsInaccessibles(entreePrincipale[0], entreePrincipale[1], liste)))
            
            # Génération + affichage chemin
            if (liste and not self.modele.supermarche.chercherProduitsAccessibles(entreePrincipale[0], entreePrincipale[1], liste) == []) :
                chemin = self.modele.supermarche.genererChemin(entreePrincipale[0], entreePrincipale[1], liste) ; self.vue.updateChemin(chemin)