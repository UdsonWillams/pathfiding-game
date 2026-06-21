from .base import SearchAlgorithm


class BeamSearch(SearchAlgorithm):
    name = "Beam Search"
    BEAM_WIDTH = 3

    def __init__(self):
        super().__init__()
        self._frontier = []
        self._seen = set()

    def _heuristic(self, pos, goal):
        return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

    def setup(self, grid, start, goal):
        super().setup(grid, start, goal)
        h = self._heuristic(start, goal)
        self._frontier = [(h, start)]
        self._seen = {start}
        self._came_from = {start: None}

    def step(self):
        if self._done:
            return self._make_state(self._frontier, True, self._path)

        if not self._frontier:
            self._done = True
            return self._make_state([], True, None)

        current_h, current = self._frontier.pop(0)
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
                h = self._heuristic(neighbor, self.goal)
                self._frontier.append((h, neighbor))

        # Manter apenas os BEAM_WIDTH melhores por heuristica
        self._frontier.sort(key=lambda x: x[0])
        self._frontier = self._frontier[:self.BEAM_WIDTH]

        return self._make_state(self._frontier, False)
