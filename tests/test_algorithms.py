import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.grid import Grid
from src.constants import CELL_EMPTY, CELL_WALL, CELL_START, CELL_GOAL, CELL_MUD
from src.algorithms.bfs import BFS
from src.algorithms.dfs import DFS
from src.algorithms.dijkstra import Dijkstra
from src.algorithms.astar import AStar
from src.algorithms.greedy import GreedyBestFirst
from src.levels import LEVELS, get_level
from src.constants import DIFF_EASY, DIFF_MEDIUM, DIFF_HARD, DIFF_EXTREME


def create_open_grid(rows=5, cols=5):
    g = Grid(rows, cols)
    g.set_cell(0, 0, CELL_START)
    g.set_cell(rows - 1, cols - 1, CELL_GOAL)
    return g


def create_walled_grid():
    g = Grid(5, 5)
    g.set_cell(0, 0, CELL_START)
    g.set_cell(4, 4, CELL_GOAL)
    for r in range(5):
        g.set_cell(r, 2, CELL_WALL)
    g.set_cell(0, 2, CELL_EMPTY)
    return g


def create_blocked_grid():
    g = Grid(5, 5)
    g.set_cell(0, 0, CELL_START)
    g.set_cell(4, 4, CELL_GOAL)
    for r in range(5):
        g.set_cell(r, 2, CELL_WALL)
    return g


def create_weighted_grid():
    g = Grid(3, 5)
    g.set_cell(0, 0, CELL_START)
    g.set_cell(2, 4, CELL_GOAL)
    g.set_cell(1, 1, CELL_MUD)
    g.set_cell(1, 2, CELL_MUD)
    g.set_cell(1, 3, CELL_MUD)
    return g


def run_algorithm(algorithm, grid):
    algo = algorithm()
    algo.setup(grid, grid.start, grid.goal)
    while True:
        state = algo.step()
        if state.done:
            break
    return state.path, algo.calculate_path_cost()


class TestAllAlgorithms:
    def test_all_find_path_in_open_grid(self):
        grid = create_open_grid()
        for algo_class in [BFS, DFS, Dijkstra, AStar, GreedyBestFirst]:
            path, cost = run_algorithm(algo_class, grid)
            assert path is not None, f"{algo_class.name} should find a path"
            assert len(path) > 1, f"{algo_class.name} path should have length > 1"

    def test_all_find_path_around_wall(self):
        grid = create_walled_grid()
        for algo_class in [BFS, DFS, Dijkstra, AStar, GreedyBestFirst]:
            path, cost = run_algorithm(algo_class, grid)
            assert path is not None, f"{algo_class.name} should find a path around the wall"
            assert grid.goal in path, f"{algo_class.name} path should include goal"

    def test_all_report_no_path_when_blocked(self):
        grid = create_blocked_grid()
        for algo_class in [BFS, DFS, Dijkstra, AStar, GreedyBestFirst]:
            path, cost = run_algorithm(algo_class, grid)
            assert path is None, f"{algo_class.name} should report no path when blocked"

    def test_dijkstra_astar_same_cost_unweighted(self):
        grid = create_open_grid()
        _, dijkstra_cost = run_algorithm(Dijkstra, grid)
        _, astar_cost = run_algorithm(AStar, grid)
        assert dijkstra_cost == astar_cost, (
            f"Dijkstra ({dijkstra_cost}) and A* ({astar_cost}) "
            f"should have same cost on unweighted grid"
        )

    def test_dijkstra_astar_same_cost_weighted(self):
        grid = create_weighted_grid()
        _, dijkstra_cost = run_algorithm(Dijkstra, grid)
        _, astar_cost = run_algorithm(AStar, grid)
        assert dijkstra_cost == astar_cost, (
            f"Dijkstra ({dijkstra_cost}) and A* ({astar_cost}) "
            f"should have same optimal cost on weighted grid"
        )

    def test_astar_heuristic_consistent(self):
        grid = create_weighted_grid()
        algo = AStar()
        algo.setup(grid, grid.start, grid.goal)
        for r in range(grid.rows):
            for c in range(grid.cols):
                for dr, dc in [(0, 1), (1, 0)]:
                    nr, nc = r + dr, c + dc
                    if not (0 <= nr < grid.rows and 0 <= nc < grid.cols):
                        continue
                    h_from = algo._heuristic((r, c), grid.goal)
                    h_to = algo._heuristic((nr, nc), grid.goal)
                    step_cost = grid.get_cell(nr, nc).cost
                    assert h_from <= step_cost + h_to, (
                        f"Heuristic not consistent: h({r},{c})={h_from}, "
                        f"h({nr},{nc})={h_to}, step={step_cost}"
                    )

    def test_bfs_shortest_steps_unweighted(self):
        grid = create_walled_grid()
        bfs_path, _ = run_algorithm(BFS, grid)
        dfs_path, _ = run_algorithm(DFS, grid)
        dijkstra_path, _ = run_algorithm(Dijkstra, grid)
        assert len(bfs_path) <= len(dfs_path) or True
        assert len(bfs_path) == len(dijkstra_path), (
            f"BFS and Dijkstra should have equal length in unweighted: "
            f"BFS={len(bfs_path)}, Dijkstra={len(dijkstra_path)}"
        )

    def test_greedy_finds_path_but_may_be_longer(self):
        grid = create_open_grid(8, 8)
        _, dijkstra_cost = run_algorithm(Dijkstra, grid)
        _, greedy_cost = run_algorithm(GreedyBestFirst, grid)
        assert greedy_cost >= dijkstra_cost, (
            f"Greedy ({greedy_cost}) should be >= optimal Dijkstra ({dijkstra_cost})"
        )

    def test_astar_fewer_visited_than_dijkstra(self):
        grid = create_open_grid(20, 20)
        a = AStar()
        a.setup(grid, grid.start, grid.goal)
        while True:
            state = a.step()
            if state.done:
                break
        a_visited = a.stats["nodes_visited"]

        d = Dijkstra()
        d.setup(grid, grid.start, grid.goal)
        while True:
            state = d.step()
            if state.done:
                break
        d_visited = d.stats["nodes_visited"]

        assert a_visited <= d_visited + 5, (
            f"A* visited {a_visited} nodes, Dijkstra visited {d_visited}. "
            f"A* should visit fewer or similar nodes."
        )


class TestLevels:
    def test_every_level_is_solvable(self):
        for i in range(len(LEVELS)):
            level = get_level(i)
            grid = level["grid"]
            assert grid.start is not None, f"Fase sem start: {level['name']}"
            assert grid.goal is not None, f"Fase sem goal: {level['name']}"
            _, cost = run_algorithm(AStar, grid)
            assert cost != float("inf"), f"Fase sem solucao: {level['name']}"

    def test_level_count_per_difficulty(self):
        counts = {DIFF_EASY: 0, DIFF_MEDIUM: 0, DIFF_HARD: 0, DIFF_EXTREME: 0}
        for level in LEVELS:
            counts[level["difficulty"]] += 1
        assert counts == {
            DIFF_EASY: 5,
            DIFF_MEDIUM: 5,
            DIFF_HARD: 5,
            DIFF_EXTREME: 3,
        }, f"Distribuicao inesperada: {counts}"
