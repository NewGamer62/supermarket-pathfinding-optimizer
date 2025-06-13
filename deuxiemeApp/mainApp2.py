# Formation : BUT 1ʳᵉ année | 2024-2025
# Ressource : SAE S2 - Algo et Graphes
# Professeur : M. Conoir
# Noms :  AMEDRO Louis (TPD)
#         HERBAUX Jules (TPD)
#         GAILLARD Noa (TPC)
#         MINNEBO Valentin (TPA)

# --------------- #
# --- Modules --- #
# --------------- #

import sys
from PyQt6.QtWidgets import QApplication
import controApp2

# ------------ #
# --- Main --- #
# ------------ #

if __name__ == "__main__" :
    
    """Lance l'application n°2"""
    
    app = QApplication(sys.argv)
    controleur_instance = controApp2.Controleur()
    sys.exit(app.exec())