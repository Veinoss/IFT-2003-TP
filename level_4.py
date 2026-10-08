def get_walls() -> set[tuple[int, int]]:
    """Niveau 4 : Labyrinthe complexe avec impasses."""
    walls: set[tuple[int, int]] = set()
    for r in range(1, 11):
        for c in range(1, 15):
            if (r % 2 == 1 and c % 2 == 1) or (r in (3, 7) and c not in (2, 8, 14)):
                walls.add((r, c))
    for r in (1, 5, 9):
        for c in (4, 10):
            walls.add((r, c))
    for r in range(2, 10):
        walls.add((r, 6))
    # Ouvertures pour garantir un chemin navigable sinueux
    walls.discard((5, 6))
    walls.discard((8, 6))
    walls.discard((3, 2))
    walls.discard((7, 8))
    walls.discard((9, 10))
    return walls

