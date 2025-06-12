# Formation : BUT 1ʳᵉ année | 2024-2025
# Ressource : SAE S2 - Algo et Graphes
# Professeur : M. Conoir
# Noms :  AMEDRO Louis (TPD)
#         HERBAUX Jules (TPD)
#         GAILLARD Noa (TPC)
#         MINNEBO Valentin (TPA)

import sys, imageZoomable
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QApplication, QScrollArea, QHBoxLayout, QPushButton, QSlider, QFileDialog, QMessageBox
from PyQt6.QtCore import Qt

#=======================================================================
# Classe Plan
#=======================================================================

class Plan(QWidget):
    # Classe principale de la vue, qui contient l'image zoomable et les contrôles pour la grille
    
    def __init__(self):
        super().__init__()

        self.chemin_image = None

        # Layout principal :
        self.layout_principal = QVBoxLayout()
        self.setLayout(self.layout_principal)

        # Layout pour l'image :
        self.layout_image = QVBoxLayout()
        self.layout_principal.addLayout(self.layout_image, stretch=1)

        # Zone de zoom :
        self.zone_zoom = QScrollArea()
        self.zone_zoom.setWidgetResizable(False)
        self.zone_zoom.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_widget = imageZoomable.ImageZoomable("")
        self.zone_zoom.setWidget(self.image_widget)
        self.layout_image.addWidget(self.zone_zoom, stretch=1)

        # Bouton charger plan (centré si pas d'image) :
        self.bouton_charger_plan = QPushButton("Ouvrir un plan/une image")
        self.bouton_charger_plan.clicked.connect(self.ouvrir_dialogue_chargement)
        self.bouton_charger_plan.setFixedSize(200, 60)
        self.bouton_charger_plan.setVisible(True)
        self.setAcceptDrops(True)  # Permet le drag & drop sur la fenêtre

        # Layout pour centrer le bouton charger plan :
        self.layout_centre = QVBoxLayout()
        self.layout_centre.addStretch()
        self.layout_centre.addWidget(self.bouton_charger_plan, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout_centre.addStretch()
        self.layout_image.addLayout(self.layout_centre)

        # Contrôles pour la taille de la grille (Slider et boutons) :
        self.layout_grille = QHBoxLayout()
        self.bouton_moins = QPushButton("-")
        self.bouton_plus = QPushButton("+")
        self.slider_grille = QSlider(Qt.Orientation.Horizontal)
        self.slider_grille.setMinimum(5)
        self.slider_grille.setMaximum(500)
        self.slider_grille.setValue(80)
        self.slider_grille.setTickInterval(5)
        self.slider_grille.setSingleStep(1)
        self.bouton_gauche = QPushButton("←")
        self.bouton_droite = QPushButton("→")
        self.bouton_haut = QPushButton("↑")
        self.bouton_bas = QPushButton("↓")
        self.layout_grille.addWidget(self.bouton_moins)
        self.layout_grille.addWidget(self.slider_grille)
        self.layout_grille.addWidget(self.bouton_plus)
        self.layout_grille.addWidget(self.bouton_gauche)
        self.layout_grille.addWidget(self.bouton_droite)
        self.layout_grille.addWidget(self.bouton_haut)
        self.layout_grille.addWidget(self.bouton_bas)
        self.layout_principal.addLayout(self.layout_grille)

        # Ligne Paramètres pour les boutons "Supprimer le plan" et "Vider la grille"
        self.layout_params = QHBoxLayout()
        self.bouton_supprimer_plan = QPushButton("Supprimer le plan")
        self.bouton_supprimer_plan.clicked.connect(self.supprimer_plan)
        
        self.bouton_vider_grille = QPushButton("Vider la grille")
        self.bouton_vider_grille.clicked.connect(self.vider_grille)
        
        self.layout_params.addWidget(self.bouton_supprimer_plan)
        self.layout_params.addWidget(self.bouton_vider_grille)
        self.layout_principal.addLayout(self.layout_params)

        # Singaux :
        self.slider_grille.valueChanged.connect(self.image_widget.setTailleGrille)
        self.bouton_plus.clicked.connect(lambda: self.slider_grille.setValue(self.slider_grille.value() + 5))
        self.bouton_moins.clicked.connect(lambda: self.slider_grille.setValue(self.slider_grille.value() - 5))
        self.bouton_gauche.clicked.connect(lambda: self.image_widget.decalerGrille(-5, 0))
        self.bouton_droite.clicked.connect(lambda: self.image_widget.decalerGrille(5, 0))
        self.bouton_haut.clicked.connect(lambda: self.image_widget.decalerGrille(0, -5))
        self.bouton_bas.clicked.connect(lambda: self.image_widget.decalerGrille(0, 5))

        # Connexion du signal pour la sélection d'une case produit
        self.image_widget.produits_case_selectionnee.connect(self.reception_produits_case)

        # Connexion du signal
        #self.image_widget.matrice_generee.connect(self.afficher_matrice_console)

        self.mettre_a_jour_affichage()
        
        
    #=================================
    # Méthodes 
    #=================================

    def ouvrir_dialogue_chargement(self):
        # Ouvre un dialogue pour charger une image
        chemin, _ = QFileDialog.getOpenFileName(self, "Ouvrir un plan", "", "Images (*.png *.jpg *.jpeg)")
        if chemin :
            self.chemin_image = chemin
            self.image_widget.charger_image(chemin)
            self.mettre_a_jour_affichage()

    def supprimer_plan(self):
        # Popup de confirmation avant suppression du plan
        message = QMessageBox(self)
        message.setWindowTitle("Confirmation")
        message.setText("Voulez-vous vraiment supprimer le plan et toutes les cases ?")
        oui = message.addButton("Oui", QMessageBox.ButtonRole.YesRole)
        message.addButton("Non", QMessageBox.ButtonRole.NoRole)
        message.setDefaultButton(oui)
        message.exec()
        
        if message.clickedButton() == oui :
            self.chemin_image = None
            self.image_widget.supprimer_image()
            self.mettre_a_jour_affichage()

    def vider_grille(self):
        # Popup de confirmation avant de vider la grille
        message = QMessageBox(self)
        message.setWindowTitle("Confirmation")
        message.setText("Voulez-vous vraiment vider toutes les cases de la grille ?")
        oui = message.addButton("Oui", QMessageBox.ButtonRole.YesRole)
        message.addButton("Non", QMessageBox.ButtonRole.NoRole)
        message.setDefaultButton(oui)
        message.exec()
        
        if message.clickedButton() == oui :
            self.image_widget.vider_elt()
            self.image_widget.update()

    def mettre_a_jour_affichage(self):
        # Met à jour l'affichage en fonction de la présence d'une image ou non
        # Si une image est chargée, on affiche les contrôles et on active la grille
        if self.image_widget.avoir_image():
            self.zone_zoom.setVisible(True)
            self.bouton_charger_plan.setVisible(False)
            
            # Active les boutons de la grille et les paramètres :
            for i in range(self.layout_grille.count()):
                widget = self.layout_grille.itemAt(i).widget()
                if widget:
                    widget.setEnabled(True)
            for i in range(self.layout_params.count()):
                widget = self.layout_params.itemAt(i).widget()
                if widget:
                    widget.setEnabled(True)
                    
        # Si aucune image n'est chargée, on cache la zone de zoom et on désactive les contrôles
        else:
            self.zone_zoom.setVisible(False)
            self.bouton_charger_plan.setVisible(True)
            
            # Désactive les boutons de la grille et les paramètres
            for i in range(self.layout_grille.count()):
                widget = self.layout_grille.itemAt(i).widget()
                if widget:
                    widget.setEnabled(False)
            for i in range(self.layout_params.count()):
                widget = self.layout_params.itemAt(i).widget()
                if widget:
                    widget.setEnabled(False)

    def dragEnterEvent(self, event):
        # Accepte le glisser si c'est un fichier image de Qt
        if event.mimeData().hasUrls(): # Vérifie si des URLs sont présentes
            for url in event.mimeData().urls(): # Vérifie chaque URL
                if url.toLocalFile().lower().endswith(('.png', '.jpg', '.jpeg')): # Si le fichier est une image
                    event.acceptProposedAction() # Accepte l'action de glisser
                    return
        event.ignore() # Sinon, ignore l'événement (si ce n'est pas une image

    def dropEvent(self, event):
        # Ouvre la première image déposée
        if event.mimeData().hasUrls(): # Vérifie si des URLs sont présentes
            for url in event.mimeData().urls(): # Vérifie chaque URL
                chemin = url.toLocalFile() # Convertit l'URL en chemin de fichier
                if chemin.lower().endswith(('.png', '.jpg', '.jpeg')):
                    self.chemin_image = chemin
                    self.image_widget.charger_image(chemin)
                    self.mettre_a_jour_affichage()
                    break

    def reception_produits_case(self, produits):
        # Méthode appelée quand une case produit est sélectionnée (aucun type magasin sélectionné)
        # produits est une liste de str
        print("Produits de la case sélectionnée :", produits)

    def mettre_a_jour_matrice(self, matrice):
        # Met à jour la matrice de l'image_widget
        self.image_widget.recevoir_matrice(matrice)

    def connecter_signal_matrice(self, signal_externe):
        # Connecte un signal externe (qui émet une matrice) à l'entrée de l'image_widget
        signal_externe.connect(self.image_widget.matrice_a_appliquer)

# Programme principal : test de la vue ---------------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = Plan()
    fenetre.show()
    sys.exit(app.exec())