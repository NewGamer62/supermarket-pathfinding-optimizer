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
class QLineEditDefault(QLineEdit):
    """QLineEdit qui restaure *default_text* sur perte de focus si vide."""

    def __init__(self, default_text: str = "", parent: QWidget | None = None):
        super().__init__(parent)
        self._default_text = default_text

    # ---------------------------------------------------------------------
    # Événement : perte de focus
    # ---------------------------------------------------------------------
    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        if not self.text().strip():
            self.setText(self._default_text)


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
        self.line_nom_projet = QLineEditDefault("nom_projet.txt")
        self.line_nom_projet.setText("nom_projet.txt")
        btn_clear_projet = self._make_clear_button(self.line_nom_projet)
        row_projet = self._wrap_row(self.line_nom_projet, btn_clear_projet)
        layout.addLayout(row_projet)

        # ----------------------------------------------------------------
        # Nom de l’auteur
        # ----------------------------------------------------------------
        layout.addWidget(QLabel("✏️ Nom De L’Auteur"))
        self.line_nom_auteur = QLineEditDefault("Auteur inconnu")
        self.line_nom_auteur.setText("Auteur inconnu")
        btn_clear_auteur = self._make_clear_button(self.line_nom_auteur)
        row_auteur = self._wrap_row(self.line_nom_auteur, btn_clear_auteur)
        layout.addLayout(row_auteur)

        # ----------------------------------------------------------------
        # Date de création (lecture seule, renseignée automatiquement)
        # ----------------------------------------------------------------
        layout.addWidget(QLabel("📆 Date De Création"))
        self.line_date = QLineEdit(date.today().strftime("%d/%m/%Y"))
        self.line_date.setReadOnly(True)
        layout.addWidget(self.line_date)

        # ----------------------------------------------------------------
        # Nom du magasin
        # ----------------------------------------------------------------
        layout.addWidget(QLabel("🏪 Nom Du Magasin"))
        self.line_nom_magasin = QLineEditDefault("MonMagasin")
        self.line_nom_magasin.setText("MonMagasin")
        btn_clear_magasin = self._make_clear_button(self.line_nom_magasin)
        row_magasin = self._wrap_row(self.line_nom_magasin, btn_clear_magasin)
        layout.addLayout(row_magasin)

        # ----------------------------------------------------------------
        # Adresse du magasin
        # ----------------------------------------------------------------
        layout.addWidget(QLabel("📬️ Adresse Du Magasin"))
        self.line_adresse = QLineEditDefault("0 Rue Exemple, 00000 Ville")
        self.line_adresse.setText("0 Rue Exemple, 00000 Ville")
        btn_clear_adresse = self._make_clear_button(self.line_adresse)
        row_adresse = self._wrap_row(self.line_adresse, btn_clear_adresse)
        layout.addLayout(row_adresse)

        layout.addStretch()

    # ------------------------------------------------------------------
    # Méthodes utilitaires privées
    # ------------------------------------------------------------------
    def _make_clear_button(self, line_edit: QLineEdit) -> QPushButton:
        """Crée un petit bouton ❌ qui vide *line_edit* lorsqu’on clique."""

        button = QPushButton("❌")
        button.setFixedWidth(30)
        button.clicked.connect(line_edit.clear)
        return button

    def _wrap_row(self, *widgets) -> QHBoxLayout:
        """Emballe les *widgets* dans un `QHBoxLayout`."""

        row = QHBoxLayout()
        for w in widgets:
            row.addWidget(w)
        return row

    # ------------------------------------------------------------------
    # Slot public : permet à un autre composant d’injecter le nom de projet
    # ------------------------------------------------------------------
    @pyqtSlot(str)
    def set_nom_projet(self, nom: str) -> None:
        """Remplit le champ *Nom du projet* avec *nom*."""

        self.line_nom_projet.setText(nom)


# ---------------------------------------------------------------------------
# Programme principal (test autonome)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = Informations()
    fenetre.resize(400, 300)
    fenetre.show()
    sys.exit(app.exec())
