def get_walls() -> set[tuple[int, int]]:
    """Niveau 1 : Chicanes simples (3 colonnes avec ouvertures)."""
    walls: set[tuple[int, int]] = set()
    for r in range(0, 9):
        walls.add((r, 4))
    for r in range(3, 12):
        walls.add((r, 8))
    for r in range(0, 9):
        walls.add((r, 12))
    return walls
