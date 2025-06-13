# Formation : BUT 1ʳᵉ année | 2024-2025
# Ressource : SAE S2 - Algo et Graphes
# Professeur : M. Conoir
# Noms :  AMEDRO Louis (TPD)
#         HERBAUX Jules (TPD)
#         GAILLARD Noa (TPC)
#         MINNEBO Valentin (TPA)

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QMenuBar, QMenu, QLabel, QWidget, QVBoxLayout,
    QMessageBox, QFileDialog
)
from PyQt6.QtGui import QAction, QDesktopServices
from PyQt6.QtCore import Qt, QUrl, pyqtSignal
import os


# ---------------------------------------------------------------------------
# --- class Bandeau
# ---------------------------------------------------------------------------

class Bandeau(QMainWindow):

    signalFichier = pyqtSignal(str)
    signalEnregistrer = pyqtSignal(str)
    signalEnregistrerSous = pyqtSignal(str)
    signalPleinEcran = pyqtSignal(bool)  # Ajout d'un signal

    def __init__(self):
        super().__init__()

        self.setMinimumSize(800, 600)
        self.etatPleinEcran = False
        self.cheminFichierActuel = None  # chemin courant

        # Menu Bar
        menuBar = QMenuBar(self)
        self.setMenuBar(menuBar)

        # Menus principaux
        fichierMenu = QMenu("Fichier", self)
        creditMenu = QMenu("Crédit", self)
        affichageMenu = QMenu("Affichage", self)

        menuBar.addMenu(fichierMenu)
        menuBar.addMenu(affichageMenu)
        menuBar.addMenu(creditMenu)

        # --- Actions pour "Fichier" ---
        ouvrirAction = QAction("📂 Ouvrir", self)
        ouvrirAction.triggered.connect(self.ouvrirDossier)
        fichierMenu.addAction(ouvrirAction)

        enregistrerAction = QAction("💾 Enregistrer", self)
        enregistrerAction.triggered.connect(self.enregistrerFichier)
        fichierMenu.addAction(enregistrerAction)

        enregistrerSousAction = QAction("📝 Enregistrer sous", self)
        enregistrerSousAction.triggered.connect(self.enregistrerSous)
        fichierMenu.addAction(enregistrerSousAction)

        # --- Actions pour "Crédit" ---
        creditAction = QAction("👥 Voir", self)
        creditAction.triggered.connect(self.afficherCredits)
        creditMenu.addAction(creditAction)

        faire_don = QAction("💰️ Faire un don", self)
        faire_don.triggered.connect(self.don)
        creditMenu.addAction(faire_don)
        
        # --- Actions pour le style clair/sombre ---
        self.action_style_clair = QAction("🌞 Style clair", self)
        self.action_style_clair.setCheckable(True)
        self.action_style_sombre = QAction("🌙 Style sombre", self)
        self.action_style_sombre.setCheckable(True)

        # --- Action "Plein écran" ---
        self.action_fullscreen = QAction("🖥️ Plein écran", self)
        self.action_fullscreen.setCheckable(True)
        self.action_fullscreen.triggered.connect(self.demanderPleinEcran)
        affichageMenu.addAction(self.action_fullscreen)        

        # Groupe exclusif pour les styles
        self.action_style_clair.setChecked(True)  # Par défaut
        self.action_style_clair.triggered.connect(lambda: self.appliquerStyle("Clair"))
        self.action_style_sombre.triggered.connect(lambda: self.appliquerStyle("Sombre"))

        affichageMenu.addAction(self.action_style_clair)
        affichageMenu.addAction(self.action_style_sombre)

        # Appliquer le style clair au démarrage
        self.appliquerStyle("Clair")

    # --- Méthode pour ouvrir un dossier ---
    def ouvrirDossier(self):
        chemin = QFileDialog.getExistingDirectory(self, "Ouvrir un dossier", "")
        if chemin:
            self.cheminFichierActuel = chemin
            self.signalFichier.emit(chemin)

    # --- Méthode pour enregistrer directement ---
    def enregistrerFichier(self):
        if self.cheminFichierActuel:
            print(f"[DEBUG] Enregistrement : {self.cheminFichierActuel}")
            self.signalEnregistrer.emit(self.cheminFichierActuel)
        else:
            self.enregistrerSous()

    # --- Méthode pour "Enregistrer sous" ---
    def enregistrerSous(self):
        chemin = QFileDialog.getExistingDirectory(self, "Enregistrer dans un dossier", "")
        if chemin:
            print(f"[DEBUG] Enregistrer sous : {chemin}")
            self.cheminFichierActuel = chemin
            self.signalEnregistrerSous.emit(chemin)

    # --- Méthode pour gérer le plein écran ---
    def demanderPleinEcran(self, checked):
        self.signalPleinEcran.emit(checked)

    def clePressee(self, event):
        if event.key() == Qt.Key.Key_Escape and self.etatPleinEcran:
            self.action_fullscreen.setChecked(False)
            self.modePleinEcran(False)

    # --- Méthode pour afficher les crédits ---
    def afficherCredits(self):
        QMessageBox.information(
            self,
            "Crédits",
            "Application développée par :\n"
            "- AMEDRO Louis\n"
            "- HERBAUX Jules\n"
            "- GAILLARD Noa\n"
            "- MINNEBO Valentin",
            QMessageBox.StandardButton.Ok
        )

    # --- Méthode pour ouvrir le lien de don ---
    def don(self):
        QDesktopServices.openUrl(QUrl("https://www.paypal.com/donate/?hosted_button_id=FLBDLPX25CVYE"))

    def appliquerStyle(self, style_nom):
        """Applique le style clair ou sombre à l'application."""
        # Gestion du check exclusif
        if style_nom == "Clair":
            self.action_style_clair.setChecked(True)
            self.action_style_sombre.setChecked(False)
        else:
            self.action_style_clair.setChecked(False)
            self.action_style_sombre.setChecked(True)

        qss_path = os.path.join(os.path.dirname(__file__), "style", f"{style_nom}.qss")
        if os.path.exists(qss_path):
            with open(qss_path, "r", encoding="utf-8") as f:
                qss = f.read()
                QApplication.instance().setStyleSheet(qss)
        else:
            QApplication.instance().setStyleSheet("")


# ---------------------------------------------------------------------------
# --- Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    
    print(f' --- main --- ')
    app = QApplication(sys.argv)

    fenetre = Bandeau()

    # Connexions de test pour debug
    fenetre.signalFichier.connect(lambda chemin: print(f"[Signal Fichier] Ouvert : {chemin}"))
    fenetre.signalEnregistrer.connect(lambda chemin: print(f"[Signal Enregistrer] Sauvegarde à : {chemin}"))
    fenetre.signalEnregistrerSous.connect(lambda chemin: print(f"[Signal Enregistrer sous] Nouveau chemin : {chemin}"))

    fenetre.show()
    sys.exit(app.exec())