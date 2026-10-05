# Labyrinth AI - IFT-2003 TP

Application interactive en Python utilisant **Pygame** (`pygame-ce`) pour visualiser et tester des algorithmes de recherche de chemin (*pathfinding*) dans une grille dynamique.

---

## 📌 Fonctionnalités

- **Grille interactive** : Grille configurable (12 lignes × 16 colonnes par défaut).
- **Édition du labyrinthe en direct** : Ajout et suppression intuitive d'obstacles à la souris.
- **Résolution de chemin** : Visualisation du chemin trouvé entre le point de départ et la sortie.
- **Support multiplateforme** : Compatible Windows, macOS et Linux avec scripts d'installation automatisés.

---

## 🚀 Installation

### 1. Prérequis
- **Python 3.10** ou version ultérieure.

### 2. Installation automatique

- **Windows (PowerShell)** :
  ```powershell
  .\install.ps1
  ```
- **Windows (Invite de commandes / Double-clic)** :
  ```cmd
  install.bat
  ```
- **Linux / macOS (Bash)** :
  ```bash
  chmod +x install.sh
  ./install.sh
  ```

### 3. Installation manuelle
```bash
pip install -r requirements.txt
```

---

## 🎮 Lancement et Utilisation

Pour lancer l'application :
```bash
python ift-2003-tp.py
```

### Contrôles

| Action | Contrôle | Description |
| :--- | :--- | :--- |
| **Ajouter un mur** | Clic gauche | Place un obstacle sur la case survolée. |
| **Supprimer un mur** | Clic droit | Retire l'obstacle et réinitialise le chemin. |
| **Lancer la recherche** | <kbd>ESPACE</kbd> | Calcule et affiche le chemin optimal jusqu'à la sortie. |
| **Effacer la grille** | <kbd>C</kbd> | Réinitialise l'ensemble des murs et le chemin. |
| **Quitter** | Croix / Fermer | Quitte l'application. |

### Légende visuelle

- 🟢 **Vert** : Point de départ `(0, 0)`
- 🔴 **Rouge** : Sortie cible `(Lignes - 1, Colonnes - 1)`
- ⚪ **Blanc** : Cases libres
- ⚫ / 🔘 **Gris** : Murs / Obstacles
- 🔵 **Bleu** : Chemin trouvé / Joueur

---

## 📂 Structure du projet

```text
IFT-2003-TP/
├── ift-2003-tp.py       # Code source principal de l'application et algorithme de recherche
├── requirements.txt     # Dépendances Python (pygame-ce)
├── install.bat          # Script d'installation automatique pour Windows (CMD)
├── install.ps1          # Script d'installation automatique pour Windows (PowerShell)
├── install.sh           # Script d'installation automatique pour Linux / macOS
└── README.md            # Documentation du projet
```
