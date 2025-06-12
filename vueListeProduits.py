# Formation : BUT 1ʳᵉ année | 2024-2025
# Ressource : SAE S2 - Algo et Graphes
# Professeur : M. Conoir
# Noms :  AMEDRO Louis (TPD)
#         HERBAUX Jules (TPD)
#         GAILLARD Noa (TPC)
#         MINNEBO Valentin (TPA)

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QFileDialog, QApplication, QMessageBox, QScrollArea, QFrame
)
from PyQt6.QtCore import pyqtSignal, Qt
import json
import sys

# -----------------------------------------------------------------------------
# --- class Partie Basse Gauche
# -----------------------------------------------------------------------------

class ListeProduits(QWidget):
    signalProduitSelectionne = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.produitsParCategorie = {}
        self.boutonsProduits = []  # Pour reset sélection
        self.initUI()

    def initUI(self):
        self.layoutPrincipal = QVBoxLayout(self)

        self.boutonOuvrir = QPushButton("Chercher dans mes fichiers")
        self.boutonOuvrir.clicked.connect(self.ouvrirFichier)
        self.layoutPrincipal.addWidget(self.boutonOuvrir, alignment=Qt.AlignmentFlag.AlignCenter)

        self.boutonsGestionLayout = QHBoxLayout()
        self.boutonSupprimer = QPushButton("Supprimer")
        self.boutonChanger = QPushButton("Changer")
        self.boutonSupprimer.clicked.connect(self.confirmerSuppression)
        self.boutonChanger.clicked.connect(self.ouvrirFichier)
        self.boutonsGestionLayout.addWidget(self.boutonSupprimer)
        self.boutonsGestionLayout.addWidget(self.boutonChanger)
        self.layoutPrincipal.addLayout(self.boutonsGestionLayout)
        self.boutonSupprimer.hide()
        self.boutonChanger.hide()

        self.labelTitre = QLabel("Liste Des Produits :")
        self.layoutPrincipal.addWidget(self.labelTitre)
        self.labelTitre.hide()

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scrollContent = QWidget()
        self.scrollLayout = QVBoxLayout(self.scrollContent)
        self.scroll.setWidget(self.scrollContent)
        self.layoutPrincipal.addWidget(self.scroll)
        self.scroll.hide()

    def ouvrirFichier(self):
        chemin, _ = QFileDialog.getOpenFileName(self, "Ouvrir un fichier JSON", "", "JSON Files (*.json)")
        if chemin:
            self.chargerFichier(chemin)

    def chargerFichier(self, chemin):
        with open(chemin, "r", encoding="utf-8") as f:
            self.produitsParCategorie = json.load(f)

        self.clearScroll()
        self.boutonsProduits.clear()

        for categorie, produits in self.produitsParCategorie.items():
            # Bouton de catégorie (fermé par défaut)
            boutonCategorie = QPushButton(f"► {categorie}")
            boutonCategorie.setCheckable(True)
            boutonCategorie.setChecked(False)
            boutonCategorie.setStyleSheet("font-weight: bold; text-align: left;")
            self.scrollLayout.addWidget(boutonCategorie)

            # Contenu de la catégorie (caché par défaut)
            frameContenu = QFrame()
            layoutContenu = QVBoxLayout(frameContenu)
            layoutContenu.setContentsMargins(20, 0, 0, 10)
            frameContenu.setVisible(False)

            for produit in produits:
                boutonProduit = QPushButton(produit)
                boutonProduit.setStyleSheet("text-align: left;")
                boutonProduit.setCheckable(True)
                boutonProduit.clicked.connect(lambda checked, p=produit, b=boutonProduit: self.selectionnerProduit(p, b))
                layoutContenu.addWidget(boutonProduit)
                self.boutonsProduits.append(boutonProduit)

            self.scrollLayout.addWidget(frameContenu)

            # Toggle show/hide
            def toggleContenu(checked, frame=frameContenu, btn=boutonCategorie, cat=categorie):
                frame.setVisible(checked)
                btn.setText(("🔽 " if checked else "▶️ ") + cat)

            boutonCategorie.toggled.connect(toggleContenu)

        self.boutonSupprimer.show()
        self.boutonChanger.show()
        self.labelTitre.show()
        self.scroll.show()
        self.boutonOuvrir.hide()

    def selectionnerProduit(self, nom, boutonClique):
        for bouton in self.boutonsProduits:
            bouton.setChecked(False)
            bouton.setStyleSheet("text-align: left;")

        boutonClique.setChecked(True)
        boutonClique.setStyleSheet("""
            background-color: #ADD8E6;
            font-weight: bold;
            text-align: left;
        """)

        self.signalProduitSelectionne.emit(nom)

    def confirmerSuppression(self):
        confirmation = QMessageBox.question(
            self, "Confirmation", "Êtes-vous sûr de vouloir supprimer la liste en cours ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirmation == QMessageBox.StandardButton.Yes:
            self.reinitialiser()

    def reinitialiser(self):
        self.produitsParCategorie = {}
        self.clearScroll()
        self.boutonSupprimer.hide()
        self.boutonChanger.hide()
        self.labelTitre.hide()
        self.scroll.hide()
        self.boutonOuvrir.show()

    def clearScroll(self):
        while self.scrollLayout.count():
            item = self.scrollLayout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)

# -----------------------------------------------------------------------------
# --- Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":

    print(f' --- main --- ')
    app = QApplication(sys.argv)

    fenetre = ListeProduits()
    fenetre.signalProduitSelectionne.connect(print)
    fenetre.show()

    sys.exit(app.exec())
