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

### Résultats de référence

| Niveau | Coût optimal | A\* — nœuds (Manh. / Eucl.) | Greedy — coût (Manh. / Eucl.) | Greedy — nœuds (Manh. / Eucl.) |
| :---: | :---: | :---: | :---: | :---: |
| 1 | 49 | 176 / 254 | 51 / 51 | 136 / 109 |
| 2 | 29 | 84 / 124 | 29 / 29 | 31 / 30 |
| 3 | 351 | 1170 / 1198 | 359 / 369 | 895 / 939 |
| 4 | 73 | 352 / 456 | 75 / 75 | 101 / 90 |
| 5 | 90 | 478 / 616 | 98 / 101 | 101 / 90 |
| 6 | 130 | 2476 / 2481 | 186 / 210 | 1938 / 1990 |
| 7 | 106 | 902 / 1470 | 208 / 248 | 90 / 90 |

A\* atteint le coût optimal sur tous les niveaux, avec les deux heuristiques ; ce coût a été vérifié par un algorithme de Dijkstra indépendant. Manhattan développe moins de nœuds que l'euclidienne, car elle est plus proche du vrai coût sur une grille à 4 directions.

---

## Description des Niveaux Pré-faits

- **Niveau 1 - Dédale arborescent** : Labyrinthe classique généré par parcours en profondeur (DFS) avec bifurcations, impasses et portails raccourcis.
- **Niveau 2 - Citadelle des Salles & Couloirs** : Architecture de type donjon composée de 9 salles reliées par des galeries sinueuses, avec téléportation entre deux salles fortifiées.
- **Niveau 3 - Chicanes Sectorisées** : Labyrinthe structuré en 4 grands secteurs horizontaux séparés par des cloisons et des rétrécissements.
- **Niveau 4 - Grand Dédale Haute Densité** : Labyrinthe complexe très dense avec de multiples embranchements et carrefours.
- **Niveau 5 - Terrains Variés & Pondérés** : Même topologie que le niveau 4, mais intégrant **8 cases de terrain lourd** (coût 4 à 10) placées sur le chemin le plus court, forçant A\* à arbitrer entre traversée coûteuse et contournement.
- **Niveau 6 - Pièges à Glouton et Faux Raccourci** : Conçu pour tromper l'heuristique :
  - Trois coupes en U emboîtées, ouvertes vers le départ, attirent la recherche dans des culs-de-sac.
  - Le portail orange, tout près de la sortie, est enfermé dans une chambre sans issue : l'heuristique promet un raccourci qui n'existe pas.
  - Greedy produit un chemin bien plus coûteux que l'optimum ; A\* reste optimal mais développe presque toute la grille.
- **Niveau 7 - Marais, Rivière et Gué** : Niveau pondéré où plusieurs stratégies se font concurrence :
  - un marais (coût 3) entoure une vase profonde (coût 8) placée sur la diagonale ;
  - une route pavée (coût 1) serpente à travers le marais ;
  - une rivière ne se franchit que par un gué (coût 9) ou par deux ponts éloignés (coût 1).
  - Greedy traverse la vase par le portail (coût 208 pour 89 pas) ; A\* fait plus de pas mais paie deux fois moins (coût 106 pour 106 pas).

### Niveaux d'exercice (6 × 6)

Petits niveaux destinés à vérifier une trace à la main. Ils s'utilisent avec `trace.py` uniquement : l'interface Pygame est fixée à une grille 40 × 68.

- **`level_trace_10`** : Départ `(0, 0)`, sortie `(2, 5)`, une case lourde `(2, 1)` de coût 4. A\* (euclidienne) se résout en **10 itérations** et contourne la case lourde (coût 9, contre 10 en la traversant).
- **`level_trace_portails`** : Départ `(0, 0)`, sortie `(5, 5)`, portails `(0, 2)` ↔ `(4, 5)`, case lourde `(1, 1)` de coût 4.
  - A\* (euclidienne) se résout en **10 itérations** pour un coût de 8 ; il utilise le portail et contourne la case lourde.
  - Greedy traverse la case lourde (coût 9).

---

## Quoi fait quoi 

| Fichier | Rôle & Responsabilité |
| :--- | :--- |
| `ift-2003-tp.py` | **Point d'entrée principal**. Gère la fenêtre Pygame, la boucle d'événements, le dessin de la grille et de la toolbar, les calculs d'heuristiques, ainsi que les algorithmes `algo_1` (Greedy) et `algo_AStar`. |
| `level_1.py` | Générateur du **Niveau 1** (labyrinthe arborescent DFS déterministe avec portails). |
| `level_2.py` | Générateur du **Niveau 2** (salles géométriques, couloirs et téléporteurs). |
| `level_3.py` | Générateur du **Niveau 3** (murs horizontaux et chicanes régulières). |
| `level_4.py` | Générateur du **Niveau 4** (dédale haute densité avec carrefours stratégiques). |
| `level_5.py` | Générateur du **Niveau 5** (dédale haute densité avec définition des cases pondérées `HEAVYCOST_TILES`). |
| `level_6.py` | Générateur du **Niveau 6** (coupes en U, faux raccourci par portail et chicane). |
| `level_7.py` | Générateur du **Niveau 7** (marais, vase, route pavée, rivière, gué et ponts). |
| `level_trace_10.py` | Niveau d'exercice 6 × 6 sans portail (trace A\* en 10 itérations). |
| `level_trace_portails.py` | Niveau d'exercice 6 × 6 avec portails (trace A\* en 10 itérations). |
| `trace.py` | Outil en ligne de commande qui génère la **trace pas à pas** d'A\* ou de Greedy sur un niveau. |
| `test_dijkstra.py` | Fichier de tests unitaires (`unittest`) validant le comportement de recherche de chemin sur des grilles réduites. |
| `requirements.txt` | Liste des dépendances requises pour l'environnement Python (`pygame-ce`). |
| `install.bat` | Script batch pour automatiser la mise à jour de `pip` et l'installation sous Windows (CMD). |
| `install.ps1` | Script PowerShell pour automatiser l'installation des dépendances sous Windows. |
| `install.sh` | Script Shell pour automatiser l'installation des dépendances sous Linux et macOS. |
| `README.md` | Guide utilisateur complet et documentation technique du projet. |



---

