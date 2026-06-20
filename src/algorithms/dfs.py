from .base import SearchAlgorithm


class DFS(SearchAlgorithm):
    name = "DFS (Busca em Profundidade)"

    def __init__(self):
        super().__init__()
        self._stack = None
        self._seen = set()

    def setup(self, grid, start, goal):
        super().setup(grid, start, goal)
        self._stack = [start]
        self._seen = {start}
        self._came_from = {start: None}

    def step(self):
        if self._done:
            return self._make_state([], True, self._path)

        if not self._stack:
            self._done = True
            return self._make_state([], True, None)

        current = self._stack.pop()
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
                self._stack.append(neighbor)

        return self._make_state(self._stack, False)
