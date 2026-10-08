"""Niveau 2 : Citadelle des Salles et Couloirs (Rooms and Corridors).

Structure de donjon avec de multiples salles interconnectées par des galeries sinueuses.
Résoluble par chemin direct ou via la téléportation entre les deux salles fortifiées.
"""

import random

ROWS = 40
COLUMNS = 68
START = (0, 0)
EXIT = (ROWS - 1, COLUMNS - 1)
PORTAL_1 = (5, 8)
PORTAL_2 = (33, 60)


def get_walls() -> set[tuple[int, int]]:
    """Génère et retourne l'ensemble des coordonnées des murs du Niveau 2."""
    random.seed(222)
    walls = set((r, c) for r in range(ROWS) for c in range(COLUMNS))
    rooms = [
        (2, 2, 8, 12),
        (2, 22, 9, 34),
        (2, 46, 8, 62),
        (14, 4, 23, 16),
        (14, 26, 24, 42),
        (14, 50, 24, 62),
        (28, 2, 36, 14),
        (28, 22, 36, 36),
        (28, 46, 37, 65),
    ]
    for r1, c1, r2, c2 in rooms:
        for r in range(r1, r2 + 1):
            for c in range(c1, c2 + 1):
                walls.discard((r, c))

    def carve_h(r, c1, c2, width=2):
        for c in range(min(c1, c2), max(c1, c2) + 1):
            for w in range(width):
                if r + w < ROWS:
                    walls.discard((r + w, c))

    def carve_v(c, r1, r2, width=2):
        for r in range(min(r1, r2), max(r1, r2) + 1):
            for w in range(width):
                if c + w < COLUMNS:
                    walls.discard((r, c + w))

    carve_h(0, 0, 5)
    carve_v(5, 0, 4)
    carve_h(5, 12, 22)
    carve_h(5, 34, 46)
    carve_v(10, 8, 14)
    carve_v(30, 9, 14)
    carve_v(56, 8, 14)
    carve_h(18, 16, 26)
    carve_h(18, 42, 50)
    carve_v(8, 23, 28)
    carve_v(30, 24, 28)
    carve_v(56, 24, 28)
    carve_h(32, 14, 22)
    carve_h(32, 36, 46)
    carve_h(38, 62, 67)
    carve_v(67, 36, 39)

    for r in range(4, 7):
        for c in range(5, 9):
            walls.add((r, c))
    for r in range(16, 21):
        for c in range(30, 38):
            if (r + c) % 2 == 0:
                walls.add((r, c))
    for r in range(30, 34):
        for c in range(50, 58):
            if c % 3 != 0:
                walls.add((r, c))

    walls.discard(START)
    walls.discard(EXIT)
    walls.discard(PORTAL_1)
    walls.discard(PORTAL_2)
    return walls


def get_portals() -> tuple[tuple[int, int], tuple[int, int]]:
    """Retourne les coordonnées des 2 portails du Niveau 2."""
    return PORTAL_1, PORTAL_2


def get_level() -> tuple[set[tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]]:
    """Retourne à la fois les murs et les portails."""
    return get_walls(), get_portals()
