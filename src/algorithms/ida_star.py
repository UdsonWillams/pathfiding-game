from .base import SearchAlgorithm


class IDAStar(SearchAlgorithm):
    name = "IDA* (Iterative Deepening A*)"

    def __init__(self):
        super().__init__()
        self._threshold = 0
        self._next_threshold = float("inf")
        self._stack = []
        self._g_values = {}
        self._iteration = 0

    def _heuristic(self, pos, goal):
        return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

    def setup(self, grid, start, goal):
        super().setup(grid, start, goal)
        self._threshold = self._heuristic(start, goal)
        self._next_threshold = float("inf")
        self._stack = [(start, 0)]
        self._g_values = {start: 0}
        self._came_from = {start: None}
        self._iteration = 0

    def step(self):
        if self._done:
            return self._make_state(self._stack, True, self._path)

        # Reiniciar se stack esvaziar
        if not self._stack:
            if self._next_threshold == float("inf"):
                self._done = True
                return self._make_state([], True, None)

            # Proximo ciclo
            self._iteration += 1
            self._threshold = self._next_threshold
            self._next_threshold = float("inf")
            self._stack = [(self.start, 0)]
            self._visited.clear()
            self._came_from = {self.start: None}
            self._g_values = {self.start: 0}

        current, g = self._stack.pop()

        if current in self._visited:
            return self._make_state(self._stack, False)

        self._visited.add(current)
        self._current = current
        self.stats["nodes_visited"] = len(self._visited)

        if current == self.goal:
            self._done = True
            self._path = self.reconstruct_path()
            return self._make_state([], True, self._path)

        for neighbor in self.grid.get_neighbors(current):
            if neighbor not in self._visited:
                new_g = g + self.grid.get_cell(*neighbor).cost
                h = self._heuristic(neighbor, self.goal)
                f = new_g + h

                if f > self._threshold:
                    self._next_threshold = min(self._next_threshold, f)
                else:
                    if neighbor not in self._g_values or new_g < self._g_values[neighbor]:
                        self._g_values[neighbor] = new_g
                        self._came_from[neighbor] = current
                        self._stack.append((neighbor, new_g))

        return self._make_state(self._stack, False)
