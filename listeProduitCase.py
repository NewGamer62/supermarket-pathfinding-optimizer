# Formation : BUT 1ʳᵉ année | 2024-2025
# Ressource : SAE S2 - Algo et Graphes
# Professeur : M. Conoir
# Noms :  AMEDRO Louis (TPD)
#         HERBAUX Jules (TPD)
#         GAILLARD Noa (TPC)
#         MINNEBO Valentin (TPA)

import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QApplication,
    QHBoxLayout, QPushButton
)
from PyQt6.QtCore import pyqtSignal


import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QApplication,
    QHBoxLayout, QPushButton
)
from PyQt6.QtCore import pyqtSignal

# -----------------------------------------------------------------------------
# --- class Partie_basse_droite
# -----------------------------------------------------------------------------

class ContenuCase(QWidget):

    # Signal émettant la liste des produits restants après suppression

    produitsRestantsApresSuppression = pyqtSignal(list)

    def __init__(self):
        super().__init__()

        # --- Mise en page générale --------------------------------------

        self.donneesProduits = {}  
        self.caseActuelle = None

        mainLayout = QVBoxLayout()
        headerLayout = QHBoxLayout()

        # --- Mise en page spécialisé --------------------------------------
        
        self.labelProduits = QLabel("Liste des produits de la case :")
        self.btnSupprimerTout = QPushButton("❌")
        self.btnSupprimerTout.setFixedWidth(30)
        self.btnSupprimerTout.clicked.connect(self.supprimerTousLesProduits)

        headerLayout.addWidget(self.labelProduits)
        headerLayout.addStretch()
        headerLayout.addWidget(self.btnSupprimerTout)

        mainLayout.addLayout(headerLayout)

        self.layoutProduits = QVBoxLayout()
        mainLayout.addLayout(self.layoutProduits)

        mainLayout.addStretch()
        self.setLayout(mainLayout)

    def miseAJourDonnees(self, dicoProduits: dict):
        self.donneesProduits = dicoProduits
        if self.caseActuelle:
            self.miseAJourCase(self.caseActuelle)

    def miseAJourCase(self, nomCase: str):
        self.caseActuelle = nomCase

        # ---------------------------------------------------------------------------
        # Nettoyage
        # ---------------------------------------------------------------------------

        for i in reversed(range(self.layoutProduits.count())):
            widget = self.layoutProduits.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        produits = self.donneesProduits.get(nomCase, [])
        for produit in produits:
            self.ajouterLigneProduit(produit)

    def ajouterLigneProduit(self, nomProduit: str):
        ligne = QHBoxLayout()
        label = QLabel(f"•  {nomProduit}")
        bouton = QPushButton("❌")
        bouton.setFixedWidth(30)

        bouton.clicked.connect(lambda _, p=nomProduit: self.supprimerProduit(p))

        ligne.addWidget(label)
        ligne.addStretch()
        ligne.addWidget(bouton)

        ligneWidget = QWidget()
        ligneWidget.setLayout(ligne)
        self.layoutProduits.addWidget(ligneWidget)

    def supprimerTousLesProduits(self):
        if self.caseActuelle in self.donneesProduits:
            self.donneesProduits[self.caseActuelle] = []
            self.miseAJourCase(self.caseActuelle)
            self.produitsRestantsApresSuppression.emit([])

    def supprimerProduit(self, produit: str):
        if self.caseActuelle in self.donneesProduits:
            if produit in self.donneesProduits[self.caseActuelle]:
                self.donneesProduits[self.caseActuelle].remove(produit)
                self.miseAJourCase(self.caseActuelle)
                self.produitsRestantsApresSuppression.emit(self.donneesProduits[self.caseActuelle])

# -----------------------------------------------------------------------------
# --- Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    def afficherListeProduits(produits):
        print(f"[Signal] Produits restants : {produits}")

    app = QApplication(sys.argv)
    fenetre = ContenuCase()
    fenetre.produitsRestantsApresSuppression.connect(afficherListeProduits)

    fenetre.miseAJourDonnees({
        "A1": ["lait", "riz", "pâtes"],
        "B2": ["sucre"]
    })
    fenetre.miseAJourCase("A1")

    fenetre.show()
    sys.exit(app.exec())
