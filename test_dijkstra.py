import importlib.util
from pathlib import Path
import unittest


module_path = Path(__file__).with_name("ift-2003-tp.py")
spec = importlib.util.spec_from_file_location("labyrinth", module_path)
game = importlib.util.module_from_spec(spec)
spec.loader.exec_module(game)


class DijkstraTests(unittest.TestCase):
    def setUp(self) -> None:
        # Keep the original values so every test starts cleanly.
        self.original_rows = game.ROWS
        self.original_columns = game.COLUMNS
        self.original_start = game.START
        self.original_exit = game.EXIT

        # A tiny board makes the expected answer easy to reason about.
        game.ROWS = 2
        game.COLUMNS = 3
        game.START = (0, 0)
        game.EXIT = (0, 2)

    def tearDown(self) -> None:
        game.ROWS = self.original_rows
        game.COLUMNS = self.original_columns
        game.START = self.original_start
        game.EXIT = self.original_exit

    def test_finds_shortest_path_on_empty_grid(self) -> None:
        path, stats = game.algo_2(walls=set())

        self.assertEqual(path[0], game.START)
        self.assertEqual(path[-1], game.EXIT)
        self.assertEqual(stats["cost"], 2)

if __name__ == "__main__":
    unittest.main()