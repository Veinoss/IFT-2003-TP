import heapq
import pygame

import level_1
import level_2
import level_3
import level_4

SQUARE_SIZE = 30
ROWS = 40
COLUMNS = 68
GRID_WIDTH = COLUMNS * SQUARE_SIZE
GRID_HEIGHT = ROWS * SQUARE_SIZE
TOOLBAR_HEIGHT = 100
WIDTH = GRID_WIDTH
HEIGHT = GRID_HEIGHT + TOOLBAR_HEIGHT

# Couleurs
WHITE = pygame.Color("white")
GRAY = pygame.Color("gray")
GRID_LINE = pygame.Color("lightgray")
START_COLOR = pygame.Color("green")
EXIT_COLOR = pygame.Color("red")
PATH_COLOR = pygame.Color("blue")
PLAYER_COLOR = pygame.Color("blue")
PORTAL_1_COLOR = pygame.Color(155, 45, 215)  # Violet
PORTAL_2_COLOR = pygame.Color(245, 130, 32)  # Orange
TOOLBAR_BG = pygame.Color(230, 235, 240)
TOOLBAR_BORDER = pygame.Color(180, 185, 195)
BTN_BG = pygame.Color(210, 215, 225)
BTN_ACTIVE = pygame.Color(45, 115, 215)
BTN_RUN = pygame.Color(40, 160, 80)
BTN_CLEAR = pygame.Color(210, 70, 70)
TEXT_COLOR = pygame.Color(30, 30, 30)
TEXT_WHITE = pygame.Color(255, 255, 255)

START = (0, 0)
EXIT = (ROWS - 1, COLUMNS - 1)


#   Fait par nous
def manhattan_distance(cell1: tuple[int, int], cell2: tuple[int, int]) -> int:
    row1, column1 = cell1
    row2, column2 = cell2
    return abs(row1 - row2) + abs(column1 - column2)


#   Fait par nous
def next_move_possible(
    current: tuple[int, int],
    walls: set[tuple[int, int]],
    portals: tuple[tuple[int, int], tuple[int, int]] | None = None,
) -> list[tuple[int, int]]:
    row, column = current
    moves_possible = []

    neighbors = [
        (row - 1, column),
        (row + 1, column),
        (row, column - 1),
        (row, column + 1),
    ]

    # Téléportation par portails si la case courante est un portail actif
    if portals:
        p1, p2 = portals
        if current == p1 and p2 not in walls and p2 not in neighbors:
            neighbors.append(p2)
        elif current == p2 and p1 not in walls and p1 not in neighbors:
            neighbors.append(p1)

    for next_cell in neighbors:
        next_row, next_col = next_cell
        is_in_bounds = 0 <= next_row < ROWS and 0 <= next_col < COLUMNS

        if is_in_bounds and next_cell not in walls:
            moves_possible.append(next_cell)

    return moves_possible



#   Fait par nous
#   Algorithme 1 : Recherche gloutonne (Greedy Best-First) basée sur la distance de Manhattan.
def algo_1(
    walls: set[tuple[int, int]],
    portals: tuple[tuple[int, int], tuple[int, int]] | None = None,
) -> list[tuple[int, int]]:
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

        for next_cell in next_move_possible(current, walls, portals):
            if next_cell not in previous:
                previous[next_cell] = current
                priority = manhattan_distance(next_cell, EXIT)
                heapq.heappush(priority_queue, (priority, next_cell))

    return []



#   Fait par nous
#   Algorithme 2 : Espace réservé pour votre deuxième algorithme de recherche (ex: A*, BFS, Dijkstra).
def algo_2(
    walls: set[tuple[int, int]],
    portals: tuple[tuple[int, int], tuple[int, int]] | None = None,
) -> list[tuple[int, int]]:
    # TODO: Implémentez votre 2e algorithme ici

    return []


# ==========================================
# Définitions des 4 niveaux pré-faits
# ==========================================
def get_preset_levels() -> dict[int, dict[str, object]]:
    modules = {1: level_1, 2: level_2, 3: level_3, 4: level_4}
    levels = {}

    for num, mod in modules.items():
        walls = set(mod.get_walls())
        portals = mod.get_portals() if hasattr(mod, "get_portals") else None
        # Sécurité : aucun mur sur START ni EXIT ni les portails
        walls.discard(START)
        walls.discard(EXIT)
        if portals:
            for p in portals:
                walls.discard(p)
        levels[num] = {"walls": walls, "portals": portals}

    return levels

# Fait par IA
def square_from_mouse(position: tuple[int, int]) -> tuple[int, int] | None:
    x, y = position
    if y < GRID_HEIGHT:
        return y // SQUARE_SIZE, x // SQUARE_SIZE
    return None

# Fait par IA
def draw_board(
    screen: pygame.Surface,
    walls: set[tuple[int, int]],
    path: list[tuple[int, int]],
    player: tuple[int, int],
    portals: tuple[tuple[int, int], tuple[int, int]] | None = None,
) -> None:
    path_cells = set(path)
    portal_1 = portals[0] if portals else None
    portal_2 = portals[1] if portals else None

    for row in range(ROWS):
        for column in range(COLUMNS):
            cell = (row, column)
            color = GRAY if cell in walls else WHITE
            if cell in path_cells:
                color = PATH_COLOR
            if cell == portal_1:
                color = PORTAL_1_COLOR
            elif cell == portal_2:
                color = PORTAL_2_COLOR
            if cell == START:
                color = START_COLOR
            elif cell == EXIT:
                color = EXIT_COLOR

            rect = pygame.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, GRID_LINE, rect, 1)

            # Effet visuel distinctif pour les portails
            if cell == portal_1:
                center_p = (column * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2)
                pygame.draw.circle(screen, WHITE, center_p, SQUARE_SIZE // 3, 2)
                pygame.draw.circle(screen, WHITE, center_p, SQUARE_SIZE // 6)
            elif cell == portal_2:
                center_p = (column * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2)
                pygame.draw.circle(screen, WHITE, center_p, SQUARE_SIZE // 3, 2)
                pygame.draw.circle(screen, WHITE, center_p, SQUARE_SIZE // 6)

    player_row, player_column = player
    center = (
        player_column * SQUARE_SIZE + SQUARE_SIZE // 2,
        player_row * SQUARE_SIZE + SQUARE_SIZE // 2,
    )
    pygame.draw.circle(screen, PLAYER_COLOR, center, SQUARE_SIZE // 4)

# Fait par IA
class Button:
    def __init__(self, rect: pygame.Rect, text: str, action_id: str, bg_color=BTN_BG, active_color=BTN_ACTIVE):
        self.rect = rect
        self.text = text
        self.action_id = action_id
        self.bg_color = bg_color
        self.active_color = active_color

    def draw(self, screen: pygame.Surface, font: pygame.font.Font, is_active: bool = False):
        color = self.active_color if is_active else self.bg_color
        pygame.draw.rect(screen, color, self.rect, border_radius=5)
        pygame.draw.rect(screen, TOOLBAR_BORDER, self.rect, width=1, border_radius=5)

        txt_color = TEXT_WHITE if is_active else TEXT_COLOR
        txt_surf = font.render(self.text, True, txt_color)
        txt_rect = txt_surf.get_rect(center=self.rect.center)
        screen.blit(txt_surf, txt_rect)

    def is_clicked(self, pos: tuple[int, int]) -> bool:
        return self.rect.collidepoint(pos)

# Fait par IA
def create_toolbar_buttons() -> list[Button]:
    buttons = []
    # Ligne 1 : Choix algorithmes et actions
    # Algorithmes
    buttons.append(Button(pygame.Rect(95, GRID_HEIGHT + 10, 125, 34), "Algo 1 (Greedy)", "algo_1"))
    buttons.append(Button(pygame.Rect(228, GRID_HEIGHT + 10, 125, 34), "Algo 2 (À faire)", "algo_2"))

    # Actions Lancer / Effacer
    buttons.append(Button(pygame.Rect(405, GRID_HEIGHT + 10, 105, 34), "▶ Lancer", "run", bg_color=BTN_RUN, active_color=BTN_RUN))
    buttons.append(Button(pygame.Rect(520, GRID_HEIGHT + 10, 105, 34), "🗑 Effacer", "clear", bg_color=BTN_CLEAR, active_color=BTN_CLEAR))

    # Ligne 2 : Niveaux
    btn_w = 80
    start_x = 95
    spacing = 10
    for i in range(1, 5):
        buttons.append(Button(pygame.Rect(start_x + (i - 1) * (btn_w + spacing), GRID_HEIGHT + 54, btn_w, 34), f"Niv. {i}", f"level_{i}"))

    return buttons

# Fait par IA
def draw_toolbar(
    screen: pygame.Surface,
    font: pygame.font.Font,
    font_bold: pygame.font.Font,
    buttons: list[Button],
    selected_algo: str,
    selected_level: int | None,
) -> None:
    # Fond de la toolbar
    toolbar_rect = pygame.Rect(0, GRID_HEIGHT, WIDTH, TOOLBAR_HEIGHT)
    pygame.draw.rect(screen, TOOLBAR_BG, toolbar_rect)
    pygame.draw.line(screen, TOOLBAR_BORDER, (0, GRID_HEIGHT), (WIDTH, GRID_HEIGHT), 2)

    # Libellés
    label_algo = font_bold.render("Algo :", True, TEXT_COLOR)
    screen.blit(label_algo, (15, GRID_HEIGHT + 18))

    label_levels = font_bold.render("Niveaux :", True, TEXT_COLOR)
    screen.blit(label_levels, (15, GRID_HEIGHT + 62))

    # Dessin des boutons
    for btn in buttons:
        is_active = False
        if btn.action_id == selected_algo:
            is_active = True
        elif selected_level is not None and btn.action_id == f"level_{selected_level}":
            is_active = True

        btn.draw(screen, font, is_active=is_active)

# Fait par IA et retrevaillé par nous
def main() -> None:
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Labyrinth AI - IFT 2003")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("Arial", 13, bold=False)
    font_bold = pygame.font.SysFont("Arial", 13, bold=True)

    levels = get_preset_levels()
    buttons = create_toolbar_buttons()

    walls: set[tuple[int, int]] = set()
    portals: tuple[tuple[int, int], tuple[int, int]] | None = None
    path: list[tuple[int, int]] = []
    player = START
    selected_algo = "algo_1"
    selected_level: int | None = None
    running = True

    def execute_selected_algo():
        nonlocal path, player
        if selected_algo == "algo_1":
            path = algo_1(walls, portals)
        else:
            path = algo_2(walls, portals)
        player = path[-1] if path else START

    def load_level(lvl_num: int):
        nonlocal walls, portals, path, player, selected_level
        selected_level = lvl_num
        lvl_data = levels[lvl_num]
        walls = set(lvl_data["walls"])
        portals = lvl_data["portals"]
        path = []
        player = START

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    execute_selected_algo()
                elif event.key == pygame.K_c:
                    walls.clear()
                    portals = None
                    path = []
                    player = START
                    selected_level = None
                elif event.key in (pygame.K_1, pygame.K_KP1):
                    selected_algo = "algo_1"
                elif event.key in (pygame.K_2, pygame.K_KP2):
                    selected_algo = "algo_2"
                elif event.key == pygame.K_q:
                    load_level(1)
                elif event.key == pygame.K_w:
                    load_level(2)
                elif event.key == pygame.K_e:
                    load_level(3)
                elif event.key == pygame.K_r:
                    load_level(4)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche
                    # Vérifier si on a cliqué sur un bouton de la toolbar
                    button_clicked = False
                    for btn in buttons:
                        if btn.is_clicked(event.pos):
                            button_clicked = True
                            if btn.action_id == "algo_1":
                                selected_algo = "algo_1"
                            elif btn.action_id == "algo_2":
                                selected_algo = "algo_2"
                            elif btn.action_id.startswith("level_"):
                                lvl_num = int(btn.action_id.split("_")[1])
                                load_level(lvl_num)
                            elif btn.action_id == "run":
                                execute_selected_algo()
                            elif btn.action_id == "clear":
                                walls.clear()
                                portals = None
                                path = []
                                player = START
                                selected_level = None
                            break

                    if not button_clicked:
                        cell = square_from_mouse(event.pos)
                        protected_cells = (START, EXIT, *(portals if portals else ()))
                        if cell is not None and cell not in protected_cells:
                            if cell not in walls:
                                walls.add(cell)
                            selected_level = None

                elif event.button == 3:  # Clic droit
                    cell = square_from_mouse(event.pos)
                    if cell is not None and cell in walls:
                        walls.remove(cell)
                        selected_level = None
                        path = []
                        player = START

            elif event.type == pygame.MOUSEMOTION:
                buttons_pressed = pygame.mouse.get_pressed()
                if buttons_pressed[0]:  # Clic gauche glissé
                    cell = square_from_mouse(event.pos)
                    protected_cells = (START, EXIT, *(portals if portals else ()))
                    if cell is not None and cell not in protected_cells:
                        if cell not in walls:
                            walls.add(cell)
                        selected_level = None
                elif buttons_pressed[2]:  # Clic droit glissé
                    cell = square_from_mouse(event.pos)
                    if cell is not None and cell in walls:
                        walls.remove(cell)
                        selected_level = None
                        path = []
                        player = START

        screen.fill(WHITE)
        draw_board(screen, walls, path, player, portals)
        draw_toolbar(screen, font, font_bold, buttons, selected_algo, selected_level)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
