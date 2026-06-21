from collections import deque
from .base import SearchAlgorithm, StepState


class BidirectionalBFS(SearchAlgorithm):
    name = "BiDir BFS (Busca Bidirecional)"

    def __init__(self):
        super().__init__()
        self._queue_fwd = None
        self._queue_bwd = None
        self._seen_fwd = set()
        self._seen_bwd = set()
        self._came_from_bwd = {}
        self._meeting = None

    def setup(self, grid, start, goal):
        super().setup(grid, start, goal)
        self._queue_fwd = deque([start])
        self._queue_bwd = deque([goal])
        self._seen_fwd = {start}
        self._seen_bwd = {goal}
        self._came_from[start] = None
        self._came_from_bwd = {goal: None}
        self._meeting = None
        self._visited = {start}
        self._visited_b = {goal}

    def step(self):
        if self._done:
            return self._make_state([], True, self._path,
                                   frontier_b=list(self._queue_bwd),
                                   visited_b=self._visited_b)

        if not self._queue_fwd and not self._queue_bwd:
            self._done = True
            return self._make_state([], True, None,
                                   frontier_b=list(self._queue_bwd),
                                   visited_b=self._visited_b)

        # Expand forward
        if self._queue_fwd:
            current = self._queue_fwd.popleft()
            self._visited.add(current)
            self._current = current

            if current in self._seen_bwd:
                self._done = True
                self._meeting = current
                self._path = self._reconstruct_bidirectional_path(current)
                return self._make_state([], True, self._path,
                                       frontier_b=list(self._queue_bwd),
                                       visited_b=self._visited_b)

            for neighbor in self.grid.get_neighbors(current):
                if neighbor not in self._seen_fwd:
                    self._seen_fwd.add(neighbor)
                    self._came_from[neighbor] = current
                    self._queue_fwd.append(neighbor)

        # Expand backward
        if self._queue_bwd:
            current = self._queue_bwd.popleft()
            self._visited_b.add(current)

            if current in self._seen_fwd:
                self._done = True
                self._meeting = current
                self._path = self._reconstruct_bidirectional_path(current)
                return self._make_state([], True, self._path,
                                       frontier_b=list(self._queue_bwd),
                                       visited_b=self._visited_b)

            for neighbor in self.grid.get_neighbors(current):
                if neighbor not in self._seen_bwd:
                    self._seen_bwd.add(neighbor)
                    self._came_from_bwd[neighbor] = current
                    self._queue_bwd.append(neighbor)

        self.stats["nodes_visited"] = len(self._visited)
        return self._make_state(list(self._queue_fwd), False,
                               frontier_b=list(self._queue_bwd),
                               visited_b=self._visited_b)

    def _reconstruct_bidirectional_path(self, meeting):
        path_fwd = []
        current = meeting
        while current is not None:
            path_fwd.append(current)
            current = self._came_from.get(current)
        path_fwd.reverse()

        path_bwd = []
        current = meeting
        while current is not None:
            path_bwd.append(current)
            current = self._came_from_bwd.get(current)

        return path_fwd + path_bwd[1:]
