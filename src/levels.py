from .constants import (
    CELL_EMPTY,
    CELL_WALL,
    CELL_START,
    CELL_GOAL,
    CELL_GRASS,
    CELL_MUD,
    CELL_WATER,
    DIFF_EASY,
    DIFF_MEDIUM,
    DIFF_HARD,
    DIFF_EXTREME,
)
from .grid import Grid


def _fill_rect(grid, row, col, width, height, cell_type):
    for dr in range(height):
        for dc in range(width):
            nr, nc = row + dr, col + dc
            if 0 <= nr < grid.rows and 0 <= nc < grid.cols:
                if grid.cells[nr][nc].cell_type in (CELL_START, CELL_GOAL):
                    continue
                grid.set_cell(nr, nc, cell_type)


def _fill_line(grid, row, col, length, cell_type, vertical=False):
    for i in range(length):
        nr = row + (i if vertical else 0)
        nc = col + (0 if vertical else i)
        if 0 <= nr < grid.rows and 0 <= nc < grid.cols:
            if grid.cells[nr][nc].cell_type in (CELL_START, CELL_GOAL):
                continue
            grid.set_cell(nr, nc, cell_type)


def _h_line(grid, row, col, length, cell_type=CELL_WALL):
    _fill_line(grid, row, col, length, cell_type, vertical=False)


def _v_line(grid, row, col, length, cell_type=CELL_WALL):
    _fill_line(grid, row, col, length, cell_type, vertical=True)


def create_level_1():
    """Easy 1: Primeiro Passo"""
    g = Grid(20, 15)
    g.set_cell(1, 1, CELL_START)
    g.set_cell(18, 13, CELL_GOAL)
    _fill_rect(g, 4, 3, 1, 6, CELL_WALL)
    _fill_rect(g, 8, 0, 10, 1, CELL_WALL)
    _fill_rect(g, 12, 7, 1, 6, CELL_WALL)
    _fill_rect(g, 3, 10, 5, 1, CELL_WALL)
    _fill_rect(g, 13, 9, 3, 2, CELL_GRASS)
    return g


def create_level_2():
    """Easy 2: Colunas Esparsas"""
    g = Grid(20, 15)
    g.set_cell(1, 1, CELL_START)
    g.set_cell(18, 13, CELL_GOAL)
    _fill_rect(g, 3, 2, 1, 5, CELL_WALL)
    _fill_rect(g, 6, 6, 1, 4, CELL_WALL)
    _fill_rect(g, 3, 10, 5, 1, CELL_WALL)
    _fill_rect(g, 10, 2, 1, 6, CELL_WALL)
    _fill_rect(g, 12, 9, 5, 1, CELL_WALL)
    _fill_rect(g, 14, 5, 1, 4, CELL_WALL)
    _fill_rect(g, 8, 10, 3, 2, CELL_GRASS)
    return g


def create_level_3():
    """Easy 3: Duas Salas"""
    g = Grid(20, 15)
    g.set_cell(2, 2, CELL_START)
    g.set_cell(17, 12, CELL_GOAL)
    _fill_rect(g, 0, 5, 1, 20, CELL_WALL)
    _fill_rect(g, 0, 5, 10, 1, CELL_EMPTY)
    _fill_line(g, 9, 5, 6, CELL_EMPTY)
    _h_line(g, 10, 0, 5, CELL_WALL)
    _h_line(g, 10, 11, 4, CELL_WALL)
    _fill_rect(g, 11, 5, 1, 9, CELL_WALL)
    _h_line(g, 11, 5, 6, CELL_EMPTY)
    _h_line(g, 15, 0, 15, CELL_WALL)
    _v_line(g, 15, 7, 5, CELL_EMPTY)
    _fill_rect(g, 12, 7, 3, 2, CELL_GRASS)
    return g


def create_level_4():
    """Medium 4: Labirinto Verde"""
    g = Grid(30, 20)
    g.set_cell(1, 1, CELL_START)
    g.set_cell(28, 18, CELL_GOAL)
    _h_line(g, 4, 0, 15, CELL_WALL)
    _h_line(g, 4, 17, 3, CELL_WALL)
    _h_line(g, 8, 2, 18, CELL_WALL)
    _h_line(g, 12, 0, 14, CELL_WALL)
    _h_line(g, 16, 4, 16, CELL_WALL)
    _h_line(g, 20, 0, 12, CELL_WALL)
    _h_line(g, 20, 15, 5, CELL_WALL)
    _h_line(g, 24, 2, 18, CELL_WALL)
    _v_line(g, 4, 15, 5, CELL_EMPTY)
    _v_line(g, 12, 14, 5, CELL_EMPTY)
    _v_line(g, 20, 12, 5, CELL_EMPTY)
    _fill_rect(g, 13, 6, 3, 3, CELL_GRASS)
    _fill_rect(g, 5, 16, 3, 3, CELL_GRASS)
    _fill_rect(g, 22, 5, 4, 3, CELL_MUD)
    return g


def create_level_5():
    """Medium 5: Atalhos de Lama"""
    g = Grid(30, 20)
    g.set_cell(1, 1, CELL_START)
    g.set_cell(28, 18, CELL_GOAL)
    _h_line(g, 6, 0, 20, CELL_WALL)
    _v_line(g, 6, 10, 8, CELL_EMPTY)
    _h_line(g, 13, 0, 10, CELL_WALL)
    _h_line(g, 13, 12, 8, CELL_WALL)
    _h_line(g, 20, 0, 20, CELL_WALL)
    _v_line(g, 14, 14, 7, CELL_EMPTY)
    _v_line(g, 20, 7, 6, CELL_EMPTY)
    _fill_rect(g, 7, 2, 5, 3, CELL_MUD)
    _fill_rect(g, 14, 15, 6, 3, CELL_GRASS)
    _fill_rect(g, 21, 2, 4, 4, CELL_MUD)
    _fill_rect(g, 9, 12, 4, 3, CELL_MUD)
    return g


def create_level_6():
    """Medium 6: Zig Zag"""
    g = Grid(30, 20)
    g.set_cell(1, 1, CELL_START)
    g.set_cell(28, 18, CELL_GOAL)
    _h_line(g, 3, 2, 16, CELL_WALL)
    _v_line(g, 3, 16, 5, CELL_WALL)
    _h_line(g, 7, 4, 14, CELL_WALL)
    _v_line(g, 7, 4, 5, CELL_WALL)
    _h_line(g, 11, 2, 16, CELL_WALL)
    _v_line(g, 11, 16, 5, CELL_WALL)
    _h_line(g, 15, 4, 14, CELL_WALL)
    _v_line(g, 15, 4, 5, CELL_WALL)
    _h_line(g, 19, 2, 16, CELL_WALL)
    _v_line(g, 19, 16, 5, CELL_WALL)
    _h_line(g, 23, 4, 14, CELL_WALL)
    _fill_rect(g, 4, 3, 3, 2, CELL_GRASS)
    _fill_rect(g, 19, 6, 3, 2, CELL_GRASS)
    _fill_rect(g, 12, 9, 3, 3, CELL_MUD)
    return g


def create_level_7():
    """Hard 7: Aqua Maze"""
    g = Grid(40, 25)
    g.set_cell(1, 1, CELL_START)
    g.set_cell(38, 23, CELL_GOAL)
    _h_line(g, 7, 4, 21, CELL_WALL)
    _h_line(g, 14, 0, 21, CELL_WALL)
    _h_line(g, 21, 4, 21, CELL_WALL)
    _h_line(g, 28, 0, 21, CELL_WALL)
    _h_line(g, 34, 4, 21, CELL_WALL)
    _fill_rect(g, 8, 6, 8, 5, CELL_WATER)
    _fill_rect(g, 22, 8, 8, 5, CELL_WATER)
    _fill_rect(g, 15, 16, 5, 5, CELL_WATER)
    _fill_rect(g, 29, 14, 6, 4, CELL_MUD)
    return g


def create_level_8():
    """Hard 8: Masmorra de Terreno"""
    g = Grid(40, 25)
    g.set_cell(1, 1, CELL_START)
    g.set_cell(38, 23, CELL_GOAL)
    _h_line(g, 5, 0, 12, CELL_WALL)
    _h_line(g, 5, 14, 11, CELL_WALL)
    _h_line(g, 11, 0, 8, CELL_WALL)
    _h_line(g, 11, 15, 10, CELL_WALL)
    _h_line(g, 18, 0, 10, CELL_WALL)
    _h_line(g, 18, 14, 11, CELL_WALL)
    _h_line(g, 25, 5, 10, CELL_WALL)
    _h_line(g, 25, 18, 7, CELL_WALL)
    _h_line(g, 32, 0, 12, CELL_WALL)
    _h_line(g, 32, 15, 10, CELL_WALL)
    _v_line(g, 5, 12, 7, CELL_EMPTY)
    _v_line(g, 11, 8, 8, CELL_EMPTY)
    _v_line(g, 18, 10, 8, CELL_EMPTY)
    _v_line(g, 25, 15, 8, CELL_EMPTY)
    _fill_rect(g, 1, 13, 4, 1, CELL_GRASS)
    _fill_rect(g, 6, 13, 4, 1, CELL_MUD)
    _fill_rect(g, 12, 9, 4, 1, CELL_GRASS)
    _fill_rect(g, 19, 11, 4, 1, CELL_MUD)
    _fill_rect(g, 26, 16, 4, 1, CELL_WATER)
    _fill_rect(g, 33, 13, 4, 1, CELL_WATER)
    _fill_rect(g, 27, 5, 4, 2, CELL_MUD)
    return g


def create_level_9():
    """Hard 9: Teia de Aranha"""
    g = Grid(40, 25)
    g.set_cell(2, 2, CELL_START)
    g.set_cell(37, 22, CELL_GOAL)
    for i in range(6):
        row = 2 + i * 6
        _h_line(g, row, 0, 25, CELL_WALL)
        if row + 3 < 40:
            _v_line(g, row, 2 + i * 4, 7, CELL_EMPTY)
    _v_line(g, 0, 0, 40, CELL_WALL)
    _v_line(g, 0, 24, 40, CELL_WALL)
    _h_line(g, 0, 0, 25, CELL_WALL)
    _h_line(g, 39, 0, 25, CELL_WALL)
    _v_line(g, 0, 1, 40, CELL_EMPTY)
    _v_line(g, 0, 23, 40, CELL_EMPTY)
    _h_line(g, 1, 1, 23, CELL_EMPTY)
    _h_line(g, 38, 1, 23, CELL_EMPTY)
    _fill_rect(g, 3, 14, 3, 3, CELL_GRASS)
    _fill_rect(g, 15, 6, 3, 4, CELL_MUD)
    _fill_rect(g, 27, 18, 3, 3, CELL_WATER)
    _fill_rect(g, 20, 14, 3, 3, CELL_WATER)
    return g


def create_level_10():
    """Extreme 10: O Labirinto Final"""
    g = Grid(50, 30)
    g.set_cell(1, 1, CELL_START)
    g.set_cell(48, 28, CELL_GOAL)
    _h_line(g, 3, 0, 12, CELL_WALL)
    _h_line(g, 3, 17, 13, CELL_WALL)
    _h_line(g, 7, 0, 8, CELL_WALL)
    _h_line(g, 7, 15, 15, CELL_WALL)
    _h_line(g, 12, 5, 10, CELL_WALL)
    _h_line(g, 12, 18, 12, CELL_WALL)
    _h_line(g, 17, 0, 14, CELL_WALL)
    _h_line(g, 17, 16, 14, CELL_WALL)
    _h_line(g, 23, 0, 10, CELL_WALL)
    _h_line(g, 23, 17, 13, CELL_WALL)
    _h_line(g, 28, 3, 12, CELL_WALL)
    _h_line(g, 28, 18, 12, CELL_WALL)
    _h_line(g, 33, 0, 10, CELL_WALL)
    _h_line(g, 33, 15, 15, CELL_WALL)
    _h_line(g, 38, 4, 14, CELL_WALL)
    _h_line(g, 38, 20, 10, CELL_WALL)
    _h_line(g, 44, 0, 12, CELL_WALL)
    _h_line(g, 44, 16, 14, CELL_WALL)
    _v_line(g, 3, 12, 5, CELL_EMPTY)
    _v_line(g, 3, 17, 5, CELL_EMPTY)
    _v_line(g, 7, 8, 6, CELL_EMPTY)
    _v_line(g, 12, 15, 6, CELL_EMPTY)
    _v_line(g, 17, 14, 7, CELL_EMPTY)
    _v_line(g, 17, 16, 7, CELL_EMPTY)
    _v_line(g, 23, 10, 6, CELL_EMPTY)
    _v_line(g, 28, 15, 6, CELL_EMPTY)
    _v_line(g, 33, 10, 6, CELL_EMPTY)
    _v_line(g, 38, 18, 7, CELL_EMPTY)
    _fill_rect(g, 4, 14, 2, 2, CELL_GRASS)
    _fill_rect(g, 13, 16, 3, 1, CELL_WATER)
    _fill_rect(g, 18, 15, 3, 1, CELL_MUD)
    _fill_rect(g, 24, 11, 3, 2, CELL_WATER)
    _fill_rect(g, 29, 16, 2, 2, CELL_GRASS)
    _fill_rect(g, 34, 11, 3, 2, CELL_MUD)
    _fill_rect(g, 39, 19, 3, 1, CELL_WATER)
    _fill_rect(g, 45, 13, 2, 3, CELL_GRASS)
    _fill_rect(g, 40, 20, 3, 3, CELL_WATER)
    return g


# ──────────────────────────── Fases novas ────────────────────────────


def create_level_easy_4():
    """Easy: Pedras no Caminho (20x15)"""
    g = Grid(20, 15)
    g.set_cell(1, 1, CELL_START)
    g.set_cell(18, 13, CELL_GOAL)
    _h_line(g, 6, 0, 10, CELL_WALL)
    _h_line(g, 12, 5, 10, CELL_WALL)
    _fill_rect(g, 7, 2, 3, 2, CELL_GRASS)
    _fill_rect(g, 13, 1, 3, 2, CELL_GRASS)
    return g


def create_level_easy_5():
    """Easy: Jardim Cercado (20x15)"""
    g = Grid(20, 15)
    g.set_cell(1, 1, CELL_START)
    g.set_cell(18, 13, CELL_GOAL)
    _h_line(g, 4, 3, 12, CELL_WALL)
    _v_line(g, 4, 3, 6, CELL_WALL)
    _h_line(g, 14, 0, 12, CELL_WALL)
    _fill_rect(g, 8, 6, 4, 3, CELL_GRASS)
    _fill_rect(g, 15, 9, 3, 2, CELL_MUD)
    return g


def create_level_medium_9():
    """Medium: Pantano Dividido (30x20)"""
    g = Grid(30, 20)
    g.set_cell(1, 1, CELL_START)
    g.set_cell(28, 18, CELL_GOAL)
    _h_line(g, 7, 0, 15, CELL_WALL)
    _h_line(g, 14, 5, 15, CELL_WALL)
    _h_line(g, 21, 0, 14, CELL_WALL)
    _fill_rect(g, 8, 2, 5, 4, CELL_MUD)
    _fill_rect(g, 15, 12, 5, 4, CELL_WATER)
    _fill_rect(g, 22, 3, 5, 3, CELL_GRASS)
    return g


def create_level_medium_10():
    """Medium: Travessia Lamacenta (30x20)"""
    g = Grid(30, 20)
    g.set_cell(1, 1, CELL_START)
    g.set_cell(28, 18, CELL_GOAL)
    _h_line(g, 6, 2, 18, CELL_WALL)
    _h_line(g, 12, 0, 18, CELL_WALL)
    _h_line(g, 18, 2, 18, CELL_WALL)
    _h_line(g, 24, 0, 18, CELL_WALL)
    _fill_rect(g, 7, 4, 6, 4, CELL_MUD)
    _fill_rect(g, 19, 6, 6, 4, CELL_GRASS)
    return g


def create_level_hard_14():
    """Hard: Cavernas Inundadas (40x25)"""
    g = Grid(40, 25)
    g.set_cell(1, 1, CELL_START)
    g.set_cell(38, 23, CELL_GOAL)
    _h_line(g, 6, 0, 18, CELL_WALL)
    _h_line(g, 12, 6, 19, CELL_WALL)
    _h_line(g, 18, 0, 18, CELL_WALL)
    _h_line(g, 24, 6, 19, CELL_WALL)
    _h_line(g, 30, 0, 18, CELL_WALL)
    _fill_rect(g, 7, 2, 8, 4, CELL_WATER)
    _fill_rect(g, 19, 8, 8, 4, CELL_WATER)
    _fill_rect(g, 31, 3, 6, 4, CELL_MUD)
    return g


def create_level_hard_15():
    """Hard: Fortaleza (40x25)"""
    g = Grid(40, 25)
    g.set_cell(1, 1, CELL_START)
    g.set_cell(38, 23, CELL_GOAL)
    _v_line(g, 0, 8, 32, CELL_WALL)
    _v_line(g, 8, 16, 32, CELL_WALL)
    _v_line(g, 0, 24, 32, CELL_WALL)
    _fill_rect(g, 4, 2, 4, 12, CELL_MUD)
    _fill_rect(g, 12, 18, 4, 12, CELL_WATER)
    return g


def create_level_extreme_17():
    """Extreme/Hardcore: Abismo (50x30)"""
    g = Grid(50, 30)
    g.set_cell(1, 1, CELL_START)
    g.set_cell(48, 28, CELL_GOAL)
    _h_line(g, 5, 0, 26, CELL_WALL)
    _h_line(g, 11, 4, 26, CELL_WALL)
    _h_line(g, 17, 0, 26, CELL_WALL)
    _h_line(g, 23, 4, 26, CELL_WALL)
    _h_line(g, 29, 0, 26, CELL_WALL)
    _h_line(g, 35, 4, 26, CELL_WALL)
    _h_line(g, 41, 0, 26, CELL_WALL)
    # Toque hardcore: agua bloqueia os atalhos curtos, grama vira o desvio barato
    _fill_rect(g, 6, 22, 5, 7, CELL_WATER)
    _fill_rect(g, 18, 22, 5, 7, CELL_WATER)
    _fill_rect(g, 30, 22, 5, 7, CELL_WATER)
    _fill_rect(g, 12, 1, 5, 6, CELL_GRASS)
    _fill_rect(g, 36, 1, 5, 6, CELL_GRASS)
    return g


def create_level_extreme_18():
    """Extreme/Hardcore: Labirinto Profundo (50x30)"""
    g = Grid(50, 30)
    g.set_cell(1, 1, CELL_START)
    g.set_cell(48, 28, CELL_GOAL)
    _v_line(g, 0, 7, 42, CELL_WALL)
    _v_line(g, 8, 14, 42, CELL_WALL)
    _v_line(g, 0, 21, 42, CELL_WALL)
    _fill_rect(g, 4, 1, 5, 14, CELL_MUD)
    _fill_rect(g, 12, 9, 4, 4, CELL_GRASS)
    _fill_rect(g, 30, 15, 5, 6, CELL_WATER)
    return g


LEVELS = [
    # Facil
    {"name": "1: Primeiro Passo", "difficulty": DIFF_EASY, "fn": create_level_1},
    {"name": "2: Colunas Esparsas", "difficulty": DIFF_EASY, "fn": create_level_2},
    {"name": "3: Duas Salas", "difficulty": DIFF_EASY, "fn": create_level_3},
    {"name": "4: Pedras no Caminho", "difficulty": DIFF_EASY, "fn": create_level_easy_4},
    {"name": "5: Jardim Cercado", "difficulty": DIFF_EASY, "fn": create_level_easy_5},
    # Medio
    {"name": "6: Labirinto Verde", "difficulty": DIFF_MEDIUM, "fn": create_level_4},
    {"name": "7: Atalhos de Lama", "difficulty": DIFF_MEDIUM, "fn": create_level_5},
    {"name": "8: Zig Zag", "difficulty": DIFF_MEDIUM, "fn": create_level_6},
    {"name": "9: Pantano Dividido", "difficulty": DIFF_MEDIUM, "fn": create_level_medium_9},
    {"name": "10: Travessia Lamacenta", "difficulty": DIFF_MEDIUM, "fn": create_level_medium_10},
    # Dificil
    {"name": "11: Aqua Maze", "difficulty": DIFF_HARD, "fn": create_level_7},
    {"name": "12: Masmorra de Terreno", "difficulty": DIFF_HARD, "fn": create_level_8},
    {"name": "13: Teia de Aranha", "difficulty": DIFF_HARD, "fn": create_level_9},
    {"name": "14: Cavernas Inundadas", "difficulty": DIFF_HARD, "fn": create_level_hard_14},
    {"name": "15: Fortaleza", "difficulty": DIFF_HARD, "fn": create_level_hard_15},
    # Hardcore (Extremo)
    {"name": "16: O Labirinto Final", "difficulty": DIFF_EXTREME, "fn": create_level_10},
    {"name": "17: Abismo", "difficulty": DIFF_EXTREME, "fn": create_level_extreme_17},
    {"name": "18: Labirinto Profundo", "difficulty": DIFF_EXTREME, "fn": create_level_extreme_18},
]


def get_level(index):
    if 0 <= index < len(LEVELS):
        info = LEVELS[index]
        grid = info["fn"]()
        return {"name": info["name"], "difficulty": info["difficulty"], "grid": grid}
    return None
