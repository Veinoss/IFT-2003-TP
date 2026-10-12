# Labyrinth AI - IFT-2003 TP

Application interactive en Python développée avec **Pygame** (`pygame-ce`) pour visualiser, tester et comparer des algorithmes de recherche de chemin (*pathfinding*) dans un environnement de grille dynamique supportant des obstacles, des portails de téléportation et des terrains pondérés.

---

## ⚡ 1. Démarrage Rapide

### Prérequis
- **Python 3.10** ou version supérieure installé sur votre machine.

### Installation

Choisissez la méthode adaptée à votre système d'exploitation :

- **Windows (Double-clic ou Invite de commandes)** :
  ```cmd
  install.bat
  ```
- **Windows (PowerShell)** :
  ```powershell
  .\install.ps1
  ```
- **Linux / macOS (Bash)** :
  ```bash
  chmod +x install.sh
  ./install.sh
  ```
- **Installation manuelle (tous systèmes)** :
  ```bash
  pip install -r requirements.txt
  ```

### Lancement du jeu
Exécutez simplement la commande suivante à la racine du projet :
```bash
python ift-2003-tp.py
```

---

## 🧠 2. Comment fonctionne le jeu ?

### Le Principe
L'objectif est de trouver un chemin optimal menant du point de départ **START** jusqu'à la sortie **EXIT** à travers une grille de **40 lignes × 68 colonnes**.

### Les Éléments de la Grille & Légende Visuelle

| Élément | Couleur | Description |
| :--- | :--- | :--- |
| **Point de départ** | 🟢 Vert | Position initiale `(0, 0)` en haut à gauche. |
| **Sortie (Cible)** | 🔴 Rouge | Destination finale `(39, 67)` en bas à droite. |
| **Cases libres** | ⚪ Blanc | Zones praticables avec un coût de déplacement par défaut de **1**. |
| **Murs / Obstacles** | ⚫ / 🔘 Gris | Cases infranchissables bloquant le passage. |
| **Portails de téléportation** | 🟣 Violet / 🟠 Orange | Paire de portails reliés entre eux. Entrer sur l'un permet d'en ressortir instantanément par l'autre. |
| **Terrain difficile** | 🟤 Marron | Cases à coût élevé (de 4 à 10 au Niveau 5) simulant un terrain lourd. |
| **Chemin trouvé / Joueur** | 🔵 Bleu | Trajet calculé par l'algorithme sélectionné et position d'arrivée. |

### Les Algorithmes de Recherche

Deux algorithmes d'exploration sont intégrés et comparables :

1. **Greedy Best-First Search (Algo 1)** :
   - **Principe** : Explore en priorité les cases minimisant la distance de Manhattan ($|x_1 - x_2| + |y_1 - y_2|$) vers la sortie.
   - **Caractéristiques** : Très rapide pour trouver une solution dans les grands espaces dégagés, mais **non optimal** (il ignore le coût cumulé du trajet et peut faire de longs détours face à des obstacles ou des terrains lourds).
2. **A\* Search (Algo 2)** :
   - **Principe** : Fonction d'évaluation $f(n) = g(n) + h(n)$, où $g(n)$ est le coût réel cumulé depuis le départ et $h(n)$ est l'heuristique basée sur la distance euclidienne ($\sqrt{\Delta x^2 + \Delta y^2}$).
   - **Caractéristiques** : **Optimal et complet**. Il calcule le chemin de coût minimal en arbitrant intelligemment entre les détours, l'usage des portails et la traversée de cases à coût élevé.

---

## 🎮 3. Contrôles & Utilisation

### Actions à la Souris
- **Placer des murs** : Clic gauche maintenu / glissé sur la grille.
- **Supprimer des murs** : Clic droit maintenu / glissé sur la grille.
- **Interagir avec la barre d'outils** : Cliquez sur les boutons pour changer d'algorithme, charger un niveau, lancer ou réinitialiser.

### Raccourcis Clavier

| Touche | Action |
| :---: | :--- |
| <kbd>ESPACE</kbd> | **Lancer la recherche** avec l'algorithme actif. |
| <kbd>C</kbd> | **Effacer** tous les murs et réinitialiser la grille. |
| <kbd>1</kbd> / <kbd>Num 1</kbd> | Sélectionner **Greedy Best-First** (Algo 1). |
| <kbd>2</kbd> / <kbd>Num 2</kbd> | Sélectionner **A\*** (Algo 2). |
| <kbd>Q</kbd> | Charger le **Niveau 1**. |
| <kbd>W</kbd> | Charger le **Niveau 2**. |
| <kbd>E</kbd> | Charger le **Niveau 3**. |
| <kbd>R</kbd> | Charger le **Niveau 4**. |
| <kbd>T</kbd> | Charger le **Niveau 5**. |

---

## 📊 4. Métriques & Comparaison de Performance

Lors de chaque exécution, 4 statistiques clés sont affichées dans la barre d'outils inférieure ainsi que dans la console :

1. **Nœuds développés** : Nombre total de cases explorées par l'algorithme (mesure l'effort de calcul et la mémoire explorée).
2. **Profondeur (Pas)** : Nombre d'étapes (cases) composant le chemin final.
3. **Temps d'exécution** : Durée de calcul de la solution en millisecondes (`ms`).
4. **Coût total (Qualité)** : Somme des coûts des cases traversées. Permet de vérifier l'optimalité de la solution.

---

## 🗺️ 5. Description des Niveaux Pré-faits

- **Niveau 1 - Dédale arborescent** : Labyrinthe classique généré par parcours en profondeur (DFS) avec bifurcations, impasses et portails raccourcis.
- **Niveau 2 - Citadelle des Salles & Couloirs** : Architecture de type donjon composée de 9 salles fortifiées reliées par des galeries sinueuses.
- **Niveau 3 - Chicanes Sectorisées** : Labyrinthe structuré en 4 grands secteurs horizontaux séparés par des cloisons et des rétrécissements.
- **Niveau 4 - Grand Dédale Haute Densité** : Labyrinthe complexe très dense avec de multiples embranchements et carrefours.
- **Niveau 5 - Terrains Variés & Pondérés** : Même topologie que le niveau 4, mais intégrant des **zones de boue / terrain lourd** à coût élevé (4 à 10) forçant A* à arbitrer entre traversée coûteuse et contournement.

---

## 📂 6. Architecture du Projet (« Quoi fait quoi »)

| Fichier | Rôle & Responsabilité |
| :--- | :--- |
| `ift-2003-tp.py` | **Point d'entrée principal**. Gère la fenêtre Pygame, la boucle d'événements, le dessin de la grille et de la toolbar, les calculs d'heuristiques, ainsi que les algorithmes `algo_1` (Greedy) et `algo_AStar`. |
| `level_1.py` | Générateur du **Niveau 1** (labyrinthe arborescent DFS déterministe avec portails). |
| `level_2.py` | Générateur du **Niveau 2** (salles géométriques, couloirs et téléporteurs). |
| `level_3.py` | Générateur du **Niveau 3** (murs horizontaux et chicanes régulières). |
| `level_4.py` | Générateur du **Niveau 4** (dédale haute densité avec carrefours stratégiques). |
| `level_5.py` | Générateur du **Niveau 5** (dédale haute densité avec définition des cases pondérées `HEAVYCOST_TILES`). |
| `test_dijkstra.py` | Fichier de tests unitaires (`unittest`) validant le comportement de recherche de chemin sur des grilles réduites. |
| `requirements.txt` | Liste des dépendances requises pour l'environnement Python (`pygame-ce`). |
| `install.bat` | Script batch pour automatiser la mise à jour de `pip` et l'installation sous Windows (CMD). |
| `install.ps1` | Script PowerShell pour automatiser l'installation des dépendances sous Windows. |
| `install.sh` | Script Shell pour automatiser l'installation des dépendances sous Linux et macOS. |
| `README.md` | Guide utilisateur complet et documentation technique du projet. |
