# Formation : BUT 1ʳᵉ année | 2024-2025
# Ressource : SAE S2 - Algo et Graphes
# Professeur : M. Conoir
# Noms :  AMEDRO Louis (TPD)
#         HERBAUX Jules (TPD)
#         GAILLARD Noa (TPC)
#         MINNEBO Valentin (TPA)

import sys
from datetime import date
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import (QApplication,QLabel,QHBoxLayout,QLineEdit,QPushButton,QVBoxLayout,QWidget)

# ---------------------------------------------------------------------------
# QLineEdit personnalisé : remet un texte par défaut si l’utilisateur
#                         quitte la case en laissant le champ vide.
# ---------------------------------------------------------------------------

class QLineEditParDefaut(QLineEdit):
    """QLineEdit qui restaure *texteParDefaut* sur perte de focus si vide."""

    def __init__(self, texteParDefaut: str = "", parent: QWidget | None = None):
        super().__init__(parent)
        self._texteParDefaut = texteParDefaut

    # ---------------------------------------------------------------------
    # Événement : perte de focus
    # ---------------------------------------------------------------------

    def focusOutEvent(self, evenement):
        super().focusOutEvent(evenement)
        if not self.text().strip():
            self.setText(self._texteParDefaut)


# ---------------------------------------------------------------------------
# Vue Informations
# ---------------------------------------------------------------------------

class Informations(QWidget):
    """Zone d’informations située en haut à droite de l’application."""

    def __init__(self) -> None:
        super().__init__()

        # --- Mise en page générale --------------------------------------

        layout = QVBoxLayout()
        self.setLayout(layout)

        # ----------------------------------------------------------------
        # Nom du projet
        # ----------------------------------------------------------------

        layout.addWidget(QLabel("📁 Nom Du Projet"))
        self.ligneNomProjet = QLineEditParDefaut("nom_projet.txt")
        self.ligneNomProjet.setText("nom_projet.txt")
        boutonSupprProjet = self._boutonSuppr(self.ligneNomProjet)
        rangeeProjet = self._envelopperRangee(self.ligneNomProjet, boutonSupprProjet)
        layout.addLayout(rangeeProjet)

        # ----------------------------------------------------------------
        # Nom de l’auteur
        # ----------------------------------------------------------------

        layout.addWidget(QLabel("✏️ Nom De L’Auteur"))
        self.ligneNomAuteur = QLineEditParDefaut("Auteur inconnu")
        self.ligneNomAuteur.setText("Auteur inconnu")
        boutonSupprAuteur = self._boutonSuppr(self.ligneNomAuteur)
        rangeeAuteur = self._envelopperRangee(self.ligneNomAuteur, boutonSupprAuteur)
        layout.addLayout(rangeeAuteur)

        # ----------------------------------------------------------------
        # Date de création (lecture seule, renseignée automatiquement)
        # ----------------------------------------------------------------

        layout.addWidget(QLabel("📆 Date De Création"))
        self.ligneDate = QLineEdit(date.today().strftime("%d/%m/%Y"))
        self.ligneDate.setReadOnly(True)
        layout.addWidget(self.ligneDate)

        # ----------------------------------------------------------------
        # Nom du magasin
        # ----------------------------------------------------------------

        layout.addWidget(QLabel("🏪 Nom Du Magasin"))
        self.ligneNomMagasin = QLineEditParDefaut("MonMagasin")
        self.ligneNomMagasin.setText("MonMagasin")
        boutonSupprMagasin = self._boutonSuppr(self.ligneNomMagasin)
        rangeeMagasin = self._envelopperRangee(self.ligneNomMagasin, boutonSupprMagasin)
        layout.addLayout(rangeeMagasin)

        # ----------------------------------------------------------------
        # Adresse du magasin
        # ----------------------------------------------------------------

        layout.addWidget(QLabel("📬️ Adresse Du Magasin"))
        self.ligneAdresse = QLineEditParDefaut("0 Rue Exemple, 00000 Ville")
        self.ligneAdresse.setText("0 Rue Exemple, 00000 Ville")
        boutonSupprAdresse = self._boutonSuppr(self.ligneAdresse)
        rangeeAdresse = self._envelopperRangee(self.ligneAdresse, boutonSupprAdresse)
        layout.addLayout(rangeeAdresse)

        layout.addStretch()

    # ------------------------------------------------------------------
    # Méthodes utilitaires privées
    # ------------------------------------------------------------------

    def _boutonSuppr(self, ligneModifier: QLineEdit) -> QPushButton:
        """Crée un petit bouton ❌ qui vide *ligneModifier* et lui redonne le focus."""

        boutton = QPushButton("❌")
        boutton.setFixedWidth(30)

        def nettoyerEtPreparer():
            ligneModifier.clear()
            ligneModifier.setFocus()

        boutton.clicked.connect(nettoyerEtPreparer)
        return boutton


    def _envelopperRangee(self, *widgets) -> QHBoxLayout:
        """Emballe les *widgets* dans un `QHBoxLayout`."""

        rangee = QHBoxLayout()
        for w in widgets:
            rangee.addWidget(w)
        return rangee

    # ------------------------------------------------------------------
    # Slot public : permet à un autre composant d’injecter le nom de projet
    # ------------------------------------------------------------------

    @pyqtSlot(str)
    def setNomProjet(self, nom: str) -> None:
        """Remplit le champ *Nom du projet* avec *nom*."""

        self.ligneNomProjet.setText(nom)


# ---------------------------------------------------------------------------
# Programme principal (test autonome)
# ---------------------------------------------------------------------------

if __name__ == "__main__":

    print(f' --- main --- ')
    app = QApplication(sys.argv)

    fenetre = Informations()
    fenetre.resize(400, 300)
    fenetre.show()

    sys.exit(app.exec())
