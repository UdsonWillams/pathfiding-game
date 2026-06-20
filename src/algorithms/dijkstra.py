import heapq
from .base import SearchAlgorithm


class Dijkstra(SearchAlgorithm):
    name = "Dijkstra"

    def __init__(self):
        super().__init__()
        self._pq = None
        self._costs = {}

    def setup(self, grid, start, goal):
        super().setup(grid, start, goal)
        self._pq = [(0, start)]
        self._costs = {start: 0}
        self._came_from = {start: None}

    def step(self):
        if self._done:
            return self._make_state([], True, self._path)

        if not self._pq:
            self._done = True
            return self._make_state([], True, None)

        cost, current = heapq.heappop(self._pq)

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
                new_cost = cost + self.grid.get_cell(*neighbor).cost
                if neighbor not in self._costs or new_cost < self._costs[neighbor]:
                    self._costs[neighbor] = new_cost
                    self._came_from[neighbor] = current
                    heapq.heappush(self._pq, (new_cost, neighbor))

        return self._make_state(self._pq, False)
