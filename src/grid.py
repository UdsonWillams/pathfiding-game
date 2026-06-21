from .constants import CELL_EMPTY, CELL_WALL, CELL_START, CELL_GOAL, CELL_COSTS


class Cell:
    def __init__(self, row, col, cell_type=CELL_EMPTY):
        self.row = row
        self.col = col
        self.cell_type = cell_type
        self.visited = False
        self.is_path = False
        self.is_frontier = False
        self.is_frontier_b = False
        self.is_visited_b = False

    @property
    def cost(self):
        return CELL_COSTS.get(self.cell_type, 1)

    @property
    def is_wall(self):
        return self.cell_type == CELL_WALL


class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.cells = [[Cell(r, c) for c in range(cols)] for r in range(rows)]
        self.start = None
        self.goal = None

    def get_cell(self, row, col):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.cells[row][col]
        return None

    def set_cell(self, row, col, cell_type):
        cell = self.get_cell(row, col)
        if cell is None:
            return
        if cell.cell_type == CELL_START:
            self.start = None
        if cell.cell_type == CELL_GOAL:
            self.goal = None
        cell.cell_type = cell_type
        if cell_type == CELL_START:
            self.start = (row, col)
        elif cell_type == CELL_GOAL:
            self.goal = (row, col)

    def get_neighbors(self, pos):
        row, col = pos
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        neighbors = []
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            cell = self.get_cell(nr, nc)
            if cell and not cell.is_wall:
                neighbors.append((nr, nc))
        return neighbors

    def reset_visual_state(self):
        for row in self.cells:
            for cell in row:
                cell.visited = False
                cell.is_path = False
                cell.is_frontier = False
                cell.is_frontier_b = False
                cell.is_visited_b = False

    def update_visual_state(self, front=None, visited_positions=None, path=None, front_b=None, visited_b=None):
        self.reset_visual_state()
        if visited_positions:
            for pos in visited_positions:
                cell = self.get_cell(*pos)
                if cell:
                    cell.visited = True
        if front:
            for pos in front:
                if isinstance(pos, tuple) and len(pos) == 2:
                    cell = self.get_cell(*pos)
                    if cell:
                        cell.is_frontier = True
        if path:
            for pos in path:
                cell = self.get_cell(*pos)
                if cell:
                    cell.is_path = True
        if visited_b:
            for pos in visited_b:
                cell = self.get_cell(*pos)
                if cell:
                    cell.is_visited_b = True
        if front_b:
            for pos in front_b:
                if isinstance(pos, tuple) and len(pos) == 2:
                    cell = self.get_cell(*pos)
                    if cell:
                        cell.is_frontier_b = True

    def to_level_data(self):
        data = []
        for r in range(self.rows):
            row = []
            for c in range(self.cols):
                row.append(self.cells[r][c].cell_type)
            data.append(row)
        return data

    @classmethod
    def from_level_data(cls, data):
        rows = len(data)
        cols = len(data[0])
        grid = cls(rows, cols)
        for r in range(rows):
            for c in range(cols):
                grid.set_cell(r, c, data[r][c])
        return grid
