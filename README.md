# 🛒 Supermarket Pathfinding & Spatial Optimizer

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/GUI-PyQt6%20%2F%20Custom%20QSS-41CD52?style=for-the-badge&logo=qt&logoColor=white" alt="PyQt6" />
  <img src="https://img.shields.io/badge/Architecture-MVC%20Strict-orange?style=for-the-badge" alt="MVC" />
  <img src="https://img.shields.io/badge/Th%C3%A9orie-Algorithmes%20de%20Graphes-purple?style=for-the-badge" alt="Graphes" />
  <img src="https://img.shields.io/badge/SAÉ-BUT%20Informatique-blueviolet?style=for-the-badge" alt="SAÉ BUT Informatique" />
</p>

---

## 📌 Présentation

**Supermarket Pathfinding & Spatial Optimizer** est une suite logicielle d'ingénierie spatiale et algorithmique conçue pour optimiser l'aménagement de grandes surfaces commerciales et automatiser le calcul d'itinéraires de collecte de produits.

Le projet repose sur deux applications découplées articulées autour d'une architecture Modèle-Vue-Contrôleur (MVC) rigoureuse :
1. **Éditeur de Modélisation Spatiale (App 1)** : Outil de CAO permettant de quadriller un plan de masse, d'agencer les rayons, obstacles, allées, caisses et points d'accès, et d'associer des métadonnées produits (catégorie, coordonnées matricielles).
2. **Moteur d'Optimisation de Parcours (App 2)** : Système d'assistance au parcours client et à la préparation de commandes. À partir d'une liste de courses saisie, l'application modélise le magasin sous forme de graphe connexe et calcule le trajet le plus court minimisant la distance totale parcourue.

---

## ✨ Fonctionnalités Clés

- **Modélisation Spatiale & Matrice Discrète** :
  - Discrétisation spatiale 2D avec gestion du zoom dynamique, de la grille d'ancrage et des zones de collision.
  - Positionnement interactif des éléments (murs, têtes de gondole, caisses, sas d'entrée).
  - Gestion de l'inventaire produit indexé par cellules avec persistance sérialisée.
- **Résolution Algorithmique de Chemins Optimaux** :
  - Modélisation du supermarché en graphe non-orienté pondéré (nœuds = intersections/rayons, arêtes = allées praticables).
  - Calcul de plus court chemin entre points d'intérêt multiples et ordonnancement de collecte.
- **Interface Utilisateur Réactive (PyQt6)** :
  - Thèmes sombre et clair personnalisés via des feuilles de style QSS modulaires.
  - Vues découplées : bandeau d'outils, panneau d'informations contextuelles, liste d'inventaire interactive et canevas vectoriel.

---

## 🛠️ Architecture Logicielle

Le projet applique une séparation stricte des responsabilités (MVC) :

```
supermarket-pathfinding-optimizer/
├── premiereApp/               # Application 1 : Éditeur et Modeleur de plan
│   ├── main.py                # Point d'entrée App 1
│   ├── controleur.py          # Logique d'orchestration & liaison Modèle/Vue
│   ├── modele.py              # Structures de données spatiales & gestion d'inventaire
│   ├── vue.py                 # Fenêtre principale et assemblage des composants UI
│   ├── vueBandeau.py          # Barre d'outils d'édition
│   ├── vueInformations.py     # Panneau d'informations et détails cellule
│   └── vueListeProduits.py    # Explorateur et gestion des références produits
├── deuxiemeApp/               # Application 2 : Moteur de navigation & optimisation
│   ├── mainApp2.py            # Point d'entrée App 2
│   ├── controApp2.py          # Contrôleur dédié au routage et à la recherche
│   ├── vueApp2.py             # Interface de sélection de liste et tracé du parcours
│   └── filepile.py            # Structures algorithmiques et parcours de graphes
├── Sauvegarde-Test/           # Plans d'exemple sérialisés pour démonstration
├── annexes/                   # Ressources graphiques, maquettes et charte
├── requirements.txt           # Dépendances Python (PyQt6, numpy)
├── run.py                     # Lanceur universel CLI
└── README.md
```

---

## 👨‍💻 Rôle & Contributions Personnelles (Noa Gaillard)

Au sein de l'équipe de développement :
- **Design UI/UX & Prototypage** : Co-conception des maquettes complètes sous Figma pour structurer l'expérience utilisateur et l'ergonomie des deux applications.
- **Développement Front-End PyQt6 (App 1)** : Conception et implémentation des composants `vueInformations.py` et `vueListeProduits.py`, intégrant le scroll dynamique et la mise à jour temps réel des états de sélection.
- **Architecture & Développement de l'Application 2** : Conception intégrale de l'interface `vueApp2.py` et développement du contrôleur `controApp2.py` faisant la passerelle entre le modèle de données spatiales et le calcul de parcours.
- **Refactoring & Qualité de Code** : Harmonisation des standards de nommage, documentation interne (docstrings) et résolution des conflits d'intégration entre branches de vues et contrôleur.

---

## 🚀 Démarrage Rapide

### 1. Installation des dépendances

```bash
pip install -r requirements.txt
```

### 2. Lancement des applications

#### Option A : Via le lanceur universel (Recommandé)
```bash
python run.py 1   # Lance l'Éditeur Spatial (App 1)
python run.py 2   # Lance le Calculateur de Parcours (App 2)
```

Ou sous PowerShell :
```powershell
.\run_app1.ps1    # App 1
.\run_app2.ps1    # App 2
```

#### Option B : Lancement direct par dossier
```bash
# Éditeur Spatial (App 1)
cd premiereApp && python main.py

# Calculateur de Parcours (App 2)
cd deuxiemeApp && python mainApp2.py
```
*Astuce : Vous pouvez ouvrir directement un plan d'exemple situé dans le répertoire `Sauvegarde-Test/` depuis le menu Fichier.*
