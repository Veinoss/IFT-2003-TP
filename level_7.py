"""
Généré par IA Générative
Niveau 7 

Niveau pondéré où trois stratégies se font concurrence :
- Traverser le marais en ligne droite : court en nombre de pas, mais chaque
  case de marais coûte 3 et la vase profonde au centre coûte 8.
- Suivre la route pavée (coût 1) qui serpente à travers le marais : beaucoup
  plus de pas, mais beaucoup moins cher.
- Franchir la rivière : le gué direct, sur la diagonale, coûte 9 par case ;
  les ponts nord et sud sont gratuits mais demandent un détour.

Le portail violet est placé au milieu de la vase : l'heuristique le juge
intéressant, mais l'atteindre coûte cher.

Greedy ignore les coûts et fonce à travers le marais. A* doit arbitrer entre
pas et coût, ce qui rend son chemin plus long en pas mais bien moins cher.
"""

ROWS = 40
COLUMNS = 68
START = (0, 0)
EXIT = (ROWS - 1, COLUMNS - 1)
PORTAL_1 = (20, 26)
PORTAL_2 = (12, 52)

SWAMP_COST = 3
MUD_COST = 8
FORD_COST = 9

# Rivière verticale (murs) et ses deux passages
RIVER_COLUMNS = (34, 35)
NORTH_BRIDGE_ROWS = (1, 2)
FORD_ROWS = (22, 23)
SOUTH_BRIDGE_ROWS = (37, 38)


def _swamp_cells() -> set[tuple[int, int]]:
    """Bande de marais en diagonale (rangées 10 à 29)."""
    return {(r, c) for r in range(10, 30) for c in range(COLUMNS)}


def _mud_cells() -> set[tuple[int, int]]:
    """Vase profonde : losange centré sur la diagonale départ-sortie."""
    cells = set()
    for r in range(13, 27):
        center = round(r * (COLUMNS - 1) / (ROWS - 1))
        for c in range(center - 9, center + 10):
            if 0 <= c < COLUMNS:
                cells.add((r, c))
    return cells


def _road_cells() -> set[tuple[int, int]]:
    """Route pavée qui serpente à travers le marais, du nord au sud."""
    road = set()

    def h(r, c1, c2):
        for c in range(min(c1, c2), max(c1, c2) + 1):
            road.add((r, c))

    def v(c, r1, r2):
        for r in range(min(r1, r2), max(r1, r2) + 1):
            road.add((r, c))

    # Côté ouest de la rivière
    v(3, 9, 16)
    h(16, 3, 12)
    v(12, 16, 21)
    h(21, 3, 12)
    v(3, 21, 30)
    # Côté est de la rivière
    v(40, 9, 14)
    h(14, 40, 63)
    v(63, 14, 30)
    return road


def get_walls() -> set[tuple[int, int]]:
    """Génère et retourne l'ensemble des coordonnées des murs du Niveau 7."""
    walls: set[tuple[int, int]] = set()

    # Rivière infranchissable, sauf aux deux ponts et au gué
    for c in RIVER_COLUMNS:
        for r in range(ROWS):
            if r not in NORTH_BRIDGE_ROWS + FORD_ROWS + SOUTH_BRIDGE_ROWS:
                walls.add((r, c))

    # Haies au nord-est : après le pont, il faut redescendre vers le marais
    for r in range(4, 9):
        for c in range(37, 68):
            if c != 40:
                walls.add((r, c))

    # Rochers épars dans la plaine sud-ouest
    for r in range(32, 39, 3):
        for c in range(6, 32, 4):
            walls.add((r, c))
            walls.add((r, c + 1))

    walls.discard(START)
    walls.discard(EXIT)
    walls.discard(PORTAL_1)
    walls.discard(PORTAL_2)
    return walls


def get_portals() -> tuple[tuple[int, int], tuple[int, int]]:
    """Retourne les coordonnées des 2 portails du Niveau 7."""
    return PORTAL_1, PORTAL_2


def get_costs(walls: set[tuple[int, int]] | None = None) -> dict[tuple[int, int], int]:
    """Retourne le coût des cases spéciales du Niveau 7.

    Ordre de priorité : route (coût 1, donc absente du dictionnaire),
    gué, vase, marais. Les murs et cases protégées ne reçoivent aucun coût.
    """
    if walls is None:
        walls = get_walls()
    protected = {START, EXIT, PORTAL_1, PORTAL_2}
    road = _road_cells()
    mud = _mud_cells()

    costs: dict[tuple[int, int], int] = {}
    for cell in _swamp_cells():
        costs[cell] = MUD_COST if cell in mud else SWAMP_COST
    for r in FORD_ROWS:
        for c in RIVER_COLUMNS:
            costs[(r, c)] = FORD_COST

    return {
        cell: cost
        for cell, cost in costs.items()
        if cell not in walls and cell not in protected and cell not in road
    }


def get_level() -> tuple[
    set[tuple[int, int]],
    tuple[tuple[int, int], tuple[int, int]],
    dict[tuple[int, int], int],
]:
    """Retourne les murs, les portails et les coûts des cases."""
    walls = get_walls()
    return walls, get_portals(), get_costs(walls)
