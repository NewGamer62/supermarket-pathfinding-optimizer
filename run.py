"""
Lanceur universel pour la suite Supermarket Pathfinding & Spatial Optimizer.
Permet d'exécuter facilement l'application 1 (Éditeur) ou l'application 2 (Optimiseur).

Usage :
    python run.py 1   # Lance l'Éditeur Spatial (App 1)
    python run.py 2   # Lance le Calculateur de Parcours (App 2)
"""

import sys
import subprocess
from pathlib import Path

def check_dependencies():
    missing = []
    try:
        import PyQt6
    except ImportError:
        missing.append("PyQt6")
    try:
        import numpy
    except ImportError:
        missing.append("numpy")
    
    if missing:
        print(f"\n[!] Dependance(s) manquante(s) : {', '.join(missing)}")
        print("    Veuillez installer les prerequis avec : pip install -r requirements.txt\n")
        return False
    return True

def main():
    root = Path(__file__).parent.resolve()
    
    choice = sys.argv[1] if len(sys.argv) > 1 else None
    
    if not choice:
        print("=== Supermarket Pathfinding & Spatial Optimizer ===")
        print("1. Lancer l'Éditeur Spatial (premiereApp)")
        print("2. Lancer le Calculateur de Parcours (deuxiemeApp)")
        print("Q. Quitter")
        choice = input("\nChoisissez une option (1/2/Q) : ").strip()

    if choice in ("1", "2") and not check_dependencies():
        sys.exit(1)

    if choice == "1":
        target = root / "premiereApp" / "main.py"
        cwd = root / "premiereApp"
        print(f"Lancement de l'Éditeur Spatial ({target})...")
        subprocess.run([sys.executable, str(target)], cwd=str(cwd))
    elif choice == "2":
        target = root / "deuxiemeApp" / "mainApp2.py"
        cwd = root / "deuxiemeApp"
        print(f"Lancement du Calculateur de Parcours ({target})...")
        subprocess.run([sys.executable, str(target)], cwd=str(cwd))
    elif choice.lower() in ("q", "quit", "exit"):
        print("Annulé.")
    else:
        print(f"Option inconnue : '{choice}'. Utilisez 1 ou 2.")
        sys.exit(1)

if __name__ == "__main__":
    main()
