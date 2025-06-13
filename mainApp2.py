# Formation : BUT 1ʳᵉ année | 2024-2025
# Ressource : SAE S2 - Algo et Graphes
# Professeur : M. Conoir
# Noms :  AMEDRO Louis (TPD)
#         HERBAUX Jules (TPD)
#         GAILLARD Noa (TPC)
#         MINNEBO Valentin (TPA)

import sys
from PyQt6.QtWidgets import QApplication
from controapp2 import Controleur  # Assure-toi que ce nom correspond au bon fichier "controleur.py"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controleur_instance = Controleur()
    controleur_instance.vue.show()
    sys.exit(app.exec())