import pygame
from .constants import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    GAME_AREA_WIDTH,
    GRID_MARGIN_BOTTOM,
    GRID_MARGIN_LEFT,
    COLOR_TEXT,
    COLOR_TEXT_DIM,
    COLOR_TEXT_HIGHLIGHT,
    COLOR_BUTTON,
    COLOR_BUTTON_HOVER,
    FPS,
    DEFAULT_STEPS_PER_FRAME,
    MAX_STEPS_PER_FRAME,
    CELL_EMPTY,
    CELL_WALL,
    CELL_START,
    CELL_GOAL,
    CELL_GRASS,
    CELL_MUD,
    CELL_WATER,
)
from .algorithms import BFS, DFS, Dijkstra, AStar, GreedyBestFirst
from .algorithms.info import get_algorithm_info
from .renderer import Renderer
from .ui import UI
from .levels import get_level

ALGORITHMS = [BFS, DFS, Dijkstra, AStar, GreedyBestFirst]

GAME_MENU = "menu"
GAME_LEVEL_SELECT = "level_select"
GAME_VISUALIZER = "visualizer"
GAME_CHALLENGE = "challenge"
GAME_RESULTS = "results"


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Pathfinding Game")
        pygame.key.set_repeat(150, 80)
        self.clock = pygame.time.Clock()
        self.renderer = Renderer(self.screen)
        self.ui = UI(self.screen)
        self.running = True

        self.state = GAME_MENU
        self.previous_state = None

        self.current_algo_idx = 3
        self.playing = False
        self.steps_per_frame = DEFAULT_STEPS_PER_FRAME
        self.algorithm = None
        self._algo_done = False
        self._last_state = None
        self._algo_time = 0
        self.show_comparison = False
        self._comparison_path = None

        self.level_idx = 0
        self._level_cards = []
        self.grid = None
        self.level_name = ""

        self.player_pos = None
        self.player_cost = 0
        self.player_path = None
        self._optimal_cost = None
        self._challenge_start_ticks = 0
        self._challenge_done = False
        self._show_player_path = False
        self._player_path_for_viz = None

        self._score = 0
        self._stars = 0

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            mx, my = pygame.mouse.get_pos()
            self._handle_events(mx, my)

            if self.state == GAME_VISUALIZER:
                self._update_visualizer()

            self._draw(mx, my)
            pygame.display.flip()

    def _handle_events(self, mx, my):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_click(event, mx, my)

    def _handle_keydown(self, event):
        if event.key == pygame.K_ESCAPE:
            if self.state == GAME_VISUALIZER and self._show_player_path:
                self._show_player_path = False
                self._player_path_for_viz = None
                self.state = GAME_RESULTS
            elif self.state in (GAME_VISUALIZER, GAME_CHALLENGE):
                self.state = GAME_LEVEL_SELECT
            elif self.state == GAME_RESULTS:
                self.state = GAME_LEVEL_SELECT
            elif self.state == GAME_LEVEL_SELECT:
                self.state = GAME_MENU
            else:
                self.running = False

        elif self.state == GAME_MENU:
            if event.key == pygame.K_1:
                self.previous_state = "visualizer"
                self.state = GAME_LEVEL_SELECT
            elif event.key == pygame.K_2:
                self.previous_state = "challenge"
                self.state = GAME_LEVEL_SELECT

        elif self.state == GAME_LEVEL_SELECT:
            if event.key == pygame.K_RETURN:
                self._start_level()
            elif event.key == pygame.K_RIGHT:
                self.level_idx = min(9, self.level_idx + 1)
            elif event.key == pygame.K_LEFT:
                self.level_idx = max(0, self.level_idx - 1)
            elif event.key == pygame.K_DOWN:
                next_idx = self._next_diff_group()
                if next_idx is not None:
                    self.level_idx = next_idx
            elif event.key == pygame.K_UP:
                prev_idx = self._prev_diff_group()
                if prev_idx is not None:
                    self.level_idx = prev_idx

        elif self.state == GAME_VISUALIZER:
            if pygame.K_1 <= event.key <= pygame.K_5:
                self.current_algo_idx = event.key - pygame.K_1
                self._reset_visualizer()
            elif event.key == pygame.K_SPACE:
                self.playing = not self.playing
            elif event.key == pygame.K_r:
                self._reset_visualizer()
            elif event.key == pygame.K_LEFT:
                self.steps_per_frame = max(1, self.steps_per_frame - 1)
            elif event.key == pygame.K_RIGHT:
                self.steps_per_frame = min(MAX_STEPS_PER_FRAME, self.steps_per_frame + 1)
            elif event.key == pygame.K_UP:
                self.steps_per_frame = min(MAX_STEPS_PER_FRAME, self.steps_per_frame + 5)
            elif event.key == pygame.K_DOWN:
                self.steps_per_frame = max(1, self.steps_per_frame - 5)
            elif event.key == pygame.K_TAB:
                self._toggle_comparison()
            elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                self._switch_to_challenge_from_visualizer()

        elif self.state == GAME_CHALLENGE:
            if event.key == pygame.K_r:
                self._reset_challenge()
            elif event.key in (pygame.K_w, pygame.K_UP):
                self._move_player(-1, 0)
            elif event.key in (pygame.K_s, pygame.K_DOWN):
                self._move_player(1, 0)
            elif event.key in (pygame.K_a, pygame.K_LEFT):
                self._move_player(0, -1)
            elif event.key in (pygame.K_d, pygame.K_RIGHT):
                self._move_player(0, 1)

        elif self.state == GAME_RESULTS:
            if event.key == pygame.K_r:
                self._retry_level()
            elif event.key == pygame.K_RETURN:
                self.state = GAME_LEVEL_SELECT
            elif event.key == pygame.K_SPACE:
                self._start_post_challenge_viz()

    def _handle_mouse_click(self, event, mx, my):
        left = (event.button == 1)
        right = (event.button == 3)

        if self.state == GAME_MENU and left:
            if hasattr(self, "_menu_rect_visualizer") and self._menu_rect_visualizer.collidepoint(mx, my):
                self.previous_state = "visualizer"
                self.state = GAME_LEVEL_SELECT
            elif hasattr(self, "_menu_rect_challenge") and self._menu_rect_challenge.collidepoint(mx, my):
                self.previous_state = "challenge"
                self.state = GAME_LEVEL_SELECT

        elif self.state == GAME_LEVEL_SELECT:
            for i, rect in enumerate(self._level_cards):
                if rect.collidepoint(mx, my):
                    self.level_idx = i
                    self._start_level()
                    break

        elif self.state == GAME_VISUALIZER:
            if mx >= GAME_AREA_WIDTH:
                return
            if hasattr(self.renderer, "_grid_x"):
                cell = self.renderer.pixel_to_cell(mx, my)
                if cell is None:
                    return
                row, col = cell
                if 0 <= row < self.grid.rows and 0 <= col < self.grid.cols:
                    current = self.grid.cells[row][col].cell_type
                    if current in (CELL_START, CELL_GOAL):
                        return
                    if left:
                        cycle = [CELL_WALL, CELL_GRASS, CELL_MUD, CELL_WATER, CELL_EMPTY]
                        if current in cycle:
                            idx = cycle.index(current)
                            nxt = cycle[(idx + 1) % len(cycle)]
                        else:
                            nxt = CELL_WALL
                    elif right:
                        cycle = [CELL_EMPTY, CELL_WATER, CELL_MUD, CELL_GRASS, CELL_WALL]
                        if current in cycle:
                            idx = cycle.index(current)
                            nxt = cycle[(idx + 1) % len(cycle)]
                        else:
                            nxt = CELL_EMPTY
                    else:
                        return
                    self.grid.set_cell(row, col, nxt)
                    self._reset_visualizer()

        elif self.state == GAME_RESULTS:
            if self.ui.get_clicked_button(mx, my) == 0:
                self._retry_level()
            elif self.ui.get_clicked_button(mx, my) == 1:
                self._start_post_challenge_viz()
            elif self.ui.get_clicked_button(mx, my) == 2:
                self.state = GAME_LEVEL_SELECT

    def _next_diff_group(self):
        current_diff = get_level(self.level_idx)["difficulty"]
        for i in range(self.level_idx + 1, 10):
            if get_level(i)["difficulty"] != current_diff:
                return i
        return None

    def _prev_diff_group(self):
        current_diff = get_level(self.level_idx)["difficulty"]
        for i in range(self.level_idx - 1, -1, -1):
            if get_level(i)["difficulty"] != current_diff:
                return i
        return None

    def _start_level(self):
        level_data = get_level(self.level_idx)
        if level_data is None:
            return
        self.grid = level_data["grid"]
        self.level_name = level_data["name"]
        self._calculate_optimal_cost()

        if self.previous_state == "visualizer":
            self.state = GAME_VISUALIZER
            self._reset_visualizer()
        else:
            self.state = GAME_CHALLENGE
            self._reset_challenge()

    def _switch_to_challenge_from_visualizer(self):
        self.previous_state = "challenge"
        self._calculate_optimal_cost()
        self.state = GAME_CHALLENGE
        self._reset_challenge()

    def _calculate_optimal_cost(self):
        if self.grid.start is None or self.grid.goal is None:
            self._optimal_cost = None
            return
        algo = AStar()
        algo.setup(self.grid, self.grid.start, self.grid.goal)
        while True:
            state = algo.step()
            if state.done:
                break
        self._optimal_cost = algo.calculate_path_cost() if state.path else None

    def _setup_algorithm(self):
        self._algo_done = False
        self._last_state = None
        self._algo_time = pygame.time.get_ticks()
        algo_class = ALGORITHMS[self.current_algo_idx]
        self.algorithm = algo_class()
        self.algorithm.setup(self.grid, self.grid.start, self.grid.goal)

    def _update_visualizer(self):
        if self.playing and not self._algo_done:
            for _ in range(self.steps_per_frame):
                state = self.algorithm.step()
                self._last_state = state
                if state.done:
                    self._algo_done = True
                    self.playing = False
                    self._algo_time = pygame.time.get_ticks() - self._algo_time
                    break

        if self._last_state and self._last_state.path:
            self.grid.update_visual_state(
                visited_positions=self._last_state.visited,
                front=self._last_state.frontier,
                path=self._last_state.path,
            )
        elif self._last_state:
            self.grid.update_visual_state(
                visited_positions=self._last_state.visited,
                front=self._last_state.frontier,
            )

    def _reset_visualizer(self):
        self.playing = False
        self._algo_time = 0
        self.grid.reset_visual_state()
        self.show_comparison = False
        self._comparison_path = None
        self._show_player_path = False
        self._player_path_for_viz = None
        self._setup_algorithm()

    def _toggle_comparison(self):
        self.show_comparison = not self.show_comparison
        if self.show_comparison and self._comparison_path is None:
            self._compute_comparison_path()

    def _compute_comparison_path(self):
        if self.grid.start is None or self.grid.goal is None:
            return
        algo = AStar()
        algo.setup(self.grid, self.grid.start, self.grid.goal)
        while True:
            state = algo.step()
            if state.done:
                break
        self._comparison_path = state.path

    def _reset_challenge(self):
        self.player_pos = self.grid.start
        self.player_cost = 0
        self.player_path = [self.grid.start]
        self._challenge_start_ticks = pygame.time.get_ticks()
        self._challenge_done = False
        self.grid.reset_visual_state()

    def _move_player(self, dr, dc):
        if self._challenge_done or self.player_pos is None:
            return
        r, c = self.player_pos
        nr, nc = r + dr, c + dc
        cell = self.grid.get_cell(nr, nc)
        if cell is None or cell.is_wall:
            return
        self.player_pos = (nr, nc)
        if (nr, nc) not in self.player_path:
            self.player_cost += cell.cost
        self.player_path.append((nr, nc))

        if (nr, nc) == self.grid.goal:
            self._challenge_done = True
            self._compute_results()

    def _compute_results(self):
        elapsed = (pygame.time.get_ticks() - self._challenge_start_ticks) / 1000.0
        if self._optimal_cost and self._optimal_cost > 0:
            efficiency = self._optimal_cost / max(self.player_cost, 1)
            self._score = int(efficiency * 1000)
        else:
            self._score = 500
        time_bonus = max(0, int(100 - elapsed * 2))
        self._score += time_bonus
        self._score = max(0, self._score)

        ratio = self.player_cost / max(self._optimal_cost or 1, 1)
        if ratio <= 1.0:
            self._stars = 3
        elif ratio <= 1.1:
            self._stars = 2
        else:
            self._stars = 1

        self._player_path_for_viz = list(self.player_path) if self.player_path else None
        self.state = GAME_RESULTS

    def _start_post_challenge_viz(self):
        self._show_player_path = True
        self.grid.reset_visual_state()
        self.current_algo_idx = 3
        self._setup_algorithm()
        self.playing = True
        self._algo_done = False
        self._algo_time = pygame.time.get_ticks()
        self.state = GAME_VISUALIZER

    def _retry_level(self):
        level_data = get_level(self.level_idx)
        if level_data is None:
            return
        self.grid = level_data["grid"]
        self.level_name = level_data["name"]
        self._calculate_optimal_cost()

        if self.previous_state == "visualizer":
            self.state = GAME_VISUALIZER
            self._reset_visualizer()
        else:
            self.state = GAME_CHALLENGE
            self._reset_challenge()

    def _draw(self, mx, my):
        self.renderer.draw_background()

        if self.state == GAME_MENU:
            self._draw_menu(mx, my)
        elif self.state == GAME_LEVEL_SELECT:
            self._draw_level_select(mx, my)
        elif self.state == GAME_VISUALIZER:
            self._draw_visualizer(mx, my)
        elif self.state == GAME_CHALLENGE:
            self._draw_challenge(mx, my)
        elif self.state == GAME_RESULTS:
            self._draw_results(mx, my)

    def _draw_menu(self, mx, my):
        self.ui.draw_title("Pathfinding Game", 80)
        self.ui.draw_subtitle("Escolha um modo:", 140)

        btn_w = 500
        btn_h = 70
        btn_x = WINDOW_WIDTH // 2 - btn_w // 2

        y1 = 200
        self._menu_rect_visualizer = pygame.Rect(btn_x, y1, btn_w, btn_h)
        hover1 = self._menu_rect_visualizer.collidepoint(mx, my)
        bg1 = COLOR_BUTTON_HOVER if hover1 else COLOR_BUTTON
        pygame.draw.rect(self.screen, bg1, self._menu_rect_visualizer, border_radius=8)
        pygame.draw.rect(self.screen, (60, 65, 70), self._menu_rect_visualizer, 2, border_radius=8)
        self.ui.draw_text("Visualizador  [1]", btn_x + 20, y1 + 10, COLOR_TEXT, self.ui.font_large)
        self.ui.draw_text(
            "Assista o algoritmo buscar o melhor caminho no mapa.",
            btn_x + 20, y1 + 42, COLOR_TEXT_DIM, self.ui.font_small,
        )

        y2 = 300
        self._menu_rect_challenge = pygame.Rect(btn_x, y2, btn_w, btn_h)
        hover2 = self._menu_rect_challenge.collidepoint(mx, my)
        bg2 = COLOR_BUTTON_HOVER if hover2 else COLOR_BUTTON
        pygame.draw.rect(self.screen, bg2, self._menu_rect_challenge, border_radius=8)
        pygame.draw.rect(self.screen, (60, 65, 70), self._menu_rect_challenge, 2, border_radius=8)
        self.ui.draw_text("Desafio  [2]", btn_x + 20, y2 + 10, COLOR_TEXT, self.ui.font_large)
        self.ui.draw_text(
            "Mova o ponto (WASD/Setas) ate o Goal. Depois veja o algoritmo.",
            btn_x + 20, y2 + 42, COLOR_TEXT_DIM, self.ui.font_small,
        )

        self.ui.draw_text(
            "ESC = Sair",
            WINDOW_WIDTH // 2,
            430,
            COLOR_TEXT_DIM,
            center_x=True,
        )

    def _draw_level_select(self, mx, my):
        mode_label = "Visualizador" if self.previous_state == "visualizer" else "Desafio"
        self.ui.draw_title("Selecionar Fase", 40)
        self.ui.draw_subtitle(f"Modo: {mode_label}", 80)

        cards_per_row = 3
        card_w = 290
        card_h = 80
        spacing_x = 20
        spacing_y = 20
        start_x = 55
        start_y = 140

        self._level_cards = []
        for i in range(10):
            level = get_level(i)
            if level is None:
                continue
            col = i % cards_per_row
            row_idx = i // cards_per_row
            row_start_y = start_y + row_idx * (card_h + spacing_y)

            if row_idx == 3:
                card_x = (WINDOW_WIDTH - card_w) // 2
            else:
                card_x = start_x + col * (card_w + spacing_x)

            rect = pygame.Rect(card_x, row_start_y, card_w, card_h)
            hover = rect.collidepoint(mx, my)
            selected = (i == self.level_idx)

            self.ui.draw_level_card(
                rect, level["name"], level["difficulty"],
                locked=False, hover=hover
            )
            if selected:
                pygame.draw.rect(self.screen, COLOR_TEXT_HIGHLIGHT, rect, 3, border_radius=8)

            self._level_cards.append(rect)

        self.ui.draw_text(
            "ENTER = Iniciar   ESC = Voltar    <- -> = Navegar",
            WINDOW_WIDTH // 2,
            WINDOW_HEIGHT - 30,
            COLOR_TEXT_DIM,
            center_x=True,
        )

    def _draw_visualizer(self, mx, my):
        self.renderer._calculate_layout(self.grid)
        self.ui.draw_text(
            "MODO: Visualizador",
            20, 12, (100, 200, 255), self.ui.font_small,
        )
        self.ui.draw_text(
            "Clique = mudar celula   Direito = desfazer   1-5 = algoritmo   Espaco = rodar",
            20, 32, COLOR_TEXT_DIM, self.ui.font_small,
        )
        self.renderer.draw_grid(self.grid)

        if self.show_comparison and self._comparison_path:
            for pos in self._comparison_path:
                r, c = pos
                cell = self.grid.get_cell(r, c)
                if cell and not cell.is_path:
                    x, y, w, h = self.renderer.cell_to_pixel(r, c)
                    cx, cy = x + w // 2, y + h // 2
                    pygame.draw.circle(
                        self.screen, (255, 255, 100, 120), (cx, cy), max(2, w // 4)
                    )

        if self._show_player_path and self._player_path_for_viz:
            for pos in self._player_path_for_viz:
                r, c = pos
                x, y, w, h = self.renderer.cell_to_pixel(r, c)
                cx, cy = x + w // 2, y + h // 2
                color_surf = pygame.Surface((w, h), pygame.SRCALPHA)
                pygame.draw.circle(
                    color_surf, (255, 140, 50, 100), (w // 2, h // 2), max(2, w // 3)
                )
                self.screen.blit(color_surf, (x, y))

            if self._player_path_for_viz:
                r, c = self._player_path_for_viz[0]
                x, y, w, h = self.renderer.cell_to_pixel(r, c)
                self.renderer._draw_label("Vc", x + w // 2, y + h // 2, (255, 255, 255))
                r, c = self._player_path_for_viz[-1]
                x, y, w, h = self.renderer.cell_to_pixel(r, c)
                self.renderer._draw_label("Vc", x + w // 2, y + h // 2, (255, 255, 255))

        algo_names = [a.name.split(" ")[0] for a in ALGORITHMS]
        self.renderer.draw_bottom_bar(
            algo_names, self.current_algo_idx, self.playing, self.steps_per_frame
        )

        visited = 0
        cost_val = "-"
        elapsed = 0
        if self._last_state:
            visited = len(self._last_state.visited)
            if self._last_state.path:
                cost_val = str(self.algorithm.calculate_path_cost())
            if self._algo_done and self._algo_time:
                elapsed = self._algo_time

        self.renderer.draw_stats(visited, cost_val, elapsed)

        algo_info = get_algorithm_info(self.current_algo_idx)

        live_info = None
        if (
            isinstance(self.algorithm, AStar)
            and self._last_state
            and self._last_state.current
            and not self._last_state.done
        ):
            cur = self._last_state.current
            g_val = self.algorithm._g_score.get(cur, "?")
            h_val = self.algorithm._heuristic(cur, self.grid.goal) if self.grid.goal else "?"
            f_val = self.algorithm._f_score.get(cur, "?")
            live_info = [
                f"Celula atual: ({cur[0]}, {cur[1]})",
                f"`g` = {g_val}  (custo ja gasto)",
                f"`h` = {h_val}  (estimativa ate o goal)",
                f"`f` = {f_val}  (`g` + `h`)",
            ]

        stats_texts = [
            (f"Nos visitados: {visited}", COLOR_TEXT_DIM),
            (f"Custo do caminho: {cost_val}", COLOR_TEXT_DIM),
            (f"Tempo: {elapsed}ms", COLOR_TEXT_DIM),
        ]
        if self._show_player_path:
            stats_texts.append(
                (f"Seu custo: {self.player_cost}", COLOR_TEXT_HIGHLIGHT)
            )
            comp = (
                "Igual ao otimo!"
                if (self._optimal_cost and self.player_cost <= self._optimal_cost)
                else "Diferente do otimo"
            )
            stats_texts.append((comp, COLOR_TEXT_HIGHLIGHT))
        if self.show_comparison and self._comparison_path:
            opt_cost = self._optimal_cost or "?"
            stats_texts.append((f"Custo otimo (A*): {opt_cost}", COLOR_TEXT_HIGHLIGHT))
        stats_texts += [
            ("", COLOR_TEXT),
            ("Cores das celulas:", COLOR_TEXT_DIM),
            ("Vazio  Parede  Grama  Lama  Agua", COLOR_TEXT_DIM),
            ("Inicio(S)  Goal(G)", COLOR_TEXT_DIM),
            ("Azul = fronteira   Cinza = visitado", COLOR_TEXT_DIM),
            ("Amarelo = caminho encontrado", COLOR_TEXT_DIM),
            ("", COLOR_TEXT),
            ("ESC = Niveis   R = Reset", COLOR_TEXT_DIM),
            ("Espaco = Play/Pause", COLOR_TEXT_DIM),
            ("<- -> = Velocidade", COLOR_TEXT_DIM),
            ("TAB = Comparar A*", COLOR_TEXT_DIM),
            ("Clique = mudar celula", COLOR_TEXT_DIM),
            ("Dir. = voltar/desfazer", COLOR_TEXT_DIM),
        ]
        if algo_info:
            self.renderer.draw_rich_sidebar(algo_info, stats_texts, live_info)
        else:
            self.renderer.draw_sidebar("Algoritmo", stats_texts)

    def _draw_challenge(self, mx, my):
        self.renderer._calculate_layout(self.grid)
        self.ui.draw_text(
            "MODO: Desafio",
            20, 12, (255, 180, 60), self.ui.font_small,
        )
        self.ui.draw_text(
            "WASD/Setas = mover player ate o Goal (G)",
            20, 32, COLOR_TEXT_DIM, self.ui.font_small,
        )
        self.renderer.draw_grid(self.grid)
        self.renderer.draw_player(self.player_pos)

        bar_y = WINDOW_HEIGHT - GRID_MARGIN_BOTTOM + 20
        self.ui.draw_text(
            "Modo Desafio - WASD/Setas para mover",
            GRID_MARGIN_LEFT,
            bar_y,
            COLOR_TEXT_DIM,
        )

        self.renderer.draw_stats(0, str(self.player_cost), 0)

        sidebar_lines = [
            ("Modo Desafio", COLOR_TEXT),
            ("", COLOR_TEXT),
            (f"Custo acumulado: {self.player_cost}", COLOR_TEXT_DIM),
            ("", COLOR_TEXT),
            ("WASD/Setas = Mover", COLOR_TEXT_DIM),
            ("R = Reiniciar", COLOR_TEXT_DIM),
            ("ESC = Niveis", COLOR_TEXT_DIM),
            ("", COLOR_TEXT),
            ("Chegue ao Goal (G)", COLOR_TEXT_DIM),
            ("com o menor custo!", COLOR_TEXT_DIM),
            ("", COLOR_TEXT),
            ("Cores do terreno:", COLOR_TEXT_DIM),
            ("Vazio = custo 1", COLOR_TEXT_DIM),
            ("Grama = custo 2", COLOR_TEXT_DIM),
            ("Lama = custo 3", COLOR_TEXT_DIM),
            ("Agua = custo 5", COLOR_TEXT_DIM),
        ]
        self.renderer.draw_sidebar("Desafio", sidebar_lines)

    def _draw_results(self, mx, my):
        self.ui.draw_title("Resultado!", 120)
        self.ui.draw_subtitle(self.level_name, 170)

        self.ui.draw_stars(WINDOW_WIDTH // 2, 220, self._stars, 48)

        y = 300
        self.ui.draw_text(
            f"Score: {self._score}",
            WINDOW_WIDTH // 2,
            y,
            COLOR_TEXT_HIGHLIGHT,
            self.ui.font_large,
            center_x=True,
        )
        y += 45
        self.ui.draw_text(
            f"Custo do jogador: {self.player_cost}",
            WINDOW_WIDTH // 2,
            y,
            COLOR_TEXT,
            center_x=True,
        )
        y += 30
        opt_text = (
            f"Custo otimo (A*): {self._optimal_cost}"
            if self._optimal_cost
            else "Custo otimo: N/A"
        )
        self.ui.draw_text(
            opt_text, WINDOW_WIDTH // 2, y, COLOR_TEXT_DIM, center_x=True
        )

        btn_w = 240
        btn_h = 50
        total_w = btn_w * 3 + 20
        btn_start_x = WINDOW_WIDTH // 2 - total_w // 2
        self.ui.begin_button_list()
        self.ui.add_button(
            pygame.Rect(btn_start_x, 430, btn_w, btn_h), "Tentar  [R]"
        )
        self.ui.add_button(
            pygame.Rect(btn_start_x + btn_w + 10, 430, btn_w, btn_h),
            "Ver A*  [Espaco]",
        )
        self.ui.add_button(
            pygame.Rect(btn_start_x + btn_w * 2 + 20, 430, btn_w, btn_h),
            "Fases  [ENTER]",
        )
        self.ui.end_button_list(mx, my)

        self.ui.draw_text(
            "R = Tentar   Espaco = Ver Algoritmo   ESC = Fases",
            WINDOW_WIDTH // 2,
            530,
            COLOR_TEXT_DIM,
            center_x=True,
        )
