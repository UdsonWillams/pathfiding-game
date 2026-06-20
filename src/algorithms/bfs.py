from collections import deque
from .base import SearchAlgorithm


class BFS(SearchAlgorithm):
    name = "BFS (Busca em Largura)"

    def __init__(self):
        super().__init__()
        self._queue = None
        self._seen = set()

    def setup(self, grid, start, goal):
        super().setup(grid, start, goal)
        self._queue = deque([start])
        self._seen = {start}
        self._came_from = {start: None}

    def step(self):
        if self._done:
            return self._make_state([], True, self._path)

        if not self._queue:
            self._done = True
            return self._make_state([], True, None)

        current = self._queue.popleft()
        self._visited.add(current)
        self._current = current
        self.stats["nodes_visited"] = len(self._visited)

        if current == self.goal:
            self._done = True
            self._path = self.reconstruct_path()
            return self._make_state([], True, self._path)

        for neighbor in self.grid.get_neighbors(current):
            if neighbor not in self._seen:
                self._seen.add(neighbor)
                self._came_from[neighbor] = current
                self._queue.append(neighbor)

        return self._make_state(self._queue, False)
