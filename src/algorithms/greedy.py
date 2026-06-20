import heapq
from .base import SearchAlgorithm


class GreedyBestFirst(SearchAlgorithm):
    name = "Greedy Best-First"

    def __init__(self):
        super().__init__()
        self._pq = None

    def _heuristic(self, pos, goal):
        return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

    def setup(self, grid, start, goal):
        super().setup(grid, start, goal)
        h = self._heuristic(start, goal)
        self._pq = [(h, start)]
        self._visited = {start}
        self._came_from = {start: None}

    def step(self):
        if self._done:
            return self._make_state([], True, self._path)

        if not self._pq:
            self._done = True
            return self._make_state([], True, None)

        _, current = heapq.heappop(self._pq)
        self._current = current
        self.stats["nodes_visited"] = len(self._visited)

        if current == self.goal:
            self._done = True
            self._path = self.reconstruct_path()
            return self._make_state([], True, self._path)

        for neighbor in self.grid.get_neighbors(current):
            if neighbor not in self._visited:
                self._visited.add(neighbor)
                self._came_from[neighbor] = current
                h = self._heuristic(neighbor, self.goal)
                heapq.heappush(self._pq, (h, neighbor))

        return self._make_state(self._pq, False)
