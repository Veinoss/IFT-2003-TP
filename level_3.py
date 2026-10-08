"""Niveau 3 : Labyrinthe Sectorisé en Chicanes (Concentric / Partitioned Maze).

Dédale structuré en 4 grands secteurs sinueux avec chicanes et rétrécissements.
Résoluble par un long cheminement direct ou par téléportation directe d'un secteur à l'autre.
"""

ROWS = 40
COLUMNS = 68
START = (0, 0)
EXIT = (ROWS - 1, COLUMNS - 1)
PORTAL_1 = (5, 54)
PORTAL_2 = (35, 12)


def get_walls() -> set[tuple[int, int]]:
    """Génère et retourne l'ensemble des coordonnées des murs du Niveau 3."""
    walls: set[tuple[int, int]] = set()

    # Murs séparateurs horizontaux avec ouvertures stratégiques
    for c in range(0, 58):
        walls.add((10, c))
    for c in range(10, 68):
        walls.add((20, c))
    for c in range(0, 58):
        walls.add((30, c))

    # Chicanes et obstacles verticaux dans les différents secteurs
    for c in range(4, 68, 5):
        for r in range(0, 8):
            walls.add((r, c))
    for c in range(2, 68, 5):
        for r in range(3, 10):
            walls.add((r, c))

    for c in range(4, 68, 5):
        for r in range(11, 18):
            walls.add((r, c))
    for c in range(7, 68, 5):
        for r in range(13, 20):
            walls.add((r, c))

    for c in range(4, 68, 5):
        for r in range(21, 28):
            walls.add((r, c))
    for c in range(2, 68, 5):
        for r in range(23, 30):
            walls.add((r, c))

    for c in range(4, 68, 5):
        for r in range(31, 38):
            walls.add((r, c))
    for c in range(7, 68, 5):
        for r in range(33, 40):
            walls.add((r, c))

    walls.discard(START)
    walls.discard(EXIT)
    walls.discard(PORTAL_1)
    walls.discard(PORTAL_2)
    return walls


def get_portals() -> tuple[tuple[int, int], tuple[int, int]]:
    """Retourne les coordonnées des 2 portails du Niveau 3."""
    return PORTAL_1, PORTAL_2


def get_level() -> tuple[set[tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]]:
    """Retourne à la fois les murs et les portails."""
    return get_walls(), get_portals()
