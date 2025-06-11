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


# ---------------------------------------------------------------------------
# --- class Bandeau
# ---------------------------------------------------------------------------

class Bandeau(QMainWindow):

    signalFichier = pyqtSignal(str)
    signalEnregistrer = pyqtSignal(str)
    signalEnregistrerSous = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.setMinimumSize(800, 600)
        self.setWindowTitle("Bandeau SAE - Algo & Graphes")
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
        menuBar.addMenu(creditMenu)
        menuBar.addMenu(affichageMenu)

        # --- Actions pour "Fichier" ---
        ouvrirAction = QAction("📂 Ouvrir", self)
        ouvrirAction.triggered.connect(self.ouvrirFichier)
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

        # --- Action "Plein écran" ---
        self.action_fullscreen = QAction("🖥️ Plein écran", self)
        self.action_fullscreen.setCheckable(True)
        self.action_fullscreen.triggered.connect(self.modePleinEcran)
        affichageMenu.addAction(self.action_fullscreen)

    # --- Méthode pour ouvrir un fichier ---
    def ouvrirFichier(self):
        chemin, _ = QFileDialog.getOpenFileName(self, "Ouvrir un fichier", "", "Tous les fichiers (*)")
        if chemin:
            print(f"[DEBUG] Fichier sélectionné : {chemin}")
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
        chemin, _ = QFileDialog.getSaveFileName(self, "Enregistrer sous", "", "Tous les fichiers (*)")
        if chemin:
            print(f"[DEBUG] Enregistrer sous : {chemin}")
            self.cheminFichierActuel = chemin
            self.signalEnregistrerSous.emit(chemin)

    # --- Méthode pour gérer le plein écran ---
    def modePleinEcran(self, checked):
        if checked:
            self.showFullScreen()
            self.etatPleinEcran = True
        else:
            self.showNormal()
            self.etatPleinEcran = False

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