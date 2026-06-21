from dataclasses import dataclass, field
from typing import Optional, Set, Dict, List, Tuple


@dataclass
class StepState:
    visited: Set[Tuple[int, int]] = field(default_factory=set)
    frontier: List[Tuple[int, int]] = field(default_factory=list)
    current: Optional[Tuple[int, int]] = None
    came_from: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = field(default_factory=dict)
    done: bool = False
    path: Optional[List[Tuple[int, int]]] = None
    frontier_b: List[Tuple[int, int]] = field(default_factory=list)
    visited_b: Set[Tuple[int, int]] = field(default_factory=set)


class SearchAlgorithm:
    name: str = "Base"

    def __init__(self):
        self.grid = None
        self.start = None
        self.goal = None
        self._done = False
        self._visited = set()
        self._came_from = {}
        self._current = None
        self._path = None
        self.stats = {"nodes_visited": 0}

    def setup(self, grid, start, goal):
        self.grid = grid
        self.start = start
        self.goal = goal
        self._done = False
        self._visited = set()
        self._came_from = {}
        self._current = None
        self._path = None
        self.stats = {"nodes_visited": 0}

    def step(self):
        raise NotImplementedError

    def reconstruct_path(self):
        if not self._came_from or self.goal not in self._came_from:
            return None
        path = []
        current = self.goal
        while current is not None:
            path.append(current)
            current = self._came_from.get(current)
        path.reverse()
        return path

    def calculate_path_cost(self):
        if not self._path:
            return float("inf")
        total = 0
        for pos in self._path[1:]:
            cell = self.grid.get_cell(*pos)
            if cell:
                total += cell.cost
        return total

    def _make_state(self, frontier, done, path=None, frontier_b=None, visited_b=None):
        items = []
        for item in frontier:
            if isinstance(item, tuple) and len(item) >= 2:
                pos = item[1] if len(item) == 2 and isinstance(item[1], tuple) else item
                if isinstance(pos, tuple) and len(pos) == 2:
                    items.append(pos)
        return StepState(
            visited=self._visited.copy(),
            frontier=items,
            current=self._current,
            came_from=self._came_from.copy(),
            done=done,
            path=path,
            frontier_b=frontier_b if frontier_b else [],
            visited_b=visited_b if visited_b else set(),
        )
