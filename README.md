# Labyrinthe - IFT-2003 TP1

Application interactive en Python développée avec **Pygame** pour visualiser, 
tester et comparer des algorithmes de recherche de chemin.
---

##  1. Démarrage 

### Prérequis
- **Python 3.10** ou version supérieure installé sur votre machine.

### Installation

Selon le système d'exploitation :

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



## Fonctionnement du jeu

### Principe
L'objectif est de trouver un chemin de coût minimal menant de la case départ **START** jusqu'à la case sortie **EXIT** à travers une grille composée de cases. Les déplacements se font dans les 4 directions (haut, bas, gauche, droite), sans diagonale. Chaque case à un cout de 1, à l'exception des cases brunes qui ont un cout plus élevé. Ce cout est variable selon la case. Le labyrinthe comportent aussi des cases de type portail. Le fonctionnement de ces cases est expliqué plus bas.

### Les Éléments de la Grille & Légende Visuelle

| Élément | Couleur | Description |
| :--- | :--- | :--- |
| **Case de départ** | 🟢 Vert | Case `(0, 0)` en haut à gauche. |
| **Case de sortie** | 🔴 Rouge | Case `(39, 67)` en bas à droite. |
| **Cases libres** | ⚪ Blanc | Cases navigable coût de déplacement par défaut de **1**. |
| **Murs / Obstacles** | 🔘 Gris | Cases infranchissables bloquant le passage. |
| **Portails de téléportation** | 🟣 Violet / 🟠 Orange | Paire de case portail reliés dans les deux sens (voir ci-dessous). |
| **Terrain difficile** | 🟤 Brun | Cases à coût élevé. |
| **Chemin trouvé / Joueur** | 🔵 Bleu | Trajet calculé par l'algorithme sélectionné et position d'arrivée. |

### Coût d'un déplacement
- Le coût d'un déplacement est le coût de la **case dans laquelle on entre** (1 par défaut, plus pour une case lourde).
- Le coût total d'un chemin est la somme des coûts des cases traversées, sans compter la case de départ.

### Fonctionnement des portails
- Quand une case portail est développée, l'autre portail est ajouté à ses voisins, en plus des 4 voisins normaux.
- La téléportation est donc facultative : on peut passer sur un portail sans l'emprunter.
- Elle compte comme un déplacement et coûte le coût de la case d'arrivée (1).


### Heuristiques

Les deux heuristiques sont sélectionnables dans la barre d'outils et s'appliquent aux deux algorithmes.

Lorsque le niveau contient des portails, l'heuristique tient compte du raccourci possible en emprutant le portail.

C'est la distance « aller jusqu'au portail de départ, puis du portail d'arrivée jusqu'à la sortie », dans les deux sens, comparée à la distance directe.

Voir la fonction **heuristic_value** pour l'implémentation des heuristiques.

### Algorithmes de Recherche

Les deux algorithmes sont des techniques de **recherche heuristique**. Ils gèrent une liste CASES_OUVERTES, les cases générées mais pas encore explorées, sous la forme d'une de priorité (`heapq`). À chaque étape, ils retirent la première case de cette liste et génèrent ses cases voisines.

#### 1. Recherche du meilleur d'abord — *Greedy Best-First Search* (Algo 1)

À chaque étape de la recherche :
1. générer les cases accessibles depuis la case courante et leur attribuer une valeur heuristique.
2. ajouter ces cases à la liste CASES_OUVERTES.
3. ordonner CASES_OUVERTES selon la valeur heuristique.
4. choisir le premier élément de CASES_OUVERTES, c'est-à-dire celui dont la valeur heuristique est la plus petite.


#### 2. Algorithme A\* (Algo 2)

**A\*** est une extension de l'algorithme de Dijkstra avec ajout d'une heuristique. 

- choisir la première case de CASES_OUVERTES, la supprimer de CASES_OUVERTES et l'ajouter à CASES_FERMÉS ;
- développer ses cases voisines :
  - si une case voisine est dans CASES_FERMÉS, il n'est pas ajouté à CASES_OUVERTES ;
  - si une case voisine est déjà dans CASES_OUVERTES avec une valeur plus grande, elle est remplacée ; sinon, elle n'est pas ajoutée.
---

## Contrôles & Utilisation

Étant donné que le l'objectif du TP n'est pas la création d'un jeu intéractif, le UI a été grandement fait à l'aide intéligence artificielle. 

### Actions à la Souris
- **Placer des murs** : Clic gauche maintenu / glissé sur la grille.
- **Supprimer des murs** : Clic droit maintenu / glissé sur la grille.
- **Interagir avec la barre d'outils** : Cliquez sur les boutons pour changer d'algorithme ou d'heuristique, charger un niveau, lancer ou réinitialiser.

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
| <kbd>Y</kbd> | Charger le **Niveau 6**. |
| <kbd>U</kbd> | Charger le **Niveau 7**. |

Le choix de l'heuristique (Manhattan / Euclidienne) se fait uniquement par les boutons de la barre d'outils.

---

## Métriques & performance

Lors de chaque exécution, 4 statistiques clés sont affichées dans la barre d'outils inférieure ainsi que dans la console :

1. **Nœuds développés** : Nombre de cases retirées de la file et développées par l'algorithme, case de sortie comprise (l'effort de calcul).
2. **Profondeur (Pas)** : Nombre de déplacements du chemin final. Une téléportation compte pour un pas.
3. **Temps d'exécution** : Durée de calcul de la solution en millisecondes (en `ms`).
4. **Coût total (Qualité)** : Somme des coûts des cases traversées. Permet de vérifier l'optimalité de la solution. Sur les niveaux pondérés, il peut différer de la profondeur.

### Résultats de référence - variable selon l'environnement d'exécution

| Niveau | Coût optimal | A\* — nœuds (Manh. / Eucl.) | Greedy — coût (Manh. / Eucl.) | Greedy — nœuds (Manh. / Eucl.) |
| :---: | :---: | :---: | :---: | :---: |
| 1 | 49 | 176 / 254 | 51 / 51 | 136 / 109 |
| 2 | 29 | 84 / 124 | 29 / 29 | 31 / 30 |
| 3 | 351 | 1170 / 1198 | 359 / 369 | 895 / 939 |
| 4 | 73 | 352 / 456 | 75 / 75 | 101 / 90 |
| 5 | 90 | 478 / 616 | 98 / 101 | 101 / 90 |
| 6 | 130 | 2476 / 2481 | 186 / 210 | 1938 / 1990 |
| 7 | 106 | 902 / 1470 | 208 / 248 | 90 / 90 |


---

## Quoi fait quoi 

| Fichier | Rôle & Responsabilité |
| :--- | :--- |
| `ift-2003-tp.py` | Fichier principal. Il contient le nécéssaire pour la génération de labyrinthe, les calculs d'heuristiques, ainsi que les algorithmes `algo_1` (Greedy) et `algo_AStar`. |
| `level_1.py` | **Niveau 1** Démontre le gain obtenus pas les portails. |
| `level_2.py` | **Niveau 2** Greedy (peut) être plus éfficace que A*. |
| `level_3.py` | **Niveau 3** L'influence de la qualité d'information de l'heuristique. |
| `level_4.py` | **Niveau 4** Labyrinthe standard |
| `level_5.py` | **Niveau 5** Permet d'observer l'impact d'ajouter des cases lourdes au niveau 4 |
| `level_6.py` | **Niveau 6** Piège pour l'algo Greedy |
| `level_7.py` | **Niveau 7** L'impact du choix de l'heuristique|
| `test_dijkstra.py` | Fichier de tests unitaires (`unittest`) validant le comportement de recherche de chemin sur des grilles réduites. |
| `requirements.txt` | Liste des dépendances requises pour l'environnement Python (`pygame-ce`). |
| `install.bat` | Script batch pour automatiser la mise à jour de `pip` et l'installation sous Windows (CMD). |
| `install.ps1` | Script PowerShell pour automatiser l'installation des dépendances sous Windows. |
| `install.sh` | Script Shell pour automatiser l'installation des dépendances sous Linux et macOS. |
| `README.md` | Guide utilisateur complet et documentation technique du projet. |



---

