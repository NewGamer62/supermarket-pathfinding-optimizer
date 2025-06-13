# Formation : BUT 1ʳᵉ année | 2024-2025
# Ressource : SAE S2 - Algo et Graphes
# Professeur : M. Conoir
# Noms :  AMEDRO Louis (TPD)
#         HERBAUX Jules (TPD)
#         GAILLARD Noa (TPC)
#         MINNEBO Valentin (TPA)

import sys
import json
from pathlib import Path
from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout,QFileDialog, QTextEdit, QMessageBox, QSizePolicy, QScrollArea)
from PyQt6.QtCore import Qt, QPoint, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QPixmap, QPainter, QPen


# -----------------------------------------------------------------------------
# --- class App2
# -----------------------------------------------------------------------------

class ClientApp(QWidget):
    signalGeneratePath = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("🛒 Application Magasin")
        self.setGeometry(100, 100, 1200, 700)
        self.setAcceptDrops(True)
        self.zoomFactor = 1.0
        self.chemin = []
        self.originalPixmap = None
        self.lastMousePos = None
        self.cases = []
        self.chemin = []  # stocke les coordonnées du chemin
        self.initUI()

    def initUI(self):
        self.imageLabel = QLabel()
        self.imageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.imageLabel.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.imageLabel.setStyleSheet("border: none;")
        self.imageLabel.setMouseTracking(True)

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.imageLabel)

        self.loadMapButton = QPushButton("📂 Charger dossier projet")
        self.loadMapButton.clicked.connect(self.loadProject)

        self.changeMapButton = QPushButton("🔁 Changer de carte")
        self.changeMapButton.clicked.connect(self.loadProject)
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

        self.shoppingListEdit = QTextEdit()
        self.shoppingListEdit.setPlaceholderText("📝 Écris ou colle ta liste de courses ici")

        self.loadShoppingListButton = QPushButton("📥 Charger une liste de courses")
        self.loadShoppingListButton.clicked.connect(self.loadShoppingList)

        self.clearListButton = QPushButton("🧹 Vider la liste")
        self.clearListButton.clicked.connect(self.shoppingListEdit.clear)

        self.missingItemsLabel = QLabel("❌ Produits introuvables :")
        self.missingItemsLabel.setStyleSheet("font-weight: bold;")

        self.missingItemsBox = QTextEdit()
        self.missingItemsBox.setReadOnly(True)
        self.missingItemsBox.setFixedHeight(80)

        self.generatePathButton = QPushButton("🚀 Générer le chemin")
        self.generatePathButton.clicked.connect(self.sendShoppingList)

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
            scaled = self.originalPixmap.scaled(width, height, Qt.AspectRatioMode.KeepAspectRatio)
            pixmap = QPixmap(scaled)

            # Dessiner le chemin si disponible
            if self.chemin:
                painter = QPainter(pixmap)
                pen = QPen(Qt.GlobalColor.red, 4)
                painter.setPen(pen)
                caseWidth = pixmap.width() // 10
                caseHeight = pixmap.height() // 10


                for i in range(len(self.chemin) - 1):
                    x1, y1 = self.chemin[i]
                    x2, y2 = self.chemin[i + 1]
                    p1 = QPoint(x1 * caseWidth + caseWidth // 2, y1 * caseHeight + caseHeight // 2)
                    p2 = QPoint(x2 * caseWidth + caseWidth // 2, y2 * caseHeight + caseHeight // 2)
                    painter.drawLine(p1, p2)

                # Affichage des points en bleu
                for point in self.chemin:
                    px, py = point
                    p = QPoint(px * caseWidth + caseWidth // 2, py * caseHeight + caseHeight // 2)
                    painter.setPen(QPen(Qt.GlobalColor.blue, 8))
                    painter.drawPoint(p)

                # Affichage des traits en rouge
                painter.setPen(QPen(Qt.GlobalColor.red, 4))
                for i in range(len(self.chemin) - 1):
                    x1, y1 = self.chemin[i]
                    x2, y2 = self.chemin[i + 1]
                    p1 = QPoint(x1 * caseWidth + caseWidth // 2, y1 * caseHeight + caseHeight // 2)
                    p2 = QPoint(x2 * caseWidth + caseWidth // 2, y2 * caseHeight + caseHeight // 2)
                painter.drawLine(p1, p2)

                painter.end()

            self.imageLabel.setPixmap(pixmap)
            self.imageLabel.resize(pixmap.size())
    def tracer_chemin(self, chemin):
        self.chemin = chemin
        self.updateMapDisplay()

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

    def sendShoppingList(self):
        text = self.shoppingListEdit.toPlainText()
        liste = [item.strip() for item in text.strip().splitlines() if item.strip()]
        print("🛒 Produits demandés :", liste)
        self.signalGeneratePath.emit(liste)

    @pyqtSlot(str)
    def updateMissingItems(self, items: list[str]):
        self.missingItemsBox.setText(items)

    @pyqtSlot(list)
    def updateChemin(self, chemin: list):
        print("🧭 Nouveau chemin reçu :", chemin)
        self.chemin = chemin
        self.updateMapDisplay()

    def loadProject(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Choisir le dossier projet contenant supermarche/")
        if not dir_path:
            return
        base = Path(dir_path)
        plan_path = base / "supermarche" / "plan.jpg"
        quad_path = base / "supermarche" / "quadrillage.json"

        if not (plan_path.exists() and quad_path.exists()):
            QMessageBox.warning(self, "Erreur", "Fichiers manquants : plan.jpg et quadrillage.json requis.")
            return

        self.setMap(str(plan_path))

        try:
            with open(quad_path, "r", encoding="utf-8") as f:
                quadrillage = json.load(f)["quadrillage"]
            self.cases = []
            for y, row in enumerate(quadrillage):
                for x, contenu in enumerate(row):
                    self.cases.append({"x": x, "y": y, "contenu": contenu})
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Erreur lecture quadrillage.json :\n{e}")

# -----------------------------------------------------------------------------
# --- Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":

    print(f' --- main --- ')
    app = QApplication(sys.argv)

    fenetre = ClientApp()
    fenetre.show()

    sys.exit(app.exec())
