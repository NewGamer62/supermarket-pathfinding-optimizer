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

# -----------------------------------------------------------------------------
# --- class Partie_haute_droite
# -----------------------------------------------------------------------------
class Partie_haute_droite(QWidget):

    signal_recherche_caractere = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.label_nom_fichier = QLabel("📄 Nom Du Fichier")
        self.label_nom_fichier2 = QLineEdit("")
        self.label_nom_auteur = QLabel("✏️ Nom De L’Auteur")
        self.label_nom_auteur2 = QLineEdit("")
        self.label_date = QLabel("📆 Date De Création")
        self.label_date2 = QLineEdit("")
        self.label_nom_projet = QLabel("📁 Nom Du Projet")
        self.label_nom_projet2 = QLineEdit("")
        self.label_adresse_magasin = QLabel("📬️ Adresse Du Magasin")
        self.label_adresse_magasin2 = QLineEdit("")

        layout.addWidget(self.label_nom_fichier)
        layout.addWidget(self.label_nom_fichier2)
        layout.addWidget(self.label_nom_auteur)
        layout.addWidget(self.label_nom_auteur2)
        layout.addWidget(self.label_date)
        layout.addWidget(self.label_date2)
        layout.addWidget(self.label_nom_projet)
        layout.addWidget(self.label_nom_projet2)
        layout.addWidget(self.label_adresse_magasin)
        layout.addWidget(self.label_adresse_magasin2)
        
        layout.addStretch()

        self.setLayout(layout)