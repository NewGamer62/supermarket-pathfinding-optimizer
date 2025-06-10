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
# --- class Partie gauche
# -----------------------------------------------------------------------------

class Partie_gauche(QWidget):

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

# -----------------------------------------------------------------------------
# --- class Partie Centre
# -----------------------------------------------------------------------------

class Partie_centre(QWidget):

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


# -----------------------------------------------------------------------------
# --- class Partie_haute_droite
# -----------------------------------------------------------------------------
class Partie_haute_droite(QWidget):

    signal_recherche_caractere = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.label_nom_fichier = QLabel("📄 Nom Du Fichier")
        self.label_nom_fichier2 = QLineEdit("")
        self.label_nom_auteur = QLabel("✏️ Nom De L’Auteur")
        self.label_nom_auteur2 = QLineEdit("")
        self.label_date = QLabel("📆 Date De Création")
        self.label_date2 = QLineEdit("")
        self.label_nom_projet = QLabel("📁 Nom Du Projet")
        self.label_nom_projet2 = QLineEdit("")
        self.label_adresse_magasin = QLabel("📬️ Adresse Du Magasin")
        self.label_adresse_magasin2 = QLineEdit("")

        layout.addWidget(self.label_nom_fichier)
        layout.addWidget(self.label_nom_fichier2)
        layout.addWidget(self.label_nom_auteur)
        layout.addWidget(self.label_nom_auteur2)
        layout.addWidget(self.label_date)
        layout.addWidget(self.label_date2)
        layout.addWidget(self.label_nom_projet)
        layout.addWidget(self.label_nom_projet2)
        layout.addWidget(self.label_adresse_magasin)
        layout.addWidget(self.label_adresse_magasin2)
        
        layout.addStretch()

        self.setLayout(layout)

# -----------------------------------------------------------------------------
# --- class Partie_basse_droite
# -----------------------------------------------------------------------------
class Partie_basse_droite(QWidget):

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

# -----------------------------------------------------------------------------
# --- class Vue
# -----------------------------------------------------------------------------
class Vue(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Super Créateur de Magasin 3000")
        self.setMinimumSize(600, 400)

        layout_principal = QHBoxLayout()
        self.partie_gauche = Partie_gauche()
        self.partie_centre = Partie_centre()
        self.partie_haute_droite = Partie_haute_droite()
        self.partie_basse_droite = Partie_basse_droite()

        layout_principal.addWidget(self.partie_gauche, 3)
        layout_principal.addWidget(self.partie_centre, 2)
        layout_principal.addWidget(self.partie_haute_droite, 1)
        layout_principal.addWidget(self.partie_basse_droite, 1)

        self.setLayout(layout_principal)

# Programme principal : test de la vue ---------------------------------------
if __name__ == "__main__":

    print(f' --- main --- ')
    app = QApplication(sys.argv)
    
    fenetre = Vue()
    fenetre.show()
    
    sys.exit(app.exec())