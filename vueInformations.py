# Formation : BUT 1ʳᵉ année | 2024-2025
# Ressource : SAE S2 - Algo et Graphes
# Professeur : M. Conoir
# Noms :  AMEDRO Louis (TPD)
#         HERBAUX Jules (TPD)
#         GAILLARD Noa (TPC)
#         MINNEBO Valentin (TPA)

import sys
from datetime import date, datetime
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

        # --- Valeurs par défaut cohérentes avec le modèle ---
        nom_defaut = "Projet sans Nom"
        auteur_defaut = "Auteur Inconnu"
        date_defaut = datetime.now().date().strftime("%d/%m/%Y")
        nom_magasin_defaut = "Supermarché Inconnu"
        adresse_defaut = "Adresse Inconnue"

        # --- Mise en page générale --------------------------------------

        layout = QVBoxLayout()
        self.setLayout(layout)

        # ----------------------------------------------------------------
        # Nom du projet
        # ----------------------------------------------------------------

        layout.addWidget(QLabel("📁 Nom Du Projet"))
        self.ligneNomProjet = QLineEditParDefaut(nom_defaut)
        self.ligneNomProjet.setText(nom_defaut)
        boutonSupprProjet = self._boutonSuppr(self.ligneNomProjet)
        rangeeProjet = self._envelopperRangee(self.ligneNomProjet, boutonSupprProjet)
        layout.addLayout(rangeeProjet)

        # ----------------------------------------------------------------
        # Nom de l’auteur
        # ----------------------------------------------------------------

        layout.addWidget(QLabel("✏️ Nom De L’Auteur"))
        self.ligneNomAuteur = QLineEditParDefaut(auteur_defaut)
        self.ligneNomAuteur.setText(auteur_defaut)
        boutonSupprAuteur = self._boutonSuppr(self.ligneNomAuteur)
        rangeeAuteur = self._envelopperRangee(self.ligneNomAuteur, boutonSupprAuteur)
        layout.addLayout(rangeeAuteur)

        # ----------------------------------------------------------------
        # Date de création (lecture seule, renseignée automatiquement)
        # ----------------------------------------------------------------

        layout.addWidget(QLabel("📆 Date De Création"))
        self.ligneDate = QLineEdit(date_defaut)
        self.ligneDate.setReadOnly(True)
        layout.addWidget(self.ligneDate)

        # ----------------------------------------------------------------
        # Nom du magasin
        # ----------------------------------------------------------------

        layout.addWidget(QLabel("🏪 Nom Du Magasin"))
        self.ligneNomMagasin = QLineEditParDefaut(nom_magasin_defaut)
        self.ligneNomMagasin.setText(nom_magasin_defaut)
        boutonSupprMagasin = self._boutonSuppr(self.ligneNomMagasin)
        rangeeMagasin = self._envelopperRangee(self.ligneNomMagasin, boutonSupprMagasin)
        layout.addLayout(rangeeMagasin)

        # ----------------------------------------------------------------
        # Adresse du magasin
        # ----------------------------------------------------------------

        layout.addWidget(QLabel("📬️ Adresse Du Magasin"))
        self.ligneAdresse = QLineEditParDefaut(adresse_defaut)
        self.ligneAdresse.setText(adresse_defaut)
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

    def getInfos(self) -> dict:
        """Retourne un dictionnaire avec les informations saisies dans la vue."""
        return {
            "nom": self.ligneNomProjet.text(),
            "auteur": self.ligneNomAuteur.text(),
            "date création": self.ligneDate.text(),
            "nom supermarché": self.ligneNomMagasin.text(),
            "adresse supermarché": self.ligneAdresse.text()
        }

    def setInfos(self, infos: dict) -> None:
        """Met à jour les champs de la vue avec les informations fournies."""
        self.ligneNomProjet.setText(infos.get("nom", ""))
        self.ligneNomAuteur.setText(infos.get("auteur", ""))
        date_val = infos.get("date création", "")
        # Conversion de la date si besoin
        if hasattr(date_val, "strftime"):
            date_str = date_val.strftime("%d/%m/%Y")
        else:
            date_str = str(date_val)
        self.ligneDate.setText(date_str)
        self.ligneNomMagasin.setText(infos.get("nom supermarché", ""))
        self.ligneAdresse.setText(infos.get("adresse supermarché", ""))

# ---------------------------------------------------------------------------
# --- Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":

    print(f' --- main --- ')
    app = QApplication(sys.argv)

    fenetre = Informations()
    fenetre.resize(400, 300)
    fenetre.show()

    sys.exit(app.exec())
