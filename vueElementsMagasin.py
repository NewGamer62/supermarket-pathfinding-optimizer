# Formation : BUT 1ʳᵉ année | 2024-2025
# Ressource : SAE S2 - Algo et Graphes
# Professeur : M. Conoir
# Noms :  AMEDRO Louis (TPD)
#         HERBAUX Jules (TPD)
#         GAILLARD Noa (TPC)
#         MINNEBO Valentin (TPA)

import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QApplication)
from PyQt6.QtCore import pyqtSignal

# ----------------------------------------------------------------------------- 
# --- class Partie Haute Gauche
# -----------------------------------------------------------------------------

class ElementsMagasin(QWidget):

    signal_element = pyqtSignal(str)  # ✅ Signal général pour envoyer "Mur", "Caisse", "Entree"

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Mur
        self.mettreMur = QPushButton("🧱 Mettre un mur")
        self.mettreMur.setCheckable(True)
        layout.addWidget(self.mettreMur)
        self.mettreMur.clicked.connect(lambda: self.selectionner("mur", self.mettreMur))

        # Caisse
        self.mettreCaisse = QPushButton("💰️ Mettre une caisse")
        self.mettreCaisse.setCheckable(True)
        layout.addWidget(self.mettreCaisse)
        self.mettreCaisse.clicked.connect(lambda: self.selectionner("caisse", self.mettreCaisse))

        # Entrée
        self.mettreEntree = QPushButton("⬆️ Mettre une entrée")
        self.mettreEntree.setCheckable(True)
        layout.addWidget(self.mettreEntree)
        self.mettreEntree.clicked.connect(lambda: self.selectionner("entree", self.mettreEntree))

        self.boutons = [self.mettreMur, self.mettreCaisse, self.mettreEntree]
        
    #=========================
    # --- Méthodes
    #=========================

    def selectionner(self, type_case, boutonClique):
        # Désélectionne tous les boutons sauf celui cliqué
        for bouton in self.boutons:
            if bouton is not boutonClique:
                bouton.setChecked(False)
                bouton.setStyleSheet("")
        # Met en surbrillance le bouton sélectionné
        if boutonClique.isChecked():
            boutonClique.setStyleSheet("background-color: #ADD8E6; font-weight: bold;")
            self.signal_element.emit(type_case)
        else:
            boutonClique.setStyleSheet("")
            self.signal_element.emit("") # Si aucun bouton n'est sélectionné, on peut émettre rien

# ----------------------------------------------------------------------------- 
# --- Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    def afficher_element(element):
        print(f"🛠️ Élément choisi : {element}")

    print(f' --- main --- ')
    app = QApplication(sys.argv)

    fenetre = ElementsMagasin()
    fenetre.signal_element.connect(afficher_element)  # 🔗 Connexion du signal au slot
    fenetre.show()

    sys.exit(app.exec())
