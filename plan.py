# Formation : BUT 1ʳᵉ année | 2024-2025
# Ressource : SAE S2 - Algo et Graphes
# Professeur : M. Conoir
# Noms :  AMEDRO Louis (TPD)
#         HERBAUX Jules (TPD)
#         GAILLARD Noa (TPC)
#         MINNEBO Valentin (TPA)

import sys
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication, QScrollArea, QHBoxLayout, QPushButton, QSlider
from PyQt6.QtGui import QPixmap, QWheelEvent, QPainter, QPen
from PyQt6.QtCore import Qt

# -----------------------------------------------------------------------------
# --- class Partie Centre
# -----------------------------------------------------------------------------

class ImageZoomable(QLabel):
    #Permet de zoomer sur une image et de sélectionner des cellules dans une grille
    
    def __init__(self, chemin, taille_grille=80, grille_x=0, grille_y=0):
        # Initialisation de la classe
        
        # Paramètres de base :
        super().__init__()
        self.image = QPixmap(chemin) # Charge l'image depuis le chemin
        self.zoom = 1.0 # Facteur de zoom initial
        self.setScaledContents(True) # Permet de redimensionner l'image dans le QLabel
        
        # Paramètres de la grille :
        self.taille_grille = taille_grille
        self.grille_x = grille_x #
        self.grille_y = grille_y
        
        self.cases_selectionnees = set() # Ensemble des cases sélectionnées
        
        # ??? :
        self._deplacement_active = False 
        self._deplacement_depart = None
        self.selection_active = False
        self.suppresion_active = False
        
        self.updateImage() # Met à jour l'affichage de l'image

    #=====================================================================
    #=== Méthodes :
    #=====================================================================

    def setTailleGrille(self, taille):
        self.taille_grille = max(5, taille)
        self.update()

    def decalerGrille(self, dx, dy):
        self.grille_x += dx
        self.grille_y += dy
        self.update()

    def updateImage(self):
        # Met à jour l'image affichée en fonction du zoom et de la taille de la grille
        
        # Vérifie si l'image est valide avant de la redimensionner :
        if not self.image.isNull():
            
            # Redimensionne l'image en fonction du zoom et de la taille de la grille :
            scaled = self.image.scaled(
                int(self.image.width() * self.zoom),
                int(self.image.height() * self.zoom),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            
            self.setPixmap(scaled) # Définit le pixmap de l'étiquette avec l'image redimensionnée
            self.resize(scaled.size()) # Redimensionne en correspondant à la taille de l'image

    def paintEvent(self, event):
        # Redessine l'image et la grille sur le QLabel automatiquement par Qt
        super().paintEvent(event)
        
        # Si l'image n'est pas valide, on ne dessine rien :
        if self.pixmap() is None or self.pixmap().isNull():
            return
        
        # Dessine la grille et les cases sélectionnées sur l'image
        affichage = QPainter(self)
        affichage.setRenderHint(QPainter.RenderHint.Antialiasing, False) # Désactive l'anticrénelage pour une grille plus nette
        w, h = self.pixmap().width(), self.pixmap().height() # Largeur et hauteur de l'image affichée
        
        # Taille de la case sur l'image affichée (toujours proportionnelle au zoom)
        taille_case = self.taille_grille * self.zoom
        if taille_case < 5:
            taille_case = 5
            
        # Décalage de la grille sur l'image affichée :
        decalage_x = self.grille_x * self.zoom
        decalage_y = self.grille_y * self.zoom
        
        # Remplir les cases sélectionnées en bleu clair :
        couleur = Qt.GlobalColor.cyan
        for col, ligne in self.cases_selectionnees:
            x = int(col * taille_case + decalage_x)
            y = int(ligne * taille_case + decalage_y)
            if 0 <= x < w and 0 <= y < h:
                affichage.fillRect(x, y, int(taille_case), int(taille_case), couleur)
                
        # Grille :
        affichage.setPen(QPen(Qt.GlobalColor.black, 1, Qt.PenStyle.SolidLine, Qt.PenCapStyle.FlatCap, Qt.PenJoinStyle.MiterJoin))
        x = decalage_x
        while x < w:
            affichage.drawLine(int(x), 0, int(x), h)
            x += taille_case
        y = decalage_y
        while y < h:
            affichage.drawLine(0, int(y), w, int(y))
            y += taille_case
            
        affichage.end()

    def wheelEvent(self, event: QWheelEvent):
        # Gère le zoom avec la molette de la souris de Qt
        
        zone_zoom = self.parent() # Zoom toujours au centre de la vue
        
        # Vérifie si le parent est un QScrollArea, sinon cherche dans les parents
        if not isinstance(zone_zoom, QScrollArea):
            zone_zoom = self.parentWidget()
            while zone_zoom and not isinstance(zone_zoom, QScrollArea):
                zone_zoom = zone_zoom.parentWidget()
                
        # Si on a trouvé un QScrollArea, on utilise ses barres de défilement pour centrer le zoom
        if zone_zoom:
            h_scroll = zone_zoom.horizontalScrollBar()
            v_scroll = zone_zoom.verticalScrollBar()
            viewport = zone_zoom.viewport() 
            centre_x = h_scroll.value() + viewport.width() // 2
            centre_y = v_scroll.value() + viewport.height() // 2
            
            # Calculer la position du centre de la vue dans l'image en x et y :
            if self.width() > 0 :
                position_x = centre_x / self.width()
            else: 
                position_x = 0
                
            if self.height() > 0:
                position_y = centre_y / self.height() # 
            else :
                position_y = 0

            # Calculer l'angle de la molette pour ajuster le zoom : 
            angle = event.angleDelta().y()
            if angle > 0:
                self.zoom = min(self.zoom * 1.1, 10.0)
            else:
                self.zoom = max(self.zoom / 1.1, 0.1)
            self.updateImage()

            new_width = self.width()
            new_height = self.height()
            h_scroll.setValue(int(position_x * new_width - viewport.width() // 2))
            v_scroll.setValue(int(position_y * new_height - viewport.height() // 2))
            
        # Sinon, on zoom simplement sur l'image :
        else :
            angle = event.angleDelta().y()
            if angle > 0:
                self.zoom = min(self.zoom * 1.1, 10.0)
            else:
                self.zoom = max(self.zoom / 1.1, 0.1)
            self.updateImage()

    def mousePressEvent(self, event):
        # Gère les clics de souris pour le drag et la sélection de cellules de Qt
        
        # Si le bouton du milieu est pressé, on active le déplacement de la vue :
        if event.button() == Qt.MouseButton.MiddleButton:
            self._deplacement_active = True
            self._deplacement_depart = event.position()
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
            
        # Si le bouton gauche est pressé, on active la sélection de cellules :
        elif event.button() == Qt.MouseButton.LeftButton:
            self.selection_active = True
            self._add_cell_from_event(event)
            
        # Si le bouton droit est pressé, on active la suppression de cellules :
        elif event.button() == Qt.MouseButton.RightButton:
            self.suppresion_active = True
            self._remove_cell_from_event(event)
            
        # Sinon, on appelle la méthode de la classe parente :
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        # Gère le déplacement de la vue ou la sélection/suppression de cellules lors du mouvement de la souris de Qt
        
        # Si le déplacement est actif, on déplace la vue en fonction du mouvement de la souris :
        if self._deplacement_active and self._deplacement_depart is not None:
            zone_zoom = self.parent()
            
            # Si le parent est un QScrollArea, sinon cherche dans les parents :
            if not isinstance(zone_zoom, QScrollArea):
                zone_zoom = self.parentWidget()
                while zone_zoom and not isinstance(zone_zoom, QScrollArea):
                    zone_zoom = zone_zoom.parentWidget()
            
            # Si on a trouvé un QScrollArea, on déplace la vue en fonction du mouvement de la souris :
            if zone_zoom:
                delta = event.position() - self._deplacement_depart
                # Si le déplacement est significatif, on met à jour les barres de défilement :
                if abs(delta.x()) >= 1 or abs(delta.y()) >= 1:
                    h_scroll = zone_zoom.horizontalScrollBar()
                    v_scroll = zone_zoom.verticalScrollBar()
                    h_scroll.setValue(h_scroll.value() - int(delta.x()))
                    v_scroll.setValue(v_scroll.value() - int(delta.y()))
                    self._deplacement_depart = event.position() # Met à jour la position de départ pour le prochain mouvement	
        
        # Sinon la sélection est active, on ajoute une cellule à la sélection :
        elif self.selection_active:
            self._add_cell_from_event(event)
            
        # Sinon la suppression est active, on supprime une cellule de la sélection :
        elif self.suppresion_active:
            self._remove_cell_from_event(event)
            
        # Sinon, on appelle la méthode de la classe parente :
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        # Gère le relâchement des boutons de la souris pour arrêter le déplacement, la sélection ou la suppression de cellules de Qt
        
        # Si le bouton du milieu est relâché, on arrête le déplacement de la vue :
        if event.button() == Qt.MouseButton.MiddleButton and self._deplacement_active:
            self._deplacement_active = False
            self.setCursor(Qt.CursorShape.ArrowCursor)
            
        # Sinon le bouton gauche est relâché, on arrête la sélection de cellules :
        elif event.button() == Qt.MouseButton.LeftButton and self.selection_active:
            self.selection_active = False
            
        # Sinon le bouton droit est relâché, on arrête la suppression de cellules :
        elif event.button() == Qt.MouseButton.RightButton and self.suppresion_active:
            self.suppresion_active = False
            
        # Sinon, on appelle la méthode de la classe parente :
        else:
            super().mouseReleaseEvent(event)

    def _add_cell_from_event(self, event):
        # Ajoute une cellule à la sélection en fonction de la position de l'événement de souris de Qt
        
        x = int(event.position().x())
        y = int(event.position().y())
        
        taille_case = self.taille_grille * self.zoom # Taille de la case en fonction du zoom
        
        if taille_case < 5:
            taille_case = 5
        
        # Décalage de la grille en fonction du zoom :
        decalage_x = self.grille_x * self.zoom
        decalage_y = self.grille_y * self.zoom
        col = int((x - decalage_x) // taille_case)
        ligne = int((y - decalage_y) // taille_case)
        
        if (x - decalage_x) >= 0 and (y - decalage_y) >= 0:
            cell = (col, ligne)
            if cell not in self.cases_selectionnees:
                self.cases_selectionnees.add(cell)
                self.update()

    def _remove_cell_from_event(self, event):
        # Supprime une cellule de la sélection en fonction de la position de l'événement de souris de Qt
        
        x = int(event.position().x())
        y = int(event.position().y())
        taille_case = self.taille_grille * self.zoom
        
        if taille_case < 5:
            taille_case = 5
        
        # Décalage de la grille en fonction du zoom :
        decalage_x = self.grille_x * self.zoom
        decalage_y = self.grille_y * self.zoom
        col = int((x - decalage_x) // taille_case)
        ligne = int((y - decalage_y) // taille_case)
        
        if (x - decalage_x) >= 0 and (y - decalage_y) >= 0:
            cell = (col, ligne)
            if cell in self.cases_selectionnees:
                self.cases_selectionnees.remove(cell)
                self.update()

class Plan(QWidget):
    def __init__(self):
        super().__init__()
        
        # Layout principal :
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Zone de zoom/image :
        self.zone_zoom = QScrollArea()
        self.zone_zoom.setWidgetResizable(False)
        self.zone_zoom.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_widget = ImageZoomable("plan.jpg", taille_grille=80)
        self.zone_zoom.setWidget(self.image_widget)
        layout.addWidget(self.zone_zoom)

        # Contrôles pour la taille de la grille
        layout_grille = QHBoxLayout()
        self.bouton_moins = QPushButton("-")
        self.bouton_plus = QPushButton("+")
        self.slider_grille = QSlider(Qt.Orientation.Horizontal)
        self.slider_grille.setMinimum(5)
        self.slider_grille.setMaximum(500)
        self.slider_grille.setValue(80)
        self.slider_grille.setTickInterval(5)
        self.slider_grille.setSingleStep(1)
        
        # Ajout des boutons de décalage
        self.bouton_gauche = QPushButton("←")
        self.bouton_droite = QPushButton("→")
        self.bouton_haut = QPushButton("↑")
        self.bouton_bas = QPushButton("↓")
        layout_grille.addWidget(self.bouton_moins)
        layout_grille.addWidget(self.slider_grille)
        layout_grille.addWidget(self.bouton_plus)
        layout_grille.addWidget(self.bouton_gauche)
        layout_grille.addWidget(self.bouton_droite)
        layout_grille.addWidget(self.bouton_haut)
        layout_grille.addWidget(self.bouton_bas)
        layout.addLayout(layout_grille)

        # Connexions
        self.slider_grille.valueChanged.connect(self.image_widget.setTailleGrille)
        self.bouton_plus.clicked.connect(lambda: self.slider_grille.setValue(self.slider_grille.value() + 5))
        self.bouton_moins.clicked.connect(lambda: self.slider_grille.setValue(self.slider_grille.value() - 5))
        self.bouton_gauche.clicked.connect(lambda: self.image_widget.decalerGrille(-5, 0))
        self.bouton_droite.clicked.connect(lambda: self.image_widget.decalerGrille(5, 0))
        self.bouton_haut.clicked.connect(lambda: self.image_widget.decalerGrille(0, -5))
        self.bouton_bas.clicked.connect(lambda: self.image_widget.decalerGrille(0, 5))

# Programme principal : test de la vue ---------------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = Plan()
    fenetre.show()
    sys.exit(app.exec())