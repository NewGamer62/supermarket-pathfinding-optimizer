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
# --- class Partie_basse_droite
# -----------------------------------------------------------------------------
class ContenuCase(QWidget):

    signal_recherche_caractere = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.label_case = QLabel("Séléctionnez une case")

        layout.addWidget(self.label_case)
        
        layout.addStretch()

        self.setLayout(layout)

    def mise_a_jour_case(self, case):
        self.label_case.setText(f"Case : {case}")
        
# Programme principal : test de la vue ---------------------------------------
if __name__ == "__main__":

    print(f' --- main --- ')
    app = QApplication(sys.argv)
    
    fenetre = ContenuCase()
    fenetre.show()
    
    sys.exit(app.exec())