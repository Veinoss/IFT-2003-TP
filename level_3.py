def get_walls() -> set[tuple[int, int]]:
    """Niveau 3 : Labyrinthe à chemins multiples et carrefours."""
    walls: set[tuple[int, int]] = set()
    for c in range(1, 15):
        if c not in (4, 11):
            walls.add((2, c))
            walls.add((9, c))
    for r in range(3, 9):
        walls.add((r, 3))
        walls.add((r, 7))
        walls.add((r, 12))
    # Passages ouverts
    walls.discard((5, 3))
    walls.discard((6, 7))
    walls.discard((4, 12))
    return walls
