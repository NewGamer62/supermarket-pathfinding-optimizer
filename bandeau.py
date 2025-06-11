# Formation : BUT 1ʳᵉ année | 2024-2025
# Ressource : SAE S2 - Algo et Graphes
# Professeur : M. Conoir
# Noms :  AMEDRO Louis (TPD)
#         HERBAUX Jules (TPD)
#         GAILLARD Noa (TPC)
#         MINNEBO Valentin (TPA)

import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QMenuBar, QMenu, QLabel, QWidget, QVBoxLayout)
from PyQt6.QtGui import QAction

# -----------------------------------------------------------------------------
# --- class Bandeau
# -----------------------------------------------------------------------------

class Bandeau(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setMinimumSize(800, 600)

        # Initialisation du bandeau
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        # Entête de menus
        fichier_menu = QMenu("Fichier", self)
        edition_menu = QMenu("Édition", self)
        affichage_menu = QMenu("Affichage", self)

        # Ajout des menus à la barre
        menu_bar.addMenu(fichier_menu)
        menu_bar.addMenu(edition_menu)
        menu_bar.addMenu(affichage_menu)

        # Actions pour "Fichier"
        fichier_menu.addAction(QAction("Nouveau", self))
        fichier_menu.addAction(QAction("Ouvrir", self))
        fichier_menu.addAction(QAction("Enregistrer", self))

        # Actions pour "Édition"
        edition_menu.addAction(QAction("Copier", self))
        edition_menu.addAction(QAction("Coller", self))
        edition_menu.addAction(QAction("Couper", self))

        # Actions pour "Affichage"
        affichage_menu.addAction(QAction("Zoom", self))
        affichage_menu.addAction(QAction("Plein écran", self))

if __name__ == "__main__":

    print(f' --- main --- ')
    app = QApplication(sys.argv)
    
    fenetre = Bandeau()
    fenetre.show()

    sys.exit(app.exec())
