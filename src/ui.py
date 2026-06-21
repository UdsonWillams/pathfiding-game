import math
import pygame
from .constants import (
    WINDOW_WIDTH,
    COLOR_BG,
    COLOR_PANEL_BG,
    COLOR_TEXT,
    COLOR_TEXT_DIM,
    COLOR_TITLE,
    COLOR_STAR_FILLED,
    COLOR_STAR_EMPTY,
    COLOR_BUTTON,
    COLOR_BUTTON_HOVER,
    COLOR_BUTTON_ACTIVE,
    COLOR_BUTTON_DISABLED,
    DIFFICULTY_NAMES,
    DIFFICULTY_COLORS,
)


class UI:
    def __init__(self, surface):
        self.surface = surface
        self.font_small = pygame.font.SysFont("consolas", 14)
        self.font_medium = pygame.font.SysFont("consolas", 18)
        self.font_large = pygame.font.SysFont("consolas", 24)
        self.font_title = pygame.font.SysFont("consolas", 36, bold=True)
        self._buttons = []
        self._hover_idx = -1

    def draw_background(self):
        self.surface.fill(COLOR_BG)

    def draw_title(self, text, y=40):
        surf = self.font_title.render(text, True, COLOR_TITLE)
        rect = surf.get_rect(center=(WINDOW_WIDTH // 2, y))
        self.surface.blit(surf, rect)

    def draw_text(self, text, x, y, color=COLOR_TEXT, font=None, center_x=False):
        if font is None:
            font = self.font_medium
        surf = font.render(text, True, color)
        if center_x:
            rect = surf.get_rect(center=(x, y))
        else:
            rect = surf.get_rect(topleft=(x, y))
        self.surface.blit(surf, rect)
        return rect

    def draw_button(self, rect, text, hover=False, active=False, disabled=False, font=None):
        if font is None:
            font = self.font_medium
        if disabled:
            color = COLOR_BUTTON_DISABLED
        elif active:
            color = COLOR_BUTTON_ACTIVE
        elif hover:
            color = COLOR_BUTTON_HOVER
        else:
            color = COLOR_BUTTON

        pygame.draw.rect(self.surface, color, rect, border_radius=6)
        text_color = COLOR_TEXT_DIM if disabled else COLOR_TEXT
        label = font.render(text, True, text_color)
        label_rect = label.get_rect(center=rect.center)
        self.surface.blit(label, label_rect)
        return rect

    def begin_button_list(self):
        self._buttons = []
        self._hover_idx = -1

    def add_button(self, rect, text="", disabled=False):
        self._buttons.append({"rect": rect, "text": text, "disabled": disabled})

    def end_button_list(self, mx, my):
        self._hover_idx = -1
        for i, btn in enumerate(self._buttons):
            if btn["rect"].collidepoint(mx, my) and not btn["disabled"]:
                self._hover_idx = i
        for i, btn in enumerate(self._buttons):
            hover = (i == self._hover_idx)
            self.draw_button(btn["rect"], btn["text"], hover=hover, disabled=btn["disabled"])
        return self._hover_idx

    def get_clicked_button(self, mx, my):
        for i, btn in enumerate(self._buttons):
            if btn["rect"].collidepoint(mx, my) and not btn["disabled"]:
                return i
        return -1

    def get_hover_button(self, mx, my):
        for i, btn in enumerate(self._buttons):
            if btn["rect"].collidepoint(mx, my) and not btn["disabled"]:
                return i
        return -1

    def draw_subtitle(self, text, y=90):
        self.draw_text(text, WINDOW_WIDTH // 2, y, COLOR_TEXT_DIM, self.font_large, center_x=True)

    def draw_stars(self, cx, y, stars, size=24):
        total_w = 3 * size + 2 * 4
        start_x = cx - total_w // 2
        for i in range(3):
            star_x = start_x + i * (size + 4)
            color = COLOR_STAR_FILLED if i < stars else COLOR_STAR_EMPTY
            self._draw_star_single(star_x, y, size, color)

    def _draw_star_single(self, x, y, size, color):
        points = []
        cx = x + size // 2
        cy = y + size // 2
        outer = size // 2
        inner = size // 4
        for i in range(10):
            angle = i * 36 - 90
            r = outer if i % 2 == 0 else inner
            px = cx + r * math.cos(math.radians(angle))
            py = cy + r * math.sin(math.radians(angle))
            points.append((px, py))
        pygame.draw.polygon(self.surface, color, points)

    def draw_difficulty_label(self, x, y, difficulty):
        name = DIFFICULTY_NAMES.get(difficulty, "?")
        color = DIFFICULTY_COLORS.get(difficulty, COLOR_TEXT)
        self.draw_text(name, x, y, color, self.font_small)

    def draw_level_card(self, rect, level_name, difficulty, locked=False, hover=False):
        if locked:
            bg_color = (35, 40, 48)
            text_color = COLOR_TEXT_DIM
        elif hover:
            bg_color = (55, 62, 75)
            text_color = COLOR_TEXT
        else:
            bg_color = COLOR_PANEL_BG
            text_color = COLOR_TEXT

        pygame.draw.rect(self.surface, bg_color, rect, border_radius=8)
        pygame.draw.rect(self.surface, (60, 65, 70), rect, 2, border_radius=8)

        diff_name = DIFFICULTY_NAMES.get(difficulty, "?")
        diff_color = DIFFICULTY_COLORS.get(difficulty, COLOR_TEXT)

        self.draw_text(level_name, rect.x + 15, rect.y + 12, text_color, self.font_medium)
        self.draw_text(diff_name, rect.x + 15, rect.y + 40, diff_color, self.font_small)

    def draw_panel(self, rect):
        pygame.draw.rect(self.surface, COLOR_PANEL_BG, rect, border_radius=8)
        pygame.draw.rect(self.surface, (60, 65, 70), rect, 2, border_radius=8)
