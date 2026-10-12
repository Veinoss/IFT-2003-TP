"""Niveau 6 : Pièges à Glouton et Faux Raccourci (Deceptive Traps).

Niveau conçu pour tromper l'heuristique :
- Deux grandes « coupes » en U, ouvertes vers le départ et fermées du côté de la
  sortie. Une recherche guidée uniquement par h(n) s'y engouffre, se heurte au
  fond et doit remonter.
- Un faux raccourci : le portail violet est tout près du départ et le portail
  orange tout près de la sortie, mais la case d'arrivée est enfermée dans une
  chambre qui ne mène qu'à une impasse. L'heuristique avec portails promet
  donc un chemin très court qui n'existe pas.
- Une porte dérobée au fond de la grande coupe (ligne 31, colonne 28) donne sur
  la chicane du bas. Le chemin optimal descend directement vers elle en longeant
  la coupe intérieure. Greedy, attiré vers le coin inférieur droit, longe le haut
  puis la paroi droite du piège et doit revenir sur ses pas le long du fond.

A* reste optimal mais, trompé par le faux raccourci, développe presque toute la
grille ; Greedy produit un chemin nettement plus long que l'optimum.
"""

ROWS = 40
COLUMNS = 68
START = (0, 0)
EXIT = (ROWS - 1, COLUMNS - 1)
PORTAL_1 = (4, 6)
PORTAL_2 = (30, 63)


def _hline(walls, r, c1, c2):
    for c in range(c1, c2 + 1):
        walls.add((r, c))


def _vline(walls, c, r1, r2):
    for r in range(r1, r2 + 1):
        walls.add((r, c))


def get_walls() -> set[tuple[int, int]]:
    """Génère et retourne l'ensemble des coordonnées des murs du Niveau 6."""
    walls: set[tuple[int, int]] = set()

    # Grande coupe extérieure : fond (ligne 31) et paroi droite (colonne 57),
    # ouverte en haut et à gauche, donc vers le départ.
    _hline(walls, 31, 8, 57)
    _vline(walls, 57, 3, 31)
    # Porte dérobée au fond de la coupe : elle « récompense » la descente
    # gloutonne, mais débouche au milieu de la chicane du bas.
    walls.discard((31, 28))

    # Coupe intérieure, emboîtée dans la première
    _hline(walls, 23, 18, 49)
    _vline(walls, 49, 9, 23)

    # Petite coupe au cœur du piège
    _hline(walls, 17, 28, 42)
    _vline(walls, 42, 13, 17)

    # Chambre du portail orange : bordée de murs, seule ouverture en haut,
    # vers une bande verticale qui est elle-même une impasse.
    _hline(walls, 25, 59, 67)
    _hline(walls, 35, 59, 67)
    _vline(walls, 59, 25, 35)
    walls.discard((25, 63))
    # La bande à droite de la grande coupe ne rejoint pas le couloir du haut
    _hline(walls, 3, 58, 67)

    # Chicane du couloir inférieur (entre la grande coupe et le bas de la grille)
    for i, c in enumerate(range(12, 56, 6)):
        if i % 2 == 0:
            _vline(walls, c, 32, 37)  # ouverte en bas
        else:
            _vline(walls, c, 33, 39)  # ouverte en haut

    # Le couloir inférieur ne rejoint la sortie que par la droite de la chicane
    _vline(walls, 58, 32, 36)

    walls.discard(START)
    walls.discard(EXIT)
    walls.discard(PORTAL_1)
    walls.discard(PORTAL_2)
    return walls


def get_portals() -> tuple[tuple[int, int], tuple[int, int]]:
    """Retourne les coordonnées des 2 portails du Niveau 6."""
    return PORTAL_1, PORTAL_2


def get_level() -> tuple[set[tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]]:
    """Retourne à la fois les murs et les portails."""
    return get_walls(), get_portals()
