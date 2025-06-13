# Formation : BUT 1ʳᵤ année | 2024-2025
# Ressource : SAE S2 - Algo et Graphes
# Professeur : M. Conoir
# Noms :  AMEDRO Louis (TPD)
#         HERBAUX Jules (TPD)
#         GAILLARD Noa (TPC)
#         MINNEBO Valentin (TPA)

import modeleSupermarche as modele
import vueApp2 as vue
from PyQt6.QtCore import QObject

class Controleur(QObject):
    def __init__(self):
        super().__init__()
        
        self.modele = modele.Supermarche()
        self.vue = vue.ClientApp()
        self.vue.signalGeneratePath.connect(lambda produits: self.setListeProduits(produits))

        self.vue.show()

    def chargerSupermarcheDepuisDossier(self, chemin: str):
        try:
            self.modele = modele.Supermarche(chemin)
            quadrillage = self.modele.getQuadrillage()
            self.vue.planWidget.image_widget.matrice_a_appliquer(quadrillage)
            self.vue.planWidget.image_widget.charger_image(self.modele.getPlan())
            self.vue.boutonEnregistrer.setVisible(True)
        except Exception as e:
            print(f"Erreur chargement dossier: {e}")

    def genererCheminDepuisListe(self, liste_texte: str):
        # Extraction et nettoyage des produits depuis QTextEdit
        listeProduits = [produit.strip() for produit in liste_texte.split('\n') if produit.strip()]

        if not listeProduits:
            print("Aucun produit à chercher")
            return

        # Recherche chemin optimal + produits introuvables
        entrees = self.modele.getEntrees()
        if not entrees:
            print("Aucune entrée définie")
            return

        entree = entrees[0]
        chemin = self.modele.genererChemin(entree[0], entree[1], listeProduits)
        produitsInaccessibles = self.modele.chercherProduitsInaccessibles(entree[0], entree[1], listeProduits)

        # Envoi signaux vers la vue
        self.vue.missingItemsBox(produitsInaccessibles)

    def setListeProduits(self, produits):
        self.listeProduits = produits
        print("Liste enregistré")