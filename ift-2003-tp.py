from collections import deque

import pygame


SQUARE_SIZE = 40
ROWS = 12
COLUMNS = 16
WIDTH = COLUMNS * SQUARE_SIZE
HEIGHT = ROWS * SQUARE_SIZE

WHITE = pygame.Color("white")
GRAY = pygame.Color("gray")
GRID_LINE = pygame.Color("lightgray")
START_COLOR = pygame.Color("green")
EXIT_COLOR = pygame.Color("red")
PATH_COLOR = pygame.Color("blue")
PLAYER_COLOR = pygame.Color("blue")

START = (0, 0)
EXIT = (ROWS - 1, COLUMNS - 1)


def find_path(walls: set[tuple[int, int]]) -> list[tuple[int, int]]:
    """TODO: Ceci a été généré automatiquement sans l'avoir demandé ;) On refait nos algo de recherche prévue..."""
    queue = deque([START])
    previous = {START: None}

    while queue:
        current = queue.popleft()
        if current == EXIT:
            path = []
            while current is not None:
                path.append(current)
                current = previous[current]
            return list(reversed(path))

        row, column = current
        for next_cell in (
            (row - 1, column),
            (row + 1, column),
            (row, column - 1),
            (row, column + 1),
        ):
            next_row, next_column = next_cell
            is_in_bounds = 0 <= next_row < ROWS and 0 <= next_column < COLUMNS
            if is_in_bounds and next_cell not in walls and next_cell not in previous:
                previous[next_cell] = current
                queue.append(next_cell)

    return []


''' Généré par IA'''
def square_from_mouse(position: tuple[int, int]) -> tuple[int, int]:
    x, y = position
    return y // SQUARE_SIZE, x // SQUARE_SIZE


''' Généré par IA'''
def draw_board(
    screen: pygame.Surface,
    walls: set[tuple[int, int]],
    path: list[tuple[int, int]],
    player: tuple[int, int],
) -> None:
    path_cells = set(path)

    for row in range(ROWS):
        for column in range(COLUMNS):
            cell = (row, column)
            color = GRAY if cell in walls else WHITE
            if cell in path_cells:
                color = PATH_COLOR
            if cell == START:
                color = START_COLOR
            elif cell == EXIT:
                color = EXIT_COLOR

            rect = pygame.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, GRID_LINE, rect, 1)

    player_row, player_column = player
    center = (
        player_column * SQUARE_SIZE + SQUARE_SIZE // 2,
        player_row * SQUARE_SIZE + SQUARE_SIZE // 2,
    )
    pygame.draw.circle(screen, PLAYER_COLOR, center, SQUARE_SIZE // 4)


''' Généré par IA et modifé pour adapter le style d'intéraction avec la souris'''
def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Labyrinth AI")
    clock = pygame.time.Clock()

    walls: set[tuple[int, int]] = set()
    path: list[tuple[int, int]] = []
    player = START
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    path = find_path(walls)
                    player = path[-1] if path else START
                elif event.key == pygame.K_c:
                    walls.clear()
                    path = []
                    player = START
            else:
                buttons = pygame.mouse.get_pressed()
                if buttons[0]:
                    cell = square_from_mouse(event.pos)
                    if cell not in (START, EXIT):
                        if cell not in walls:
                            walls. add(cell)
                elif buttons[2]:
                    cell = square_from_mouse(event.pos)
                    if cell in walls:
                        walls.remove(cell)
                          
                    path = []
                    player = START

        screen.fill(WHITE)
        draw_board(screen, walls, path, player)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
