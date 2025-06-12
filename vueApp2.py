# Formation : BUT 1ʳᵉ année | 2024-2025
# Ressource : SAE S2 - Algo et Graphes
# Professeur : M. Conoir
# Noms :  AMEDRO Louis (TPD)
#         HERBAUX Jules (TPD)
#         GAILLARD Noa (TPC)
#         MINNEBO Valentin (TPA)

import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout,
    QFileDialog, QTextEdit, QMessageBox, QSizePolicy, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QPixmap, QDragEnterEvent, QDropEvent

# -----------------------------------------------------------------------------
# --- class Appli Client
# -----------------------------------------------------------------------------

class ClientApp(QWidget):
    cheminGenere = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("🛒 Application Magasin")
        self.setGeometry(100, 100, 1200, 700)
        self.setAcceptDrops(True)
        self.zoomFactor = 1.0
        self.originalPixmap = None
        self.initUI()

    def initUI(self):
        # Carte
        self.imageLabel = QLabel()
        self.imageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.imageLabel.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.imageLabel.setStyleSheet("border: none;")

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.imageLabel)

        self.loadMapButton = QPushButton("🗺️ Charger une carte")
        self.loadMapButton.clicked.connect(self.loadMap)

        self.changeMapButton = QPushButton("🔁 Changer de carte")
        self.changeMapButton.clicked.connect(self.loadMap)
        self.changeMapButton.setVisible(False)

        self.saveMapButton = QPushButton("💾 Enregistrer la carte")
        self.saveMapButton.clicked.connect(self.saveMap)
        self.saveMapButton.setVisible(False)

        self.zoomInButton = QPushButton("➕️ Zoom")
        self.zoomInButton.clicked.connect(self.zoomIn)
        self.zoomInButton.setVisible(False)

        self.zoomOutButton = QPushButton("➖ Zoom")
        self.zoomOutButton.clicked.connect(self.zoomOut)
        self.zoomOutButton.setVisible(False)

        mapButtonLayout = QHBoxLayout()
        mapButtonLayout.addStretch()
        mapButtonLayout.addWidget(self.loadMapButton)
        mapButtonLayout.addWidget(self.changeMapButton)
        mapButtonLayout.addWidget(self.zoomInButton)
        mapButtonLayout.addWidget(self.zoomOutButton)
        mapButtonLayout.addWidget(self.saveMapButton)
        mapButtonLayout.addStretch()

        mapLayout = QVBoxLayout()
        mapLayout.addWidget(self.scrollArea, stretch=1)
        mapLayout.addLayout(mapButtonLayout)

        # Liste de courses
        self.shoppingListEdit = QTextEdit()
        self.shoppingListEdit.setPlaceholderText("📝 Écris ou colle ta liste de courses ici")

        self.loadShoppingListButton = QPushButton("📂 Charger une liste de courses")
        self.loadShoppingListButton.clicked.connect(self.loadShoppingList)

        self.clearListButton = QPushButton("🧹 Vider la liste")
        self.clearListButton.clicked.connect(self.shoppingListEdit.clear)

        self.missingItemsLabel = QLabel("❌ Produits introuvables :")
        self.missingItemsLabel.setStyleSheet("font-weight: bold;")

        self.missingItemsBox = QTextEdit()
        self.missingItemsBox.setReadOnly(True)
        self.missingItemsBox.setFixedHeight(80)

        self.generatePathButton = QPushButton("🚀 Générer le chemin")
        self.generatePathButton.clicked.connect(self.cheminGenere.emit)

        rightLayout = QVBoxLayout()
        rightLayout.addWidget(self.shoppingListEdit)
        rightLayout.addWidget(self.loadShoppingListButton)
        rightLayout.addWidget(self.clearListButton)
        rightLayout.addWidget(self.missingItemsLabel)
        rightLayout.addWidget(self.missingItemsBox)
        rightLayout.addStretch()
        rightLayout.addWidget(self.generatePathButton)

        mainLayout = QHBoxLayout()
        mainLayout.addLayout(mapLayout, stretch=3)
        mainLayout.addLayout(rightLayout, stretch=2)
        self.setLayout(mainLayout)

    def loadMap(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Ouvrir une carte", "", "Images (*.png *.jpg *.bmp)")
        if filePath:
            self.setMap(filePath)

    def saveMap(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "Enregistrer la carte", "", "Images (*.png *.jpg *.bmp)")
        if filePath and self.originalPixmap:
            scaled = self.originalPixmap.scaled(
                int(self.originalPixmap.width() * self.zoomFactor),
                int(self.originalPixmap.height() * self.zoomFactor),
                Qt.AspectRatioMode.KeepAspectRatio
            )
            scaled.save(filePath)

    def setMap(self, filePath: str):
        pixmap = QPixmap(filePath)
        if pixmap.isNull():
            QMessageBox.warning(self, "Erreur", "Image invalide.")
            return
        self.originalPixmap = pixmap
        self.zoomFactor = 1.0
        self.updateMapDisplay()
        self.loadMapButton.setVisible(False)
        self.changeMapButton.setVisible(True)
        self.saveMapButton.setVisible(True)
        self.zoomInButton.setVisible(True)
        self.zoomOutButton.setVisible(True)

    def updateMapDisplay(self):
        if self.originalPixmap:
            width = int(self.originalPixmap.width() * self.zoomFactor)
            height = int(self.originalPixmap.height() * self.zoomFactor)
            scaled = self.originalPixmap.scaled(
                width,
                height,
                Qt.AspectRatioMode.KeepAspectRatio
            )
            self.imageLabel.setPixmap(scaled)
            self.imageLabel.resize(scaled.size())

    def zoomIn(self):
        if self.zoomFactor < 3.0:
            self.zoomFactor *= 1.2
            self.updateMapDisplay()

    def zoomOut(self):
        if self.zoomFactor > 0.2:
            self.zoomFactor *= 0.8
            self.updateMapDisplay()

    def loadShoppingList(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Charger une liste de courses", "", "Fichiers texte (*.txt)")
        if filePath:
            with open(filePath, 'r', encoding='utf-8') as f:
                self.shoppingListEdit.setText(f.read())

    @pyqtSlot(str)
    def updateMissingItems(self, items: str):
        self.missingItemsBox.setText(items)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if any(url.toLocalFile().lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')) for url in urls):
                event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                self.setMap(path)
                break

# -----------------------------------------------------------------------------
# --- Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":

    print(f' --- main --- ')
    app = QApplication(sys.argv)

    fenetre = ClientApp()
    fenetre.cheminGenere.connect(lambda: print("Signal: Génération de chemin déclenchée."))
    fenetre.show()

    sys.exit(app.exec())
