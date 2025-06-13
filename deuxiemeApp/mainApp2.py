# Formation : BUT 1ʳᵉ année | 2024-2025
# Ressource : SAE S2 - Algo et Graphes
# Professeur : M. Conoir
# Noms :  AMEDRO Louis (TPD)
#         HERBAUX Jules (TPD)
#         GAILLARD Noa (TPC)
#         MINNEBO Valentin (TPA)

import sys
from PyQt6.QtWidgets import QApplication
import controApp2

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controleur_instance = controApp2.Controleur()
    controleur_instance.vue.show()
    sys.exit(app.exec())