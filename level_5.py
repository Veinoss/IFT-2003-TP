"""Niveau 5 : Grand Dédale à Terrains Variés (Weighted Intricate Labyrinth).

Labyrinthe haute densité avec chemins sinueux, impasses complexes et multiples carrefours.
Résoluble par parcours complet ou via les portails positionnés aux carrefours clés.
Huit cases lourdes ont un coût de déplacement supérieur.
"""

import random

ROWS = 40
COLUMNS = 68
START = (0, 0)
EXIT = (ROWS - 1, COLUMNS - 1)
PORTAL_1 = (12, 14)
PORTAL_2 = (30, 52)

# Cases lourdes : {(ligne, colonne): coût}
# Placées sur le chemin le plus court (sans coûts) pour forcer A* à arbitrer
# entre traverser une case chère ou faire un détour.
HEAVYCOST_TILES = {
    (4, 4): 5,
    (9, 6): 8,
    (12, 9): 6,
    (15, 13): 10,
    (28, 55): 7,
    (26, 61): 5,
    (32, 61): 6,
    (37, 64): 4,
}


def get_walls() -> set[tuple[int, int]]:
    """Génère et retourne l'ensemble des coordonnées des murs du Niveau 5."""
    random.seed(444)
    walls = set((r, c) for r in range(ROWS) for c in range(COLUMNS))
    passages = set([(0, 0)])
    walls.discard((0, 0))
    stack = [(0, 0)]

    while stack:
        cr, cc = stack[-1]
        nbrs = []
        for dr, dc in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
            nr, nc = cr + dr, cc + dc
            if 0 <= nr < ROWS and 0 <= nc < COLUMNS and (nr, nc) not in passages:
                nbrs.append((nr, nc, cr + dr // 2, cc + dc // 2))
        if nbrs:
            nr, nc, wr, wc = random.choice(nbrs)
            passages.add((nr, nc))
            passages.add((wr, wc))
            walls.discard((nr, nc))
            walls.discard((wr, wc))
            stack.append((nr, nc))
        else:
            stack.pop()

    for w in list(walls):
        wr, wc = w
        if 1 <= wr < ROWS - 1 and 1 <= wc < COLUMNS - 1:
            if random.random() < 0.18:
                if ((wr - 1, wc) not in walls and (wr + 1, wc) not in walls) or (
                    (wr, wc - 1) not in walls and (wr, wc + 1) not in walls
                ):
                    walls.discard(w)

    walls.discard(START)
    walls.discard(EXIT)
    walls.discard((ROWS - 1, COLUMNS - 2))
    walls.discard((ROWS - 2, COLUMNS - 1))
    walls.discard(PORTAL_1)
    walls.discard(PORTAL_2)
    return walls


def get_portals() -> tuple[tuple[int, int], tuple[int, int]]:
    """Retourne les coordonnées des 2 portails du Niveau 5."""
    return PORTAL_1, PORTAL_2


def get_costs(walls: set[tuple[int, int]] | None = None) -> dict[tuple[int, int], int]:
    """Retourne le coût des cases spéciales du Niveau 5.

    Seules les cases de passage (pas les murs) reçoivent un coût.
    Les cases absentes du dictionnaire coûtent 1 par défaut.
    Si les murs sont fournis, on évite de régénérer le labyrinthe.
    """
    if walls is None:
        walls = get_walls()
    protected = {START, EXIT, PORTAL_1, PORTAL_2}

    return {
        cell: cost
        for cell, cost in HEAVYCOST_TILES.items()
        if cell not in walls and cell not in protected
    }


def get_level() -> tuple[
    set[tuple[int, int]],
    tuple[tuple[int, int], tuple[int, int]],
    dict[tuple[int, int], int],
]:
    """Retourne les murs, les portails et les coûts des cases."""
    walls = get_walls()
    return walls, get_portals(), get_costs(walls)