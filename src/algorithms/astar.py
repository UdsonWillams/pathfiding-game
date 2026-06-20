import heapq
from .base import SearchAlgorithm


class AStar(SearchAlgorithm):
    name = "A* (A-Star)"

    def __init__(self):
        super().__init__()
        self._pq = None
        self._g_score = {}
        self._f_score = {}

    def _heuristic(self, pos, goal):
        return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

    def setup(self, grid, start, goal):
        super().setup(grid, start, goal)
        h = self._heuristic(start, goal)
        self._pq = [(h, start)]
        self._g_score = {start: 0}
        self._f_score = {start: h}
        self._came_from = {start: None}

    def step(self):
        if self._done:
            return self._make_state([], True, self._path)

        if not self._pq:
            self._done = True
            return self._make_state([], True, None)

        _, current = heapq.heappop(self._pq)

        if current in self._visited:
            return self._make_state(self._pq, False)

        self._visited.add(current)
        self._current = current
        self.stats["nodes_visited"] = len(self._visited)

        if current == self.goal:
            self._done = True
            self._path = self.reconstruct_path()
            return self._make_state([], True, self._path)

        for neighbor in self.grid.get_neighbors(current):
            if neighbor not in self._visited:
                tentative_g = self._g_score.get(current, 0) + self.grid.get_cell(*neighbor).cost
                if tentative_g < self._g_score.get(neighbor, float("inf")):
                    self._came_from[neighbor] = current
                    self._g_score[neighbor] = tentative_g
                    f = tentative_g + self._heuristic(neighbor, self.goal)
                    self._f_score[neighbor] = f
                    heapq.heappush(self._pq, (f, neighbor))

        return self._make_state(self._pq, False)
