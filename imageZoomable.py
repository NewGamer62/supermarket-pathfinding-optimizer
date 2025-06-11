# Formation : BUT 1ʳᵉ année | 2024-2025
# Ressource : SAE S2 - Algo et Graphes
# Professeur : M. Conoir
# Noms :  AMEDRO Louis (TPD)
#         HERBAUX Jules (TPD)
#         GAILLARD Noa (TPC)
#         MINNEBO Valentin (TPA)

from PyQt6.QtWidgets import QLabel, QScrollArea
from PyQt6.QtGui import QPixmap, QWheelEvent, QPainter, QPen
from PyQt6.QtCore import Qt, pyqtSlot

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
        # Ajout des ensembles pour chaque type de case
        self.cases_mur = set()
        self.cases_caisse = set()
        self.cases_entree = set()
        self.type_case_actuel = "mur"  # Par défaut, mur sélectionné
        
        # Initialisation des états de la souris/curseur :
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

    def charger_image(self, chemin):
        self.image = QPixmap(chemin)
        self.zoom = 1.0
        self.cases_selectionnees.clear()
        self.updateImage()
        
    def vider_elt(self):
        # Efface les ensembles de cases pour chaque type
        self.cases_mur.clear()
        self.cases_caisse.clear()
        self.cases_entree.clear()

    def supprimer_image(self):
        self.image = QPixmap()
        self.cases_selectionnees.clear()
        self.vider_elt()  # Correction : appel sans argument
        self.updateImage()

    def avoir_image(self):
        return not self.image.isNull()

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
        else:
            self.clear()
            self.resize(0, 0)

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
        
        # Affichage des cases par type
        for col, ligne in self.cases_mur:
            x = int(col * taille_case + decalage_x)
            y = int(ligne * taille_case + decalage_y)
            if 0 <= x < w and 0 <= y < h:
                affichage.fillRect(x, y, int(taille_case), int(taille_case), Qt.GlobalColor.darkGray)
        for col, ligne in self.cases_caisse:
            x = int(col * taille_case + decalage_x)
            y = int(ligne * taille_case + decalage_y)
            if 0 <= x < w and 0 <= y < h:
                affichage.fillRect(x, y, int(taille_case), int(taille_case), Qt.GlobalColor.yellow)
        for col, ligne in self.cases_entree:
            x = int(col * taille_case + decalage_x)
            y = int(ligne * taille_case + decalage_y)
            if 0 <= x < w and 0 <= y < h:
                affichage.fillRect(x, y, int(taille_case), int(taille_case), Qt.GlobalColor.green)
        # Suppression de l'affichage des cases_selectionnees (bleu/cyan)

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

    def changer_type_case(self, case, type_case):
        # Retire la case de tous les ensembles
        self.cases_mur.discard(case)
        self.cases_caisse.discard(case)
        self.cases_entree.discard(case)
        self.cases_selectionnees.discard(case)
        # Ajoute la case dans le bon ensemble
        if type_case == "mur":
            self.cases_mur.add(case)
        elif type_case == "caisse":
            self.cases_caisse.add(case)
        elif type_case == "entree":
            self.cases_entree.add(case)
        self.update()

    @pyqtSlot(str)
    def recevoir_signal_type_case(self, type_case):
        # Slot à connecter à un signal externe pour changer le type à appliquer
        if type_case in ("mur", "caisse", "entree"):
            self.type_case_actuel = type_case
        else:
            self.type_case_actuel = "mur"  # Toujours revenir à mur si signal inconnu

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
            self._deplacement_depart = event.globalPosition().toPoint() # Position de départ du déplacement
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
                delta = event.globalPosition().toPoint() - self._deplacement_depart
                # Si le déplacement est significatif, on met à jour les barres de défilement :
                if abs(delta.x()) >= 1 or abs(delta.y()) >= 1:
                    h_scroll = zone_zoom.horizontalScrollBar()
                    v_scroll = zone_zoom.verticalScrollBar()
                    h_scroll.setValue(h_scroll.value() - int(delta.x()))
                    v_scroll.setValue(v_scroll.value() - int(delta.y()))
                    self._deplacement_depart = event.globalPosition().toPoint() # Met à jour la position de départ pour le prochain mouvement	
        
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
            # Toujours appliquer le type courant (par défaut "mur")
            self.changer_type_case(cell, self.type_case_actuel)

    def _remove_cell_from_event(self, event):
        # Supprime une cellule de n'importe quel type en fonction de la position de l'événement de souris
        
        x = int(event.position().x())
        y = int(event.position().y())
        taille_case = self.taille_grille * self.zoom

        if taille_case < 5:
            taille_case = 5

        decalage_x = self.grille_x * self.zoom
        decalage_y = self.grille_y * self.zoom
        col = int((x - decalage_x) // taille_case)
        ligne = int((y - decalage_y) // taille_case)

        if (x - decalage_x) >= 0 and (y - decalage_y) >= 0:
            cell = (col, ligne)
            # Supprime la case de tous les ensembles
            self.cases_mur.discard(cell)
            self.cases_caisse.discard(cell)
            self.cases_entree.discard(cell)
            self.cases_selectionnees.discard(cell)
            self.update()