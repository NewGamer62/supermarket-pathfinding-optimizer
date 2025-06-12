# Formation : BUT 1ʳᵉ année | 2024-2025
# Ressource : SAE S2 - Algo et Graphes
# Professeur : M. Conoir
# Noms :  AMEDRO Louis (TPD)
#         HERBAUX Jules (TPD)
#         GAILLARD Noa (TPC)
#         MINNEBO Valentin (TPA)

from PyQt6.QtWidgets import QApplication
import sys, controleur

# --- main ---
if __name__ == "__main__":

    print('\n--- main ---\n')

    # Création d'une QApplication
    app = QApplication(sys.argv)
    
    # Création du Contrôleur :
    controleur_instance = controleur.Controleur()

    # Affichage de la Vue du Contrôleur
    controleur_instance.vue.show()
    
    # lancement de l'application  
    sys.exit(app.exec())