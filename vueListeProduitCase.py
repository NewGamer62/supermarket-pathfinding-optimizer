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
    QHBoxLayout, QPushButton, QMessageBox  # Ajout QMessageBox
)
from PyQt6.QtCore import pyqtSignal

# -----------------------------------------------------------------------------
# --- class Partie Basse Droite
# -----------------------------------------------------------------------------

class ContenuCase(QWidget):

    # Signal émettant la liste des produits restants après suppression

    produitsRestantsApresSuppression = pyqtSignal(list)

    def __init__(self):
        super().__init__()

        # --- Mise en page générale --------------------------------------

        self.donneesProduits = {}  
        self.caseActuelle = None
        self.listeProduitsCourante = None  # Ajout pour mémoriser la liste courante si ce n'est pas une case nommée

        mainLayout = QVBoxLayout()
        headerLayout = QHBoxLayout()

        # --- Mise en page spécialisé --------------------------------------
        
        self.labelProduits = QLabel("Liste des produits de la case :")
        self.btnSupprimerTout = QPushButton("❌")
        self.btnSupprimerTout.setVisible(False)  # Caché par défaut
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
        
    def miseAJourCase(self, nomCase):
        # Si on reçoit une liste (produits), on affiche directement cette liste
        if isinstance(nomCase, list):
            self.listeProduitsCourante = list(nomCase)  # Copie pour édition locale
            # Nettoyage
            for i in reversed(range(self.layoutProduits.count())):
                widget = self.layoutProduits.itemAt(i).widget()
                if widget:
                    widget.setParent(None)
            for produit in self.listeProduitsCourante:
                self.ajouterLigneProduit(produit)
            self.caseActuelle = None  # On n'est pas sur une case nommée
            # Affiche ou cache la croix selon si la liste est vide
            self.btnSupprimerTout.setVisible(bool(self.listeProduitsCourante))
            return
        # Accepte aussi une chaîne (nom de case)
        if not isinstance(nomCase, str):
            return
        self.caseActuelle = nomCase
        self.listeProduitsCourante = None
        # Nettoyage
        for i in reversed(range(self.layoutProduits.count())):
            widget = self.layoutProduits.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        # Affichage des produits de la case (tuple)
        produits = self.donneesProduits.get(nomCase, [])
        for produit in produits:
            self.ajouterLigneProduit(produit)
        # Affiche ou cache la croix selon si la liste est vide
        self.btnSupprimerTout.setVisible(bool(produits))


    def miseAJourDonnees(self, dicoProduits: dict):
        self.donneesProduits = dicoProduits
        if self.caseActuelle:
            self.miseAJourCase(self.caseActuelle)

    def ajouterLigneProduit(self, nomProduit: str):
        ligne = QHBoxLayout()
        label = QLabel(f"•  {nomProduit}")
        label.setObjectName("produits")
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
        # Popup de confirmation avant suppression
        message = QMessageBox(self)
        message.setWindowTitle("Confirmation")
        message.setText("Voulez-vous vraiment supprimer tous les produits de la case ?")
        oui = message.addButton("Oui", QMessageBox.ButtonRole.YesRole)
        non = message.addButton("Non", QMessageBox.ButtonRole.NoRole)
        message.setDefaultButton(non)
        message.exec()
        if message.clickedButton() != oui:
            return
        # Cas où on affiche une liste directe (case rouge, pas une case nommée)
        if self.listeProduitsCourante is not None:
            self.listeProduitsCourante.clear()
            # Nettoyage affichage
            for i in reversed(range(self.layoutProduits.count())):
                widget = self.layoutProduits.itemAt(i).widget()
                if widget:
                    widget.setParent(None)
            # Émet la liste vide pour synchroniser le plan
            self.produitsRestantsApresSuppression.emit([])
            return
        # Cas classique : suppression dans le dico
        if self.caseActuelle in self.donneesProduits:
            self.donneesProduits[self.caseActuelle] = []
            self.miseAJourCase(self.caseActuelle)
            self.produitsRestantsApresSuppression.emit([])

    def supprimerProduit(self, produit: str):
        # Cas où on affiche une liste directe (case rouge, pas une case nommée)
        if self.listeProduitsCourante is not None:
            if produit in self.listeProduitsCourante:
                self.listeProduitsCourante.remove(produit)
                # Rafraîchit l'affichage
                for i in reversed(range(self.layoutProduits.count())):
                    widget = self.layoutProduits.itemAt(i).widget()
                    if widget:
                        widget.setParent(None)
                for p in self.listeProduitsCourante:
                    self.ajouterLigneProduit(p)
                # Émet la nouvelle liste au plan (qui mettra à jour la vraie source)
                self.produitsRestantsApresSuppression.emit(self.listeProduitsCourante)
            return
        # Cas classique : suppression dans le dico
        if self.caseActuelle in self.donneesProduits:
            if produit in self.donneesProduits[self.caseActuelle]:
                self.donneesProduits[self.caseActuelle].remove(produit)
                self.miseAJourCase(self.caseActuelle)
                self.produitsRestantsApresSuppression.emit(self.donneesProduits[self.caseActuelle])

# -----------------------------------------------------------------------------
# --- Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":

    app = QApplication(sys.argv)
    fenetre = ContenuCase()

    fenetre.show()
    sys.exit(app.exec())
