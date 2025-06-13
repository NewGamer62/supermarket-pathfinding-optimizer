# Formation : BUT 1ʳᵉ année | 2024-2025
# Ressource : SAE S2 - Algo et Graphes
# Professeur : M. Conoir
# Noms :  AMEDRO Louis (TPD)
#         HERBAUX Jules (TPD)
#         GAILLARD Noa (TPC)
#         MINNEBO Valentin (TPA)

import modele, vue
from datetime import datetime

#=====================================
#== Classe Controleur :
#=====================================

class Controleur:
    
    #==========================
    #== Constructeur :
    #==========================
    
    def __init__(self) -> None:
        
        # Attributs (Modele et Vue) :
        self.modele = modele.Projet()
        self.vue = vue.Vue()
        
        # Connexions des signaux venant de la Vue :
        self.vue.OuvertureFichier.connect(self.ouvrirFichier)
        self.vue.EnregistrerFichier.connect(self.enregistrerFichier)
        self.vue.changementCase.connect(self.changementCase)
        self.vue.changementInfos.connect(self.changementInfos)
        self.vue.matrice_generee.connect(self.modele.supermarche.setQuadrillage)
        # Synchronisation initiale
        self.synchroniser_vue_modele()
        
    #==========================
    #== Méthodes :
    #==========================

    def ouvrirFichier(self, chemin: str) -> None:
        self.modele = modele.Projet(chemin)
        self.vue.plan.image_widget.matrice_a_appliquer(self.modele.supermarche.getQuadrillage())
        # Synchroniser la taille de la grille à partir du modèle (lecture de la matrice)
        quadrillage = self.modele.supermarche.getQuadrillage()
        taille_grille = 80  # Valeur par défaut si la matrice est vide
        min_slider = self.vue.plan.slider_grille.minimum() if hasattr(self.vue.plan, "slider_grille") else 20
        max_slider = self.vue.plan.slider_grille.maximum() if hasattr(self.vue.plan, "slider_grille") else 500
        if quadrillage and len(quadrillage) > 0 and len(quadrillage[0]) > 0:
            largeur_image = self.vue.plan.image_widget.image.width()
            nb_colonnes = len(quadrillage[0])
            if nb_colonnes > 0:
                taille_grille = max(min_slider, min(int(largeur_image / nb_colonnes), max_slider))
        self.vue.plan.set_taille_grille(taille_grille)
        # Synchroniser les infos à droite
        self.vue.informations.setInfos(self.modele.informations.getInfos())
        # Charger l'image du dossier si elle existe
        self.charger_image_depuis_dossier(chemin)

    def synchroniser_vue_modele(self):
        # Synchronise les infos et la liste des produits du modèle vers la vue
        infos = self.modele.informations.getInfos()
        self.vue.informations.setInfos(infos)
        # Synchronise la matrice du plan
        self.vue.plan.image_widget.matrice_a_appliquer(self.modele.supermarche.getQuadrillage())
        # Synchronise l'image si besoin (optionnel, à appeler si nécessaire)

    def charger_image_depuis_dossier(self, dossier):
        #Cherche une image dans le dossier supermarche et la charge dans la vue si trouvée.
        import os
        dossier_supermarche = os.path.join(dossier, "supermarche")
        if not os.path.exists(dossier_supermarche):
            return
        for nom in ["plan.png", "plan.jpg", "plan.jpeg"]:
            chemin_image = os.path.join(dossier_supermarche, nom)
            if os.path.exists(chemin_image):
                self.vue.plan.set_image(chemin_image)
                break

    def enregistrerFichier(self, chemin: str) -> None:
        # Synchronise les infos et produits de la vue vers le modèle avant sauvegarde
        infos = self.vue.informations.getInfos()
        # Synchroniser la matrice de la vue vers le modèle (ajouté)
        matrice_vue = self.vue.plan.image_widget.generer_matrice()
        self.modele.supermarche.setQuadrillage(matrice_vue)
        # Conversion de la date si besoin
        date_creation = infos['date création']
        if isinstance(date_creation, str):
            try:
                # Essaye de parser la date au format français
                date_creation = datetime.strptime(date_creation, "%d/%m/%Y").date()
            except Exception:
                # Sinon, laisse la chaîne telle quelle (le modèle lèvera une erreur si ce n'est pas une date)
                pass
        self.modele.informations.setInfos(
            infos['nom'],
            infos['auteur'],
            date_creation,
            infos['nom supermarché'],
            infos['adresse supermarché'],
        )
        self.modele.ecrireDossier(chemin)

    def changementCase(self, x: int, y: int, contenu : list) -> None:
        # Vérifie et agrandit le quadrillage si besoin avant modification
        quadrillage = self.modele.supermarche.getQuadrillage()
        hauteur = len(quadrillage)
        longueur = len(quadrillage[0]) if hauteur > 0 else 0
        if y >= hauteur:
            self.modele.supermarche.setHauteur(y + 1)
        if x >= longueur:
            self.modele.supermarche.setLongueur(x + 1)
        # Après agrandissement éventuel, on peut modifier la case
        self.modele.supermarche.setCase(x, y, contenu)
        
        if not contenu in ["entrée", "caisse", "mur", "sol", ""] and contenu != []: 
            self.modele.supermarche.ajouterProduit(contenu[0])
        elif contenu == "" :
            self.modele.supermarche.setListeProduits([])

    def changementInfos(self, infos: dict) -> None:
        self.modele.informations.setInfos(
            infos['nom'],
            infos['auteur'],
            infos['date création'],
            infos['nom supermarché'],
            infos['adresse supermarché'],
        )
