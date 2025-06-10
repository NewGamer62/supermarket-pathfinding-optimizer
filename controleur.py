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

class Controller:
    
    #==========================
    #== Constructeur :
    #==========================
    
    def __init__(self) -> None:
        
        # Attributs (Modele et Vue) :
        self.modele = modele.Projet()
        #self.vue = vue.Vue()
        
        # Signaux entrant / Signaux venant de la Vue :
        self.vue.OuvertureFichier.connect(self.ouvrirFichier)
        self.vue.EnregistrerFichier.connect(self.enregistrerFichier)
        self.vue.changementCase.connect(self.changementCase) #Il me faut les coordonnées du clic (x, y) (ajout/suppression de produits)
        self.vue.changementInfos.connect(self.changementInfos)


        
    #==========================
    #== Méthodes :
    #==========================
    
    def ouvrirFichier(self, chemin: str) -> None:
        '''
        Modifier
        '''
        self.modele = modele.Projet(chemin) 
    
    def enregistrerFichier(self, chemin: str) -> None:
        '''
        Modifier
        '''
        self.modele.enregistrer(chemin)
    
    def changementCase(self, x: int, y: int, contenu : list) -> None:
        '''
        Modifier
        '''
        self.modele.updateCase(x, y, contenu)
    
    def changementInfos(self, infos: dict) -> None:
        '''
        Modifier
        '''
        self.modele.setInfos(
            infos['nom'],
            infos['auteur'],
            infos['date_creation'],
            infos['nom_supermarche'],
            infos['adresse_supermarche'],
        )
    