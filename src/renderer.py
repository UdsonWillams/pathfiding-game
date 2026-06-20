import pygame
from .constants import (
    GAME_AREA_WIDTH,
    WINDOW_HEIGHT,
    SIDEBAR_WIDTH,
    CELL_MARGIN,
    GRID_MARGIN_TOP,
    GRID_MARGIN_BOTTOM,
    GRID_MARGIN_LEFT,
    GRID_MARGIN_RIGHT,
    COLOR_BG,
    COLOR_SIDEBAR_BG,
    COLOR_EMPTY,
    COLOR_WALL,
    COLOR_START,
    COLOR_GOAL,
    COLOR_GRASS,
    COLOR_MUD,
    COLOR_WATER,
    COLOR_VISITED,
    COLOR_FRONTIER,
    COLOR_PATH,
    COLOR_PLAYER,
    COLOR_PLAYER_GLOW,
    COLOR_GRID_LINE,
    COLOR_TEXT,
    COLOR_TEXT_DIM,
    COLOR_TEXT_HIGHLIGHT,
    COLOR_G_VAR,
    COLOR_H_VAR,
    COLOR_F_VAR,
    COLOR_BUTTON,
    COLOR_BUTTON_HOVER,
    COLOR_BUTTON_ACTIVE,
    CELL_EMPTY,
    CELL_WALL,
    CELL_START,
    CELL_GOAL,
    CELL_GRASS,
    CELL_MUD,
    CELL_WATER,
)

CELL_COLORS = {
    CELL_EMPTY: COLOR_EMPTY,
    CELL_WALL: COLOR_WALL,
    CELL_START: COLOR_START,
    CELL_GOAL: COLOR_GOAL,
    CELL_GRASS: COLOR_GRASS,
    CELL_MUD: COLOR_MUD,
    CELL_WATER: COLOR_WATER,
}


class Renderer:
    def __init__(self, surface):
        self.surface = surface
        self.font_small = pygame.font.SysFont("consolas", 14)
        self.font_medium = pygame.font.SysFont("consolas", 16)
        self.font_large = pygame.font.SysFont("consolas", 22)
        self.font_title = pygame.font.SysFont("consolas", 28, bold=True)
        self._cell_size = 20

    def draw_background(self):
        self.surface.fill(COLOR_BG)

    def _calculate_layout(self, grid):
        avail_w = GAME_AREA_WIDTH - GRID_MARGIN_LEFT - GRID_MARGIN_RIGHT
        avail_h = WINDOW_HEIGHT - GRID_MARGIN_TOP - GRID_MARGIN_BOTTOM
        cell_w = (avail_w - CELL_MARGIN * (grid.cols + 1)) // grid.cols
        cell_h = (avail_h - CELL_MARGIN * (grid.rows + 1)) // grid.rows
        self._cell_size = max(4, min(cell_w, cell_h))
        grid_pixel_w = grid.cols * (self._cell_size + CELL_MARGIN) + CELL_MARGIN
        grid_pixel_h = grid.rows * (self._cell_size + CELL_MARGIN) + CELL_MARGIN
        self._grid_x = GRID_MARGIN_LEFT + (avail_w - grid_pixel_w) // 2
        self._grid_y = GRID_MARGIN_TOP + (avail_h - grid_pixel_h) // 2

    def cell_to_pixel(self, row, col):
        x = self._grid_x + col * (self._cell_size + CELL_MARGIN) + CELL_MARGIN
        y = self._grid_y + row * (self._cell_size + CELL_MARGIN) + CELL_MARGIN
        return x, y, self._cell_size, self._cell_size

    def pixel_to_cell(self, mx, my):
        if mx < self._grid_x or my < self._grid_y:
            return None
        col = (mx - self._grid_x) // (self._cell_size + CELL_MARGIN)
        row = (my - self._grid_y) // (self._cell_size + CELL_MARGIN)
        return row, col

    def draw_grid(self, grid, highlight_cell=None):
        for r in range(grid.rows):
            for c in range(grid.cols):
                cell = grid.cells[r][c]
                x, y, w, h = self.cell_to_pixel(r, c)

                color = CELL_COLORS.get(cell.cell_type, COLOR_EMPTY)
                if cell.is_path:
                    color = COLOR_PATH
                elif cell.is_frontier:
                    color = COLOR_FRONTIER
                elif cell.visited:
                    color = COLOR_VISITED

                rect = pygame.Rect(x, y, w, h)
                pygame.draw.rect(self.surface, color, rect)

                if w >= 6 and h >= 6:
                    darker = tuple(max(0, c - 40) for c in color)
                    lighter = tuple(min(255, c + 30) for c in color)
                    if w >= 4:
                        pygame.draw.line(self.surface, darker, (x, y + h - 1), (x + w, y + h - 1))
                        pygame.draw.line(self.surface, darker, (x + w - 1, y), (x + w - 1, y + h))
                    if w >= 4:
                        pygame.draw.line(self.surface, lighter, (x, y), (x + w, y))
                        pygame.draw.line(self.surface, lighter, (x, y), (x, y + h))

                pygame.draw.rect(self.surface, COLOR_GRID_LINE, rect, 1)

                if cell.cell_type == CELL_START:
                    self._draw_label("S", x + w // 2, y + h // 2, COLOR_EMPTY)
                elif cell.cell_type == CELL_GOAL:
                    self._draw_label("G", x + w // 2, y + h // 2, COLOR_EMPTY)

        if highlight_cell:
            x, y, w, h = self.cell_to_pixel(*highlight_cell)
            pygame.draw.rect(self.surface, (255, 255, 255), (x, y, w, h), 3)

    def draw_player(self, pos):
        if pos is None:
            return
        x, y, w, h = self.cell_to_pixel(*pos)
        cx, cy = x + w // 2, y + h // 2
        glow_radius = max(w, h) // 2 + 3
        glow_surf = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, COLOR_PLAYER_GLOW, (glow_radius, glow_radius), glow_radius)
        self.surface.blit(glow_surf, (cx - glow_radius, cy - glow_radius))
        radius = max(w, h) // 2 - 2
        pygame.draw.circle(self.surface, COLOR_PLAYER, (cx, cy), radius)

    def draw_sidebar(self, title="", lines=None):
        sidebar_rect = pygame.Rect(GAME_AREA_WIDTH, 0, SIDEBAR_WIDTH, WINDOW_HEIGHT)
        pygame.draw.rect(self.surface, COLOR_SIDEBAR_BG, sidebar_rect)
        pygame.draw.line(
            self.surface,
            (60, 65, 70),
            (GAME_AREA_WIDTH, 0),
            (GAME_AREA_WIDTH, WINDOW_HEIGHT),
            2,
        )

        y = 20
        if title:
            title_surf = self.font_large.render(title, True, (255, 255, 255))
            self.surface.blit(title_surf, (GAME_AREA_WIDTH + 15, y))
            y += 40

        if lines:
            for line_text, color in lines:
                if y > WINDOW_HEIGHT - 30:
                    break
                surf = self.font_small.render(line_text, True, color)
                self.surface.blit(surf, (GAME_AREA_WIDTH + 15, y))
                y += 20

    def draw_rich_sidebar(self, algo_info, stats_texts=None, live_info=None):
        sidebar_x = GAME_AREA_WIDTH
        sidebar_rect = pygame.Rect(sidebar_x, 0, SIDEBAR_WIDTH, WINDOW_HEIGHT)
        pygame.draw.rect(self.surface, COLOR_SIDEBAR_BG, sidebar_rect)
        pygame.draw.line(
            self.surface,
            (60, 65, 70),
            (sidebar_x, 0),
            (sidebar_x, WINDOW_HEIGHT),
            2,
        )

        x = sidebar_x + 15
        y = 15

        title_surf = self.font_large.render(algo_info.name, True, COLOR_TEXT)
        self.surface.blit(title_surf, (x, y))
        y += 35

        for badge_text, badge_color in zip(algo_info.badges, algo_info.badges_colors):
            badge_surf = self.font_small.render(badge_text, True, badge_color)
            self.surface.blit(badge_surf, (x, y))
            y += 18

        y += 8
        pygame.draw.line(self.surface, (70, 75, 80), (x, y), (x + SIDEBAR_WIDTH - 30, y))
        y += 10

        section_surf = self.font_medium.render("Como funciona:", True, COLOR_TEXT)
        self.surface.blit(section_surf, (x, y))
        y += 22

        for line in algo_info.how_it_works:
            if y > WINDOW_HEIGHT - 100:
                break
            y = self._draw_rich_line(line, x, y)

        y += 6
        section_surf = self.font_medium.render("Quando usar:", True, COLOR_TEXT)
        self.surface.blit(section_surf, (x, y))
        y += 22

        for line in algo_info.when_to_use:
            if y > WINDOW_HEIGHT - 12:
                break
            y = self._draw_rich_line(line, x, y, default_color=COLOR_TEXT_DIM)

        if live_info:
            y += 8
            pygame.draw.line(self.surface, (70, 75, 80), (x, y), (x + SIDEBAR_WIDTH - 30, y))
            y += 10
            info_surf = self.font_small.render("Ao vivo:", True, COLOR_TEXT)
            self.surface.blit(info_surf, (x, y))
            y += 20
            for line in live_info:
                if y > WINDOW_HEIGHT - 12:
                    break
                y = self._draw_rich_line(line, x, y, default_color=COLOR_TEXT_DIM)

        if stats_texts:
            y += 8
            pygame.draw.line(self.surface, (70, 75, 80), (x, y), (x + SIDEBAR_WIDTH - 30, y))
            y += 12
            for text, color in stats_texts:
                if y > WINDOW_HEIGHT - 12:
                    break
                stat_surf = self.font_small.render(text, True, color)
                self.surface.blit(stat_surf, (x, y))
                y += 18

    def _draw_rich_line(self, text, x, y, default_color=COLOR_TEXT):
        if not text:
            return y + 18

        max_x = GAME_AREA_WIDTH + SIDEBAR_WIDTH - 15

        words = text.split(" ")
        current_parts = []
        current_x = x
        result_y = y

        for wi, word in enumerate(words):
            word_parts = self._tokenize_word(word, default_color)
            word_width = sum(
                self.font_small.size(p[0])[0] for p in word_parts
            )

            space_width = self.font_small.size(" ")[0] if wi > 0 else 0

            if current_x + space_width + word_width > max_x and current_parts:
                result_y = self._render_parts(current_parts, x, result_y)
                current_parts = word_parts
                current_x = x + word_width
            else:
                if wi > 0 and current_parts:
                    current_parts.append((" ", default_color))
                    current_x += space_width
                current_parts.extend(word_parts)
                current_x += word_width

        if current_parts:
            result_y = self._render_parts(current_parts, x, result_y)

        return result_y

    def _tokenize_word(self, word, default_color):
        parts = []
        i = 0
        while i < len(word):
            if word[i] == "`":
                end = word.find("`", i + 1)
                if end == -1:
                    parts.append((word[i:], default_color))
                    i = len(word)
                else:
                    token = word[i + 1 : end]
                    if token == "g":
                        parts.append((token, COLOR_G_VAR))
                    elif token == "h":
                        parts.append((token, COLOR_H_VAR))
                    elif token == "f":
                        parts.append((token, COLOR_F_VAR))
                    else:
                        parts.append((token, COLOR_TEXT_HIGHLIGHT))
                    i = end + 1
            else:
                end = word.find("`", i)
                if end == -1:
                    parts.append((word[i:], default_color))
                    i = len(word)
                else:
                    parts.append((word[i:end], default_color))
                    i = end
        return parts

    def _render_parts(self, parts, x, y):
        cx = x
        for part_text, part_color in parts:
            surf = self.font_small.render(part_text, True, part_color)
            self.surface.blit(surf, (cx, y))
            cx += surf.get_width()
        return y + 18

    def _draw_label(self, text, cx, cy, color):
        label = self.font_small.render(text, True, color)
        rect = label.get_rect(center=(cx, cy))
        self.surface.blit(label, rect)

    def draw_text(self, text, x, y, color=COLOR_TEXT, font=None, center=False):
        if font is None:
            font = self.font_medium
        surf = font.render(text, True, color)
        if center:
            rect = surf.get_rect(center=(x, y))
        else:
            rect = surf.get_rect(topleft=(x, y))
        self.surface.blit(surf, rect)
        return surf.get_height()

    def draw_button(self, rect, text, active=False, hover=False):
        color = COLOR_BUTTON_ACTIVE if active else (COLOR_BUTTON_HOVER if hover else COLOR_BUTTON)
        pygame.draw.rect(self.surface, color, rect, border_radius=4)
        label = self.font_medium.render(text, True, COLOR_TEXT)
        label_rect = label.get_rect(center=rect.center)
        self.surface.blit(label, label_rect)

    def draw_bottom_bar(self, algorithm_names, current_algo, playing, steps_per_frame):
        bar_y = WINDOW_HEIGHT - GRID_MARGIN_BOTTOM + 15
        x = GRID_MARGIN_LEFT

        for i, name in enumerate(algorithm_names):
            btn_rect = pygame.Rect(x, bar_y, 16, 16)
            active = (i == current_algo)
            self.draw_button(btn_rect, str(i + 1), active=active)
            x += 22
            self.draw_text(name, x, bar_y, COLOR_TEXT, self.font_small)
            x += self.font_small.size(name)[0] + 16

        icon = "II" if playing else ">"
        btn_rect = pygame.Rect(x, bar_y, 40, 20)
        self.draw_button(btn_rect, icon)
        x += 50

        self.draw_text(f"Vel: {steps_per_frame}", x, bar_y + 2, COLOR_TEXT_DIM, self.font_small)

    def draw_stats(self, nodes_visited, path_cost, elapsed_ms):
        x = GRID_MARGIN_LEFT + 30
        y = 15
        self.draw_text(f"Visitados: {nodes_visited}", x, y, COLOR_TEXT_DIM, self.font_small)
        x += 180
        self.draw_text(f"Custo: {path_cost}", x, y, COLOR_TEXT_DIM, self.font_small)
        x += 150
        self.draw_text(f"Tempo: {elapsed_ms}ms", x, y, COLOR_TEXT_DIM, self.font_small)
