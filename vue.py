# Formation : BUT 1ʳᵉ année | 2024-2025
# Ressource : SAE S2 - Algo et Graphes
# Professeur : M. Conoir
# Noms :  AMEDRO Louis (TPD)
#         HERBAUX Jules (TPD)
#         GAILLARD Noa (TPC)
#         MINNEBO Valentin (TPA)

import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLabel, QPushButton, QLineEdit
from PyQt6.QtCore import pyqtSignal
import vueBandeau, vueElementsMagasin, vueInformations, vueListeProduitCase, vueListeProduits, vuePlan
import os

# -----------------------------------------------------------------------------
# --- class Vue
# -----------------------------------------------------------------------------

class Vue(QWidget):

    # Signaux pour le contrôleur
    OuvertureFichier = pyqtSignal(str)
    EnregistrerFichier = pyqtSignal(str)
    changementCase = pyqtSignal(int, int, list)
    changementInfos = pyqtSignal(dict)
    matrice_generee = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Éditeur de Magasin")
        self.setMinimumSize(600, 400)

        # Layout principal :
        layout_principal = QVBoxLayout()
        self.setLayout(layout_principal)

        # Instanciation des widgets
        self.bandeau = vueBandeau.Bandeau()
        self.bandeau.setFixedHeight(40)  # Hauteur réduite du bandeau
        self.elementsMagasin = vueElementsMagasin.ElementsMagasin()
        self.informations = vueInformations.Informations()
        self.listeProduitCase = vueListeProduitCase.ContenuCase()
        self.listeProduits = vueListeProduits.ListeProduits()
        self.plan = vuePlan.Plan()

        # Layouts gauche :
        layout_gauche = QVBoxLayout()
        layout_gauche.addWidget(self.elementsMagasin)
        layout_gauche.addWidget(self.listeProduits)

        layout_droite = QVBoxLayout()
        layout_droite.addWidget(self.informations)
        layout_droite.addWidget(self.listeProduitCase)

        # Layout horizontal principal pour le contenu central
        layout_contenu = QHBoxLayout()
        layout_contenu.addLayout(layout_gauche, 2)
        layout_contenu.addWidget(self.plan, 4)
        layout_contenu.addLayout(layout_droite, 2)

        # Ajout des widgets et layouts dans le layout principal
        layout_principal.addWidget(self.bandeau)
        layout_principal.addLayout(layout_contenu, 8)

        # Connexions de signaux/slots entre widgets

        # 1. Boutons "mur/caisse/entree" -> type de case à placer sur le plan
        self.elementsMagasin.signal_element.connect(self.plan.image_widget.recevoir_signal_type_case)
        self.elementsMagasin.signal_element.connect(self.deselectionner_produit_liste)

        # 2. Sélection d'une case produit sur le plan -> affichage dans la partie droite
        self.plan.image_widget.produits_case_selectionnee.connect(self.listeProduitCase.miseAJourCase)

        # 3. Suppression d'un produit dans la liste de la case -> mise à jour des produits sur le plan
        self.listeProduitCase.produitsRestantsApresSuppression.connect(self.plan.image_widget.mettre_a_jour_produits_case)

        # 4. Sélection d'un produit dans la liste de gauche -> ajout sur la case sélectionnée du plan
        self.listeProduits.signalProduitSelectionne.connect(self.plan.image_widget.recevoir_signal_produit)
        self.listeProduits.signalProduitSelectionne.connect(self.deselectionner_element_magasin)

        # 5. Signal matrice_generee du plan (émis à chaque modif) -> slot pour traitement éventuel (exemple)
        # self.plan.image_widget.matrice_generee.connect(self.votre_slot_pour_traiter_la_matrice)

        # Connexion du signal plein écran
        self.bandeau.signalPleinEcran.connect(self.modePleinEcran)

        # Connexion des signaux du bandeau pour le contrôleur
        self.bandeau.signalFichier.connect(self.OuvertureFichier)
        self.bandeau.signalEnregistrer.connect(self.EnregistrerFichier)
        self.bandeau.signalEnregistrerSous.connect(self.EnregistrerFichier)

        # Connexion du signal matrice_generee du plan pour le contrôleur
        self.plan.image_widget.matrice_generee.connect(self.matrice_generee)

        # Exemple de connexion pour changementCase (à adapter selon votre logique)
        # Ici, on suppose que la suppression/ajout de produits sur une case doit émettre ce signal
        self.plan.image_widget.produits_case_selectionnee.connect(self._emission_changement_case)
        self.listeProduitCase.produitsRestantsApresSuppression.connect(self._maj_case_depuis_vue)

        # Appliquer le style clair à toute l'application si le fichier existe
        qss_path = os.path.join(os.path.dirname(__file__), "style", "Clair.qss")
        if os.path.exists(qss_path):
            with open(qss_path, "r", encoding="utf-8") as f:
                qss = f.read()
                # Nettoyage du QSS : retire les lignes JSON ou autres non-QSS
                qss = "\n".join(line for line in qss.splitlines() if not line.strip().startswith('"files.associations"') and not line.strip().startswith("{") and not line.strip().startswith("}"))
                app = QApplication.instance()
                if app is not None:
                    app.setStyleSheet(qss)
                else:
                    self.setStyleSheet(qss)

    def _emission_changement_case(self, produits):
        # Cette méthode doit être adaptée pour émettre les coordonnées et la liste de produits
        # Il faut mémoriser la dernière case sélectionnée dans le plan
        if hasattr(self.plan.image_widget, "_derniere_case") and self.plan.image_widget._derniere_case is not None:
            col, lig = self.plan.image_widget._derniere_case
            self.changementCase.emit(col, lig, produits)

    def _maj_case_depuis_vue(self, produits):
        # Quand la liste de produits d'une case change (suppression), on émet le signal changementCase
        if hasattr(self.plan.image_widget, "_derniere_case") and self.plan.image_widget._derniere_case is not None:
            col, lig = self.plan.image_widget._derniere_case
            self.changementCase.emit(col, lig, produits)

    def deselectionner_produit_liste(self, *_):
        # Déselectionne tout produit dans la liste de produits
        for bouton in self.listeProduits.boutonsProduits:
            bouton.setChecked(False)
            bouton.setStyleSheet("text-align: left;")
            bouton.setProperty("selectionne", False)

    def deselectionner_element_magasin(self, *_):
        # Déselectionne tous les boutons d'éléments magasin
        for bouton in self.elementsMagasin.boutons:
            bouton.setChecked(False)
            bouton.setStyleSheet("")

    def modePleinEcran(self, checked):
        if checked:
            self.showFullScreen()
        else:
            self.showNormal()

# Programme principal : test de la vue ---------------------------------------
if __name__ == "__main__":

    print(f' --- main --- ')
    app = QApplication(sys.argv)
    
    fenetre = Vue()
    fenetre.show()
    
    sys.exit(app.exec())