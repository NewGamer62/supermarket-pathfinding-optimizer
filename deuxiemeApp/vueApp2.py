# Formation : BUT 1ʳᵉ année | 2024-2025
# Ressource : SAE S2 - Algo et Graphes
# Professeur : M. Conoir
# Noms :  AMEDRO Louis (TPD)
#         HERBAUX Jules (TPD)
#         GAILLARD Noa (TPC)
#         MINNEBO Valentin (TPA)

# --------------- #
# --- Modules --- #
# --------------- #

from PyQt6.QtWidgets import (QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout,QFileDialog, QTextEdit, QSizePolicy, QScrollArea)
from PyQt6.QtCore import Qt, QPoint, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QPixmap, QPainter, QPen

# --------------- #
# --- Classes --- #
# --------------- #

class ClientApp(QWidget) :
    
    """Vue de l'application n°2."""
    
    # --------------- #
    # --- Signaux --- #
    # --------------- #
    
    signalGeneratePath = pyqtSignal(list) # Signal émis lorsque l'utilisateur veut générer un chemin sur le plan
    signalGetFolder = pyqtSignal(str) # Signal émis lorsque l'utilisateur ouvre un dossier
    
    # ---------------- #
    # --- Méthodes --- #
    # ---------------- #
    
    # --- Constructeur --- #

    def __init__(self) :
        
        """Instancie la vue complète."""
        
        # --- Initialisation graphique --- #
        
        super().__init__()
        
        self.setWindowTitle("🛒 Application Magasin")
        self.setGeometry(100, 100, 1200, 700)
        self.setAcceptDrops(True)  
        self.zoomFactor = 1.0
        self.originalPixmap = None
        self.lastMousePos = None
        self.initUI()
        
        # --- Initialisation attributs --- #
        
        self.chemin = [] # Chemin affiché sur la vue

    def initUI(self) :
        
        """Instancie toute la partie graphique de la vue."""
        
        # --- Plan de supermarché affiché sur la vue --- #
        
        self.imageLabel = QLabel()
        self.imageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.imageLabel.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.imageLabel.setStyleSheet("border: none;")
        self.imageLabel.setMouseTracking(True)

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.imageLabel)
        
        # --- Boutons en bas du plan de la vue --- #

        # Bouton affiché lorsqu'aucun projet n'a été chargé
        self.loadMapButton = QPushButton("📂 Charger dossier projet")
        self.loadMapButton.clicked.connect(self.loadProject)

        # Boutons affichés lorsqu'un projet a été chargé
        self.changeMapButton = QPushButton("🔁 Changer de projet")
        self.changeMapButton.clicked.connect(self.loadProject)
        self.changeMapButton.setVisible(False)
        
        self.zoomInButton = QPushButton("➕️ Zoom")
        self.zoomInButton.clicked.connect(self.zoomIn)
        self.zoomInButton.setVisible(False)

        self.zoomOutButton = QPushButton("➖ Zoom")
        self.zoomOutButton.clicked.connect(self.zoomOut)
        self.zoomOutButton.setVisible(False)
        
        # --- Zone d'écriture de liste de courses --- #

        self.shoppingListEdit = QTextEdit()
        self.shoppingListEdit.setPlaceholderText("📝 Écris ou colle ta liste de courses ici")

        self.clearListButton = QPushButton("🧹 Vider la liste")
        self.clearListButton.clicked.connect(self.clearList)
        
        # --- Zone d'affichage de produits introuvables --- #

        self.missingItemsLabel = QLabel("❌ Produits introuvables :")
        self.missingItemsLabel.setStyleSheet("font-weight: bold;")

        self.missingItemsBox = QTextEdit()
        self.missingItemsBox.setReadOnly(True)
        self.missingItemsBox.setFixedHeight(200)
        
        # --- Bouton de génération de chemin --- #

        self.generatePathButton = QPushButton("🚀 Générer le chemin")
        self.generatePathButton.clicked.connect(self.sendShoppingList)
        
        # --- Placement des widgets dans la vue --- #

        # Boutons en bas du plan de la vue
        mapButtonLayout = QHBoxLayout()
        mapButtonLayout.addStretch()
        mapButtonLayout.addWidget(self.loadMapButton)
        mapButtonLayout.addWidget(self.changeMapButton)
        mapButtonLayout.addWidget(self.zoomInButton)
        mapButtonLayout.addWidget(self.zoomOutButton)
        mapButtonLayout.addStretch()

        # Plan de la vue
        mapLayout = QVBoxLayout()
        mapLayout.addWidget(self.scrollArea, stretch=1)
        mapLayout.addLayout(mapButtonLayout)

        # Liste de course + produits introuvables + bouton génération chemin
        rightLayout = QVBoxLayout()
        rightLayout.addWidget(self.shoppingListEdit)
        rightLayout.addWidget(self.clearListButton)
        rightLayout.addWidget(self.missingItemsLabel)
        rightLayout.addWidget(self.missingItemsBox)
        rightLayout.addWidget(self.generatePathButton)

        # Vue générale
        mainLayout = QHBoxLayout()
        mainLayout.addLayout(mapLayout, stretch=3)
        mainLayout.addLayout(rightLayout, stretch=2)
        self.setLayout(mainLayout)

    def setMap(self, filePath : str) :
        
        """Change le plan affiché par la vue.\n
Paramètres :
    - filePath : str = chemin du plan à utiliser"""
        
        if (QPixmap(filePath).isNull() == False) :
            
            # Changement plan
            self.originalPixmap = QPixmap(filePath)
            self.zoomFactor = 1.0
            self.updateMapDisplay()
            
            # Mise à jour boutons affichés sur la vue
            self.loadMapButton.setVisible(False)
            self.changeMapButton.setVisible(True)
            self.zoomInButton.setVisible(True)
            self.zoomOutButton.setVisible(True)
            

    def updateMapDisplay(self) :
        
        """Modifie ce qui est affiché sur le plan du supermarché."""
        
        if self.originalPixmap :
            
            # Mise à jour plan affiché
            width = int(self.originalPixmap.width() * self.zoomFactor) ; height = int(self.originalPixmap.height() * self.zoomFactor)
            pixmap = QPixmap(self.originalPixmap.scaled(width, height, Qt.AspectRatioMode.KeepAspectRatio))

            # Affichage chemin s'il en existe un
            if self.chemin :
                
                painter = QPainter(pixmap)
                caseWidth = pixmap.width() // 10
                caseHeight = pixmap.height() // 10

                # Traits rouges dessinant le chemin
                painter.setPen(QPen(Qt.GlobalColor.red, 4))
                for i in range(len(self.chemin) - 1) :
                    
                    x1, y1 = self.chemin[i] ; x2, y2 = self.chemin[i + 1]
                    p1 = QPoint(x1 * caseWidth + caseWidth // 2, y1 * caseHeight + caseHeight // 2)
                    p2 = QPoint(x2 * caseWidth + caseWidth // 2, y2 * caseHeight + caseHeight // 2)
                    painter.drawLine(p1, p2)

                # Points bleus représentant les cases atteintes par le chemin
                painter.setPen(QPen(Qt.GlobalColor.blue, 8))
                for point in self.chemin :

                    painter.drawPoint(QPoint(point[0] * caseWidth + caseWidth // 2, point[1] * caseHeight + caseHeight // 2))

                painter.end()

            # Mise à jour finale
            self.imageLabel.setPixmap(pixmap)
            self.imageLabel.resize(pixmap.size())

    def zoomIn(self) :
        
        """Agrandit le plan du supermarché."""
        
        if self.zoomFactor < 3.0 : self.zoomFactor *= 1.2 ; self.updateMapDisplay()

    def zoomOut(self) :
        
        """Réduit le plan du supermarché."""
        
        if self.zoomFactor > 0.2 : self.zoomFactor *= 0.8 ; self.updateMapDisplay()

    def sendShoppingList(self) :
        
        """Émet un signal contenant tous les produits entrés dans la liste de courses."""
        
        self.signalGeneratePath.emit([item.strip() for item in self.shoppingListEdit.toPlainText().strip().splitlines() if item.strip()])

    @pyqtSlot(list)
    def updateChemin(self, chemin: list) :
        
        """Modifie le chemin affiché sur le plan du supermarché."""
        
        self.chemin = chemin ; self.updateMapDisplay()

    def loadProject(self) :
        
        """Émet un signal contenant un dossier de projet choisi par l'utilisateur."""
        
        self.signalGetFolder.emit(QFileDialog.getExistingDirectory(self, "Choisir le dossier projet contenant supermarche/"))
        
    def clearList(self) :
        
        """Réinitialise la liste de courses, la liste des produits introuvables et efface les chemins du plan."""
        
        self.shoppingListEdit.clear() ; self.missingItemsBox.clear()
        self.updateChemin(None)