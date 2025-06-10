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
# --- class Partie Centre
# -----------------------------------------------------------------------------

class Plan(QWidget):

    signal_ouvrir = pyqtSignal()
    signal_enregistrer = pyqtSignal()
    signal_effacer = pyqtSignal()
    signal_texte_modifie = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.editeur = QTextEdit()
        layout_boutons = QHBoxLayout()

        self.bouton_ouvrir = QPushButton("Ouvrir")
        self.bouton_enregistrer = QPushButton("Enregistrer")
        self.bouton_effacer = QPushButton("Effacer")

        layout_boutons.addWidget(self.bouton_ouvrir)
        layout_boutons.addWidget(self.bouton_enregistrer)
        layout_boutons.addWidget(self.bouton_effacer)

        layout.addWidget(self.editeur)
        layout.addLayout(layout_boutons)
        self.setLayout(layout)

        # Connexion des boutons
        self.bouton_ouvrir.clicked.connect(self.signal_ouvrir.emit)
        self.bouton_enregistrer.clicked.connect(self.signal_enregistrer.emit)
        self.bouton_effacer.clicked.connect(self.signal_effacer.emit)
        self.editeur.textChanged.connect(self._texte_change)

    def _texte_change(self):
        self.signal_texte_modifie.emit(self.editeur.toPlainText())

    def afficher_texte(self, texte):
        self.editeur.blockSignals(True)
        self.editeur.setPlainText(texte)
        self.editeur.blockSignals(False)
        
# Programme principal : test de la vue ---------------------------------------
if __name__ == "__main__":

    print(f' --- main --- ')
    app = QApplication(sys.argv)
    
    fenetre = Plan()
    fenetre.show()
    
    sys.exit(app.exec())