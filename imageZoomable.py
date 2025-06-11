# Formation : BUT 1ʳᵉ année | 2024-2025
# Ressource : SAE S2 - Algo et Graphes
# Professeur : M. Conoir
# Noms :  AMEDRO Louis (TPD)
#         HERBAUX Jules (TPD)
#         GAILLARD Noa (TPC)
#         MINNEBO Valentin (TPA)

from PyQt6.QtWidgets import QLabel, QScrollArea
from PyQt6.QtGui import QPixmap, QWheelEvent, QPainter, QPen, QColor, QFont
from PyQt6.QtCore import Qt, pyqtSlot, pyqtSignal

#========================================================================
# Class ImageZoomable
#========================================================================

class ImageZoomable(QLabel):
    #Permet de zoomer sur une image et de sélectionner des cellules dans une grille
    
    matrice_generee = pyqtSignal(list)  # Signal pour transmettre la matrice
    produits_case_selectionnee = pyqtSignal(list)  # Signal pour transmettre la liste des produits de la case sélectionnée

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
        
        # Ajout des ensembles pour chaque type de case
        self.cases_mur = set()
        self.cases_caisse = set()
        self.cases_entree = set()
        self.type_case_actuel = "mur"  # Par défaut, rien sélectionné
        
        # Initialisation des états de la souris/curseur :
        self._deplacement_active = False 
        self._deplacement_depart = None
        self.selection_active = False
        self.suppresion_active = False
        
        # Ajout d'un dictionnaire pour les produits par case
        self.cases_produits = dict()  # (col, ligne) -> [produit1, produit2, ...]
        
        self.updateImage() # Met à jour l'affichage de l'image

    #=================================
    # Méthodes 
    #=================================
    
    def generer_matrice(self):
        # Détermine la taille maximale de la grille utilisée
        toutes_cases = self.cases_mur | self.cases_caisse | self.cases_entree | set(self.cases_produits.keys())
        if not toutes_cases:
            return []
        
        max_col = max((col for col, _ in toutes_cases), default=0)
        max_lig = max((lig for _, lig in toutes_cases), default=0)
        matrice = []
        
        for lig in range(max_lig + 1):
            ligne = []
            for col in range(max_col + 1):
                cellule = []
                if (col, lig) in self.cases_mur:
                    cellule.append("mur")
                if (col, lig) in self.cases_caisse:
                    cellule.append("caisse")
                if (col, lig) in self.cases_entree:
                    cellule.append("entree")
                if (col, lig) in self.cases_produits and self.cases_produits[(col, lig)]:
                    cellule.extend(self.cases_produits[(col, lig)])
                ligne.append(cellule)  # Toujours une liste de str, même vide
            matrice.append(ligne)
        return matrice
    
    def emettre_matrice(self):
        matrice = self.generer_matrice()
        self.matrice_generee.emit(matrice)

    def case_valide(self, cellule):
        # Vérifie si une cellule est valide dans l'image actuelle
        col, ligne = cellule
        x = int(col * self.taille_grille + self.grille_x)
        y = int(ligne * self.taille_grille + self.grille_y)
        return (0 <= x < self.image.width()) and (0 <= y < self.image.height())

    def filtrer_cases_visibles(self):
        # Supprime les cases hors de l'image originale (pas le zoom)
        # Si l'image n'est pas valide avant de filtrer les cases, on ne fait rien :
        if self.image.isNull():
            return
        # Filtre les cases pour ne garder que celles qui sont valides dans l'image actuelle
        self.cases_mur = set(filter(self.case_valide, self.cases_mur))
        self.cases_caisse = set(filter(self.case_valide, self.cases_caisse))
        self.cases_entree = set(filter(self.case_valide, self.cases_entree))
        # Filtrer aussi les produits pour ne garder que ceux dans des cases valides
        self.cases_produits = {cell: produits for cell, produits in self.cases_produits.items() if self.case_valide(cell)}

    def setTailleGrille(self, taille):
        # Définit la taille de la grille et met à jour l'affichage
        self.taille_grille = max(5, taille)
        self.filtrer_cases_visibles()
        self.update()
        self.emettre_matrice() # Émet la matrice mise à jour

    def decalerGrille(self, dx, dy):
        # Décale la grille de dx en x et dy en y, puis met à jour l'affichage
        self.grille_x += dx
        self.grille_y += dy
        self.filtrer_cases_visibles()
        self.update()
        self.emettre_matrice()

    def charger_image(self, chemin):
        # Charge une nouvelle image depuis le chemin spécifié et met à jour l'affichage
        self.image = QPixmap(chemin)
        self.zoom = 1.0 # Réinitialise le zoom à 1.0
        self.filtrer_cases_visibles()
        self.updateImage()
        self.emettre_matrice()
        
    def vider_elt(self):
        # Vide les ensembles de cases et met à jour l'affichage, soit les élements de la grille
        self.cases_mur.clear()
        self.cases_caisse.clear()
        self.cases_entree.clear()
        self.cases_produits.clear()
        self.emettre_matrice()

    def supprimer_image(self):
        # Supprime l'image actuelle et vide les ensembles de cases
        self.image = QPixmap()
        self.vider_elt()
        self.updateImage()
        self.emettre_matrice()

    def changer_type_case(self, case, type_case):
        # 
        self.cases_mur.discard(case)
        self.cases_caisse.discard(case)
        self.cases_entree.discard(case)
        if type_case == "mur":
            self.cases_mur.add(case)
        elif type_case == "caisse":
            self.cases_caisse.add(case)
        elif type_case == "entree":
            self.cases_entree.add(case)
        self.update()
        self.emettre_matrice()

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
            self.filtrer_cases_visibles()
        else:
            self.clear()
            self.resize(0, 0)

    def paintEvent(self, event):
        # Redessine l'image et la grille sur le QLabel automatiquement par Qt
        super().paintEvent(event)
        
        # Si l'image n'est pas valide, on ne dessine rien :
        if self.pixmap() is None or self.pixmap().isNull():
            return
        affichage = QPainter(self)
        affichage.setRenderHint(QPainter.RenderHint.Antialiasing, False)
        w, h = self.pixmap().width(), self.pixmap().height()
        taille_case = self.taille_grille * self.zoom
        if taille_case < 5:
            taille_case = 5
        decalage_x = self.grille_x * self.zoom
        decalage_y = self.grille_y * self.zoom

        # Colorie en rouge uniquement les cases contenant au moins un produit
        # et qui ne sont pas une entrée, une caisse ou un mur
        couleur_case = QColor(Qt.GlobalColor.red)
        couleur_case.setAlpha(200)
        for (col, lig), produits in self.cases_produits.items():
            if produits and (col, lig) not in self.cases_mur and (col, lig) not in self.cases_caisse and (col, lig) not in self.cases_entree:
                x = int(col * taille_case + decalage_x)
                y = int(lig * taille_case + decalage_y)
                if 0 <= x < w and 0 <= y < h:
                    affichage.fillRect(x, y, int(taille_case), int(taille_case), couleur_case)

        # Affichage des cases par type (optionnel, peut être supprimé si tu veux que seul le rouge apparaisse)
        couleur_mur = QColor(Qt.GlobalColor.darkGray)
        couleur_mur.setAlpha(200)
        couleur_caisse = QColor(Qt.GlobalColor.yellow)
        couleur_caisse.setAlpha(200)
        couleur_entree = QColor(Qt.GlobalColor.green)
        couleur_entree.setAlpha(200)
        for col, ligne in self.cases_mur:
            x = int(col * taille_case + decalage_x)
            y = int(ligne * taille_case + decalage_y)
            if 0 <= x < w and 0 <= y < h:
                affichage.fillRect(x, y, int(taille_case), int(taille_case), couleur_mur)
        for col, ligne in self.cases_caisse:
            x = int(col * taille_case + decalage_x)
            y = int(ligne * taille_case + decalage_y)
            if 0 <= x < w and 0 <= y < h:
                affichage.fillRect(x, y, int(taille_case), int(taille_case), couleur_caisse)
        for col, ligne in self.cases_entree:
            x = int(col * taille_case + decalage_x)
            y = int(ligne * taille_case + decalage_y)
            if 0 <= x < w and 0 <= y < h:
                affichage.fillRect(x, y, int(taille_case), int(taille_case), couleur_entree)

        # Affichage des produits dans les cases
        font = QFont()
        font.setPointSize(int(taille_case // 3))
        affichage.setFont(font)
        for (col, ligne), produits in self.cases_produits.items():
            if not produits:
                continue
            x = int(col * taille_case + decalage_x)
            y = int(ligne * taille_case + decalage_y)
            if 0 <= x < w and 0 <= y < h:
                texte = produits[-1]
                affichage.setPen(QPen(Qt.GlobalColor.red))
                affichage.drawText(x+2, y+int(taille_case*0.7), texte)

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

    @pyqtSlot(str)
    def recevoir_signal_type_case(self, type_case):
        # Slot à connecter à un signal externe pour changer le type à appliquer
        if type_case in ("mur", "caisse", "entree"):
            self.type_case_actuel = type_case
        else:
            self.type_case_actuel = "mur"  # Toujours revenir à mur si signal inconnu

    @pyqtSlot(str)
    def recevoir_signal_produit(self, produit):
        # Ajoute un produit dans la dernière case sélectionnée (ou à définir selon logique)
        # Ici, on suppose que la dernière case sélectionnée est stockée dans self._derniere_case
        if hasattr(self, "_derniere_case") and self._derniere_case is not None:
            case = self._derniere_case
            if case not in self.cases_produits:
                self.cases_produits[case] = []
            self.cases_produits[case].append(produit)
            self.update()
            self.emettre_matrice()

    @pyqtSlot(list)
    def mettre_a_jour_produits_case(self, produits):
        # Met à jour la liste des produits de la dernière case sélectionnée
        if hasattr(self, "_derniere_case") and self._derniere_case is not None:
            case = self._derniere_case
            if produits:
                self.cases_produits[case] = produits
            else:
                # Si la liste est vide, on retire la case des produits
                self.cases_produits.pop(case, None)
            self.update()
            self.emettre_matrice()

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
            self.ajouter_cellule(event)
            
        # Si le bouton droit est pressé, on active la suppression de cellules :
        elif event.button() == Qt.MouseButton.RightButton:
            self.suppresion_active = True
            self.supprimer_cellule(event)
            
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
            self.ajouter_cellule(event)
            
        # Sinon la suppression est active, on supprime une cellule de la sélection :
        elif self.suppresion_active:
            self.supprimer_cellule(event)
            
        # Sinon, on appelle la méthode de la classe parente :
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        # Gère le relâchement des boutons de la souris pour arrêter le déplacement, la sélection ou la suppression de cellule de Qt
        
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

    def ajouter_cellule(self, event):
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
            cellule = (col, ligne)
            self._derniere_case = cellule  # Mémorise la dernière case sélectionnée
            # Si aucun type d'élément magasin n'est sélectionné, on sélectionne la case "produit"
            if self.type_case_actuel is None:
                # Émet la liste des produits de cette case (vide si aucun produit)
                produits = self.cases_produits.get(cellule, [])
                self.produits_case_selectionnee.emit(produits)
                self.update()
            else:
                # Toujours appliquer le type courant (par défaut "mur")
                self.changer_type_case(cellule, self.type_case_actuel)

    def supprimer_cellule(self, event):
        # Supprime une cellule de n'importe quel type en fonction de la position de l'événement de souris de Qt
        
        x = int(event.position().x())
        y = int(event.position().y())
        taille_case = self.taille_grille * self.zoom

        if taille_case < 5:
            taille_case = 5

        decalage_x = self.grille_x * self.zoom
        decalage_y = self.grille_y * self.zoom
        col = int((x - decalage_x) // taille_case)
        ligne = int((y - decalage_y) // taille_case)

        # Vérifie que la position est valide avant de supprimer la cellule :
        if (x - decalage_x) >= 0 and (y - decalage_y) >= 0:
            cellule = (col, ligne)
            self.cases_mur.discard(cellule)
            self.cases_caisse.discard(cellule)
            self.cases_entree.discard(cellule)
            # Supprime aussi les produits de cette case
            self.cases_produits.pop(cellule, None)
            self.update()
            self.emettre_matrice()

    def avoir_image(self):
        return not self.image.isNull()