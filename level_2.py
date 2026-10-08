def get_walls() -> set[tuple[int, int]]:
    """Niveau 2 : Serpentin / Zigzag fluide."""
    walls: set[tuple[int, int]] = set()
    for c in range(0, 14):
        walls.add((2, c))
    for c in range(2, 16):
        walls.add((5, c))
    for c in range(0, 14):
        walls.add((8, c))
    for c in range(2, 15):
        walls.add((10, c))
    return walls
