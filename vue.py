# Formation : BUT 1ʳᵉ année | 2024-2025
# Ressource : SAE S2 - Algo et Graphes
# Professeur : M. Conoir
# Noms :  AMEDRO Louis (TPD)
#         HERBAUX Jules (TPD)
#         GAILLARD Noa (TPC)
#         MINNEBO Valentin (TPA)

import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextEdit,QLabel, QPushButton, QLineEdit, QApplication)
from PyQt6.QtCore import pyqtSignal
import vueBandeau, vueElementsMagasin, vueInformations, vueListeProduitCase, vueListeProduits, vuePlan

# -----------------------------------------------------------------------------
# --- class Vue
# -----------------------------------------------------------------------------

class Vue(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Super Créateur de Magasin 3000")
        self.setMinimumSize(600, 400)

        # Layout principal :
        layout_principal = QVBoxLayout()
        self.setLayout(layout_principal)

        # Instanciation des widgets
        self.bandeau = vueBandeau.Bandeau()
        self.bandeau.setFixedHeight(40)  # Hauteur réduite du bandeau
        self.elementsMagasin = vueElementsMagasin.ElementsMagasin()
        self.informations = vueInformations.Informations()
        self.listeProduitCase = vueListeProduitCase.ContenuCase()
        self.listeProduits = vueListeProduits.ListeProduits()
        self.plan = vuePlan.Plan()

        # Layouts secondaires
        layout_gauche = QVBoxLayout()
        layout_gauche.addWidget(self.elementsMagasin)
        layout_gauche.addWidget(self.listeProduits)

        layout_droite = QVBoxLayout()
        layout_droite.addWidget(self.informations)
        layout_droite.addWidget(self.listeProduitCase)

        # Layout horizontal principal pour le contenu central
        layout_contenu = QHBoxLayout()
        layout_contenu.addLayout(layout_gauche, 2)
        layout_contenu.addWidget(self.plan, 4)
        layout_contenu.addLayout(layout_droite, 2)

        # Ajout des widgets et layouts dans le layout principal
        layout_principal.addWidget(self.bandeau)
        layout_principal.addLayout(layout_contenu, 8)

# Programme principal : test de la vue ---------------------------------------
if __name__ == "__main__":

    print(f' --- main --- ')
    app = QApplication(sys.argv)
    
    fenetre = Vue()
    fenetre.show()
    
    sys.exit(app.exec())