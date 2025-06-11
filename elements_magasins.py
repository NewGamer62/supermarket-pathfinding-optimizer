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
# --- class Partie_haute_gauche
# -----------------------------------------------------------------------------
class ElementsMagasin(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        mettreMur = QPushButton("Mettre un mur")
        mettreCaisse = QPushButton("Mettre une caisse")
        mettreEntree = QPushButton("Mettre une entrée")


# Programme principal : test de la vue ---------------------------------------
if __name__ == "__main__":

    print(f' --- main --- ')
    app = QApplication(sys.argv)
    
    fenetre = ElementsMagasin()
    fenetre.show()
    
    sys.exit(app.exec())