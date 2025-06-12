# Formation : BUT 1ʳᵉ année | 2024-2025
# Ressource : SAE S2 - Algo et Graphes
# Professeur : M. Conoir
# Noms :  AMEDRO Louis (TPD)
#         HERBAUX Jules (TPD)
#         GAILLARD Noa (TPC)
#         MINNEBO Valentin (TPA)

import modele, vue

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

    def ouvrirFichier(self, chemin: str) -> None:
        '''
        Modifier
        '''
        self.modele = modele.Projet(chemin)
        self.vue.plan.image_widget.matrice_a_appliquer(self.modele.supermarche.getQuadrillage())
        self.synchroniser_vue_modele()

    def synchroniser_vue_modele(self):
        # Synchronise les infos et la liste des produits du modèle vers la vue
        infos = self.modele.informations.getInfos()
        #à mettre dans la vue (plan->image chemin et infos) !!!
        

    def enregistrerFichier(self, chemin: str) -> None:
        '''
        Modifier
        '''
        # Synchronise les infos et produits de la vue vers le modèle avant sauvegarde
        if hasattr(self.vue.informations, "getInfos"):
            infos = self.vue.informations.getInfos()
            self.modele.informations.setInfos(
                infos['nom'],
                infos['auteur'],
                infos['date création'],
                infos['nom supermarché'],
                infos['adresse supermarché'],
            )
        if hasattr(self.vue.listeProduits, "getProduits"):
            produits = self.vue.listeProduits.getProduits()
            self.modele.supermarche.setListeProduits(produits)
        self.modele.ecrireDossier(chemin)

    def changementCase(self, x: int, y: int, contenu : list) -> None:
        '''
        Modifier
        '''
        # Vérifie et agrandit le quadrillage si besoin avant modification
        quadrillage = self.modele.supermarche.getQuadrillage()
        hauteur = len(quadrillage)
        longueur = len(quadrillage[0]) if hauteur > 0 else 0
        agrandir = False
        if y >= hauteur:
            self.modele.supermarche.setHauteur(y + 1)
            agrandir = True
        if x >= longueur:
            self.modele.supermarche.setLongueur(x + 1)
            agrandir = True
        # Après agrandissement éventuel, on peut modifier la case
        self.modele.supermarche.setCase(x, y, contenu)

    def changementInfos(self, infos: dict) -> None:
        '''
        Modifier
        '''
        self.modele.informations.setInfos(
            infos['nom'],
            infos['auteur'],
            infos['date création'],
            infos['nom supermarché'],
            infos['adresse supermarché'],
        )
