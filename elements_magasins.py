import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QApplication)
from PyQt6.QtCore import pyqtSignal

# ----------------------------------------------------------------------------- 
# --- class ElementsMagasin
# -----------------------------------------------------------------------------
class ElementsMagasin(QWidget):

    signal_element = pyqtSignal(str)  # ✅ Signal général pour envoyer "Mur", "Caisse", "Entree"

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Mur
        self.mettreMur = QPushButton("🧱 Mettre un mur")
        layout.addWidget(self.mettreMur)
        self.mettreMur.clicked.connect(self.mur)

        # Caisse
        self.mettreCaisse = QPushButton("💰️ Mettre une caisse")
        layout.addWidget(self.mettreCaisse)
        self.mettreCaisse.clicked.connect(self.caisse)

        # Entrée
        self.mettreEntree = QPushButton("⬆️ Mettre une entrée")
        layout.addWidget(self.mettreEntree)
        self.mettreEntree.clicked.connect(self.entree)

    def mur(self):
        self.signal_element.emit("mur")

    def caisse(self):
        self.signal_element.emit("caisse")

    def entree(self):
        self.signal_element.emit("entree")

# Programme principal : test de la vue ---------------------------------------
if __name__ == "__main__":
    def afficher_element(element):
        print(f"🛠️ Élément choisi : {element}")

    print(f' --- main --- ')
    app = QApplication(sys.argv)

    fenetre = ElementsMagasin()
    fenetre.signal_element.connect(afficher_element)  # 🔗 Connexion du signal au slot
    fenetre.show()

    sys.exit(app.exec())
