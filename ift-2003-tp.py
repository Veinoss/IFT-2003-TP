from collections import deque
from time import sleep

import pygame
import heapq
import random


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

def manhattan_distance(cell1: tuple[int, int], cell2: tuple[int, int]) -> int:
    row1, column1 = cell1
    row2, column2 = cell2
    return abs(row1 - row2) + abs(column1 - column2)

def next_move_possible(current: tuple[int, int], walls: set[tuple[int, int]]) -> list[tuple[int, int]]:
    row, column = current
    moves_possible = []

    neighbors = [
        (row - 1, column),
        (row + 1, column),
        (row, column - 1),
        (row, column + 1),
    ]

    for next_cell in neighbors:
        next_row, next_col = next_cell
        is_in_bounds = 0 <= next_row < ROWS and 0 <= next_col < COLUMNS

        if is_in_bounds and next_cell not in walls:
            moves_possible.append(next_cell)

    return moves_possible

""" 
    Fonction fait à la main. Elle utilise la distance de Manhattan pour calculer la priorité des cellules. 
    Va rester à la modifier quand on aura fait les teleporteurs.
"""
def algo_1(walls: set[tuple[int, int]]) -> list[tuple[int, int]]:
    priority_queue = []
    heapq.heappush(priority_queue, (manhattan_distance(START, EXIT), START))
    previous = {START: None}

    while priority_queue:
        _, current = heapq.heappop(priority_queue)

        if current == EXIT:
            path = []
            while current is not None:
                path.append(current)
                current = previous[current]
            return list(reversed(path))

        for next_cell in next_move_possible(current, walls):
            if next_cell not in previous:
                previous[next_cell] = current
                priority = manhattan_distance(next_cell, EXIT)
                heapq.heappush(priority_queue, (priority, next_cell))

    return []

''' Généré par IA'''
def square_from_mouse(position: tuple[int, int]) -> tuple[int, int]:
    x, y = position
    return y // SQUARE_SIZE, x // SQUARE_SIZE


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

    portal: tuple[int, int] = (random.randint(0, ROWS - 1), random.randint(0, COLUMNS - 1))
    if portal[0] == START[0] and portal[1] == START[1]:
        portal = (portal[0]+1, (portal[1] + 1))

    portal2: tuple[int, int] = (random.randint(0, ROWS - 1), random.randint(0, COLUMNS - 1))
    if portal[0] == START[0] and portal[1] == START[1]:
        portal = (portal[0]+1, (portal[1] + 1))
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    path = algo_1(walls)
                    player = path[-1] if path else START
                elif event.key == pygame.K_c:
                    walls.clear()
                    path = []
                    player = START
            else:
                buttons = pygame.mouse.get_pressed()
                if buttons[0]:
                    cell = square_from_mouse(event.pos)
                    if cell not in (START, EXIT, portal, portal2):
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
        pygame.draw.rect(screen, pygame.Color("purple"), (portal[1] * SQUARE_SIZE, portal[0] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        pygame.draw.rect(screen, pygame.Color("indigo"), (portal2[1] * SQUARE_SIZE, portal2[0] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
