import heapq
import math
import time
import pygame

import level_1
import level_2
import level_3
import level_4
import level_5

ROWS = 40
COLUMNS = 68
TOOLBAR_HEIGHT = 100
MARGIN = 80
# Est nécessaire pour connaitre les dimensions de l'écran 
pygame.init()

# La dimension des cases se fait selon la taille de l'affichage
_info = pygame.display.Info()
SQUARE_SIZE = max(8, min(
    (_info.current_w - 20) // COLUMNS,
    (_info.current_h - TOOLBAR_HEIGHT - MARGIN) // ROWS,
))

GRID_WIDTH = COLUMNS * SQUARE_SIZE
GRID_HEIGHT = ROWS * SQUARE_SIZE
WIDTH = GRID_WIDTH
HEIGHT = GRID_HEIGHT + TOOLBAR_HEIGHT
DEFAULT_COST = 1

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
HIGHCOST_TILE_COLOR = pygame.Color(150, 110, 60)  
TOOLBAR_BG = pygame.Color(230, 235, 240)
TOOLBAR_BORDER = pygame.Color(180, 185, 195)
BTN_BG = pygame.Color(210, 215, 225)
BTN_ACTIVE = pygame.Color(45, 115, 215)
BTN_RUN = pygame.Color(40, 160, 80)
BTN_CLEAR = pygame.Color(210, 70, 70)
TEXT_COLOR = pygame.Color(30, 30, 30)
TEXT_WHITE = pygame.Color(255, 255, 255)
STAT_CARD_BG = pygame.Color(245, 248, 252)
STAT_CARD_BORDER = pygame.Color(195, 205, 220)
STAT_LABEL_COLOR = pygame.Color(90, 105, 125)
STAT_VAL_COLOR = pygame.Color(20, 35, 60)
STAT_VAL_SUCCESS = pygame.Color(30, 130, 60)
STAT_VAL_WARN = pygame.Color(190, 60, 60)

START = (0, 0)
EXIT = (ROWS - 1, COLUMNS - 1)


#  Fait par nous - somme des diférences absolues de chaque coordonée
def manhattan_distance(cell1: tuple[int, int], cell2: tuple[int, int]) -> int:
    row1, column1 = cell1
    row2, column2 = cell2
    return abs(row1 - row2) + abs(column1 - column2)

#  Fait par nous - distance en ligne droite entre deux points
def euclidean_distance(cell1: tuple[int, int], cell2: tuple[int, int]) -> float:
    row1, column1 = cell1
    row2, column2 = cell2

    return math.sqrt(
        (row1 - row2) ** 2
        + (column1 - column2) ** 2
    )

#   Fait par nous - détermine les cases voisines accessibles
def next_move_possible(
    current: tuple[int, int],
    walls: set[tuple[int, int]],
    portals: tuple[tuple[int, int], tuple[int, int]] | None = None,
) -> list[tuple[int, int]]:
    row, column = current
    moves_possible = []

    # Les voisins sont bas, haut, gauche, droite. Pas de déplacement en diagonale
    neighbors = [
        (row - 1, column),
        (row + 1, column),
        (row, column - 1),
        (row, column + 1),
    ]

    # Téléportation par portails si la case courante est un portail actif
    if portals:
        # portals est composé de deux cases permettant la téléportation entre les deux (bidirectionnel)
        p1, p2 = portals
        # si la case active est un portail, la case d'arrivée devient un voisin
        if current == p1 and p2 not in walls and p2 not in neighbors:
            neighbors.append(p2)
        elif current == p2 and p1 not in walls and p1 not in neighbors:
            neighbors.append(p1)

    for next_cell in neighbors:
        next_row, next_col = next_cell

        # Vérifie si c'est un déplacement valide
        is_in_bounds = 0 <= next_row < ROWS and 0 <= next_col < COLUMNS

         # Vérifie si la case est libre
        if is_in_bounds and next_cell not in walls:
            moves_possible.append(next_cell)

    return moves_possible

#   Fait par nous - calcul le cout du déplacement pour entrer dans la cellule
def tile_move_cost(
    cell: tuple[int, int],
    costs: dict[tuple[int, int], int] | None = None
    ) -> int:
    if costs:
        # le dictionnaire costs contient une case et un cout
        return costs.get(cell,DEFAULT_COST)
    else:
        return DEFAULT_COST



#   Fait par nous
#   Algorithme 1 : Recherche gloutonne (Greedy Best-First) basée sur la distance de Manhattan.
#   Pas optimal, on ne prend pas en compte les portails s'ils sont à l'opposé, ni les chemins de terre.
#
def algo_1(
    walls: set[tuple[int, int]],
    portals: tuple[tuple[int, int], tuple[int, int]] | None = None,
    costs: dict[tuple[int, int], int] | None = None
) -> tuple[list[tuple[int, int]], dict[str, object]]:

    # Pour le calcul du temps d'exécution
    start_time = time.perf_counter()

    # File contenant la priorité d'exécution selon la distance de manathan
    priority_queue = []
    heapq.heappush(priority_queue, (manhattan_distance(START, EXIT), START))

    # Mémorise le parent de chaque case
    previous = {START: None}
    # Nombre de case développées
    nodes_expanded = 0

    # On itère la file tant qu'il y a une case à traiter
    while priority_queue:
        # La case courante est celle qui est la plus susceptible d'être la meilleure
        _, current = heapq.heappop(priority_queue)
        nodes_expanded += 1

        # Atteinte de la case finale
        if current == EXIT:
            path = []
            # Reconstruction du chemin
            while current is not None:
                path.append(current)
                current = previous[current]
            path = list(reversed(path))
            path_without_start = path[1:]
            # Calcul du cout en faisant la somme des couts des cases parcourues
            total_cost = sum(tile_move_cost(tile, costs) for tile in path_without_start)
            exec_time_ms = (time.perf_counter() - start_time) * 1000
            # Le nombre de déplacements
            depth = len(path) - 1
            stats = {
                "nodes_expanded": nodes_expanded,
                "depth": depth,
                "cost": total_cost,
                "execution_time_ms": exec_time_ms,
            }
            return path, stats

        # On développe les voisins (cases accessibles)
        for next_cell in next_move_possible(current, walls, portals):
            if next_cell not in previous:
                previous[next_cell] = current
                priority = manhattan_distance(next_cell, EXIT)
                heapq.heappush(priority_queue, (priority, next_cell))

    # Temps d'exécution
    exec_time_ms = (time.perf_counter() - start_time) * 1000
    stats = {
        "nodes_expanded": nodes_expanded,
        "depth": 0,
        "cost": float("inf"),
        "execution_time_ms": exec_time_ms,
    }
    return [], stats




# Fait par nous
# Algorithme 2 : A* utilisant la distance euclidienne.
def algo_AStar(
    walls: set[tuple[int, int]],
    portals: tuple[tuple[int, int], tuple[int, int]] | None = None,
    costs: dict[tuple[int, int], int] | None = None
) -> tuple[list[tuple[int, int]], dict[str, object]]:
    
    start_time = time.perf_counter()

    # Priorité selon le coût réel + distance euclidienne
    priority_queue = []
    
    # Calcul de la distance en ligne droite entre la case initiale et la case finale
    start_h = euclidean_distance(START, EXIT)
    heapq.heappush(priority_queue, (start_h, 0, START))

    # Contient le parent de la case du meilleur chemin connu
    previous = {START: None}
    # Contient le meilleur coût réel pour ce rendre à cette case
    square_cost = {START: 0}

    nodes_expanded = 0

    # On itère tant qu'il y a des cases à traiter
    while priority_queue:
        # La case courante est celle qui est la plus susceptible d'être la meilleure
        _, current_cost, current = heapq.heappop(priority_queue)

        # Si le cout ne correpond pas au meilleur cout pour ce rendre à cette case, on ignore la case
        if current_cost != square_cost.get(current, float("inf")):
            continue

        nodes_expanded += 1

        if current == EXIT:
            path = []
            cell = current

            # Reconstruction du chemin
            while cell is not None:
                path.append(cell)
                cell = previous[cell]

            path.reverse()
            # Temps d'exécution
            exec_time_ms = (time.perf_counter() - start_time) * 1000
            # Nombre de déplacement
            depth = len(path) - 1

            stats = {
                "nodes_expanded": nodes_expanded,
                "depth": depth,
                "cost": current_cost,
                "execution_time_ms": exec_time_ms,
            }

            return path, stats

        # Exploration des voisins
        for next_cell in next_move_possible(current, walls, portals):

            # Cout pour rejoindre le voisin
            new_cost = current_cost + tile_move_cost(next_cell, costs)

            # Meilleur coût pour ce voisin  (pour l'instant)
            old_cost = square_cost.get(next_cell, float("inf"))

            # Garder uniquement les routes plus économiques
            if new_cost < old_cost:
                square_cost[next_cell] = new_cost
                previous[next_cell] = current

                # A* : f(n) = g(n) + h(n)
                heuristic = euclidean_distance(next_cell, EXIT)
                priority = new_cost + heuristic

                heapq.heappush(priority_queue, (priority, new_cost, next_cell))

    exec_time_ms = (time.perf_counter() - start_time) * 1000

    stats = {
        "nodes_expanded": nodes_expanded,
        "depth": 0,
        "cost": float("inf"),
        "execution_time_ms": exec_time_ms,
    }

    return [], stats


# ==========================================
# Définitions des 5 niveaux pré-faits
# ==========================================
def get_preset_levels() -> dict[int, dict[str, object]]:
    modules = {1: level_1, 2: level_2, 3: level_3, 4: level_4, 5: level_5}
    levels = {}

    for num, mod in modules.items():
        walls = set(mod.get_walls())
        portals = mod.get_portals() if hasattr(mod, "get_portals") else None
        costs = mod.get_costs()  if hasattr(mod, "get_costs") else {}
        # Sécurité : aucun mur sur START ni EXIT ni les portails
        walls.discard(START)
        walls.discard(EXIT)
        if portals:
            for p in portals:
                walls.discard(p)
        levels[num] = {"walls": walls, "portals": portals, "costs": costs}

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
    costs: dict[tuple[int, int], int] | None = None,
) -> None:
    costs = costs or {}
    path_cells = set(path)
    portal_1 = portals[0] if portals else None
    portal_2 = portals[1] if portals else None

    for row in range(ROWS):
        for column in range(COLUMNS):
            cell = (row, column)
            color = GRAY if cell in walls else WHITE
            if cell in costs:
                color = HIGHCOST_TILE_COLOR
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
    buttons.append(Button(pygame.Rect(95, GRID_HEIGHT + 10, 125, 34), "Greedy Best-First", "algo_1"))
    buttons.append(Button(pygame.Rect(228, GRID_HEIGHT + 10, 125, 34), "A*", "algo_2"))

    # Actions Lancer / Effacer
    buttons.append(Button(pygame.Rect(405, GRID_HEIGHT + 10, 105, 34), "Lancer", "run", bg_color=BTN_RUN, active_color=BTN_RUN))
    buttons.append(Button(pygame.Rect(520, GRID_HEIGHT + 10, 105, 34), "Effacer", "clear", bg_color=BTN_CLEAR, active_color=BTN_CLEAR))

    # Ligne 2 : Niveaux
    btn_w = 80
    start_x = 95
    spacing = 10
    for i in range(1, 6):
        buttons.append(Button(pygame.Rect(start_x + (i - 1) * (btn_w + spacing), GRID_HEIGHT + 54, btn_w, 34), f"Niv.{i}", f"level_{i}"))

    return buttons

# Fait par IA
def draw_toolbar(
    screen: pygame.Surface,
    font: pygame.font.Font,
    font_bold: pygame.font.Font,
    font_stat_label: pygame.font.Font,
    font_stat_val: pygame.font.Font,
    buttons: list[Button],
    selected_algo: str,
    selected_level: int | None,
    stats: dict[str, object] | None,
) -> None:
    # Fond de la toolbar
    toolbar_rect = pygame.Rect(0, GRID_HEIGHT, WIDTH, TOOLBAR_HEIGHT)
    pygame.draw.rect(screen, TOOLBAR_BG, toolbar_rect)
    pygame.draw.line(screen, TOOLBAR_BORDER, (0, GRID_HEIGHT), (WIDTH, GRID_HEIGHT), 2)

    # Libellés
    label_algo = font_bold.render("Algorithme :", True, TEXT_COLOR)
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

    # Séparateur vertical vers la section statistiques
    pygame.draw.line(screen, TOOLBAR_BORDER, (650, GRID_HEIGHT + 10), (650, GRID_HEIGHT + TOOLBAR_HEIGHT - 10), 1)

    # Configuration des 4 cartes de statistiques
    cards_config = [
        ("NŒUDS DÉVELOPPÉS", 670, 200),
        ("PROFONDEUR (PAS)", 885, 190),
        ("TEMPS D'EXÉCUTION", 1090, 205),
        ("COÛT TOTAL (QUALITÉ)", 1310, 215),
    ]

    has_stats = stats is not None
    is_failed = has_stats and stats.get("cost") == float("inf")

    # Formatage des valeurs
    if not has_stats:
        vals = ["-", "-", "-", "-"]
        colors = [STAT_VAL_COLOR] * 4
    elif is_failed:
        nodes = str(stats.get("nodes_expanded", 0))
        depth = "N/A"
        t_ms = stats.get("execution_time_ms", 0.0)
        t_str = f"{t_ms:.2f} ms" if t_ms >= 0.01 else "< 0.01 ms"
        cost = "Infini (Échec)"
        vals = [nodes, depth, t_str, cost]
        colors = [STAT_VAL_COLOR, STAT_VAL_WARN, STAT_VAL_COLOR, STAT_VAL_WARN]
    else:
        nodes = str(stats.get("nodes_expanded", 0))
        depth = str(stats.get("depth", 0))
        t_ms = stats.get("execution_time_ms", 0.0)
        t_str = f"{t_ms:.2f} ms" if t_ms >= 0.01 else "< 0.01 ms"
        cost = str(stats.get("cost", 0))
        vals = [nodes, depth, t_str, cost]
        colors = [STAT_VAL_COLOR, STAT_VAL_COLOR, STAT_VAL_COLOR, STAT_VAL_SUCCESS]

    # Rendu des cartes de statistiques
    for (title, x, w), val_text, val_color in zip(cards_config, vals, colors):
        card_rect = pygame.Rect(x, GRID_HEIGHT + 12, w, 76)
        pygame.draw.rect(screen, STAT_CARD_BG, card_rect, border_radius=6)
        pygame.draw.rect(screen, STAT_CARD_BORDER, card_rect, width=1, border_radius=6)

        lbl_surf = font_stat_label.render(title, True, STAT_LABEL_COLOR)
        screen.blit(lbl_surf, (card_rect.x + 12, card_rect.y + 12))

        val_surf = font_stat_val.render(val_text, True, val_color)
        screen.blit(val_surf, (card_rect.x + 12, card_rect.y + 36))

# Fait par IA et retrevaillé par nous
def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Labyrinth AI - IFT 2003")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("Arial", 13, bold=False)
    font_bold = pygame.font.SysFont("Arial", 13, bold=True)
    font_stat_label = pygame.font.SysFont("Arial", 10, bold=True)
    font_stat_val = pygame.font.SysFont("Arial", 17, bold=True)

    levels = get_preset_levels()
    buttons = create_toolbar_buttons()

    walls: set[tuple[int, int]] = set()
    portals: tuple[tuple[int, int], tuple[int, int]] | None = None
    path: list[tuple[int, int]] = []
    costs: dict[tuple[int, int], int] = {}
    player = START
    selected_algo = "algo_1"
    selected_level: int | None = None
    current_stats: dict[str, object] | None = None
    running = True

    def execute_selected_algo():
        nonlocal path, player, current_stats
        start_time = time.perf_counter()
        if selected_algo == "algo_1":
            result = algo_1(walls, portals, costs)
        else:
            result = algo_AStar(walls, portals, costs)
        exec_time_fallback = (time.perf_counter() - start_time) * 1000

        if isinstance(result, tuple) and len(result) == 2 and isinstance(result[0], list):
            path, current_stats = result
        else:
            path = result if isinstance(result, list) else []
            depth = len(path) - 1 if path else 0
            cost = depth if path else float("inf")
            current_stats = {
                "nodes_expanded": 0,
                "depth": depth,
                "cost": cost,
                "execution_time_ms": exec_time_fallback,
            }
        player = path[-1] if path else START

        # Affichage synthétique des métriques dans la console
        if current_stats:
            algo_name = "Algo 1 (Greedy Best-First)" if selected_algo == "algo_1" else "Algo 2"
            print(f"\n--- Statistiques : {algo_name} ---")
            print(f"• Nœuds développés : {current_stats.get('nodes_expanded', 0)}")
            print(f"• Profondeur de la solution : {current_stats.get('depth', 0)}")
            print(f"• Temps d'exécution : {current_stats.get('execution_time_ms', 0.0):.3f} ms")
            cost_val = current_stats.get('cost', 0)
            cost_str = f"{cost_val}" if cost_val != float("inf") else "Infini (Aucun chemin)"
            print(f"• Qualité de la solution (Coût total) : {cost_str}")

    def load_level(lvl_num: int):
        nonlocal walls, portals, costs, path, player, selected_level, current_stats
        selected_level = lvl_num
        lvl_data = levels[lvl_num]
        walls = set(lvl_data["walls"])
        portals = lvl_data["portals"]
        costs = dict(lvl_data["costs"])
        path = []
        player = START
        current_stats = None

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
                    costs = {}
                    path = []
                    player = START
                    selected_level = None
                    current_stats = None
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
                elif event.key == pygame.K_t:
                    load_level(5)

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
                                costs = None
                                path = []
                                player = START
                                selected_level = None
                                current_stats = None
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
                        current_stats = None

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
                        current_stats = None

        screen.fill(WHITE)
        draw_board(screen, walls, path, player, portals, costs)
        draw_toolbar(screen, font, font_bold, font_stat_label, font_stat_val, buttons, selected_algo, selected_level, current_stats)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
