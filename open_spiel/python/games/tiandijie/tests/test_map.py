import unittest

from open_spiel.python.games.tiandijie.calculation.PathFinding import bfs_move_range, a_star_search
from open_spiel.python.games.tiandijie.primitives.map.BattleMap import BattleMap


class TestMap(unittest.TestCase):
    # set up the test suite with a initial map
    def __int__(self):
        self.initial_terrain_map = [
            [0, 0, 2, 0, 0],
            [0, 1, 3, 1, 0],
            [2, 3, 4, 3, 2],
            [0, 1, 3, 1, 0],
            [0, 0, 2, 0, 0]
        ]
        self.initial_map = BattleMap(5, 5, self.initial_terrain_map)
        # display the initial map
        self.initial_map.display_map()

    def test_bfs_move_range(self):
        # test the move range of the actor
        actor_point = [2, 2]
        move_range = 2
        move_range_map = bfs_move_range(actor_point, move_range, self.initial_map, False)
        self.assertEqual(move_range_map, [[2, 2], [2, 1], [2, 3], [1, 2], [3, 2], [1, 1], [1, 3], [3, 1], [3, 3]])

    def test_a_start_search(self):
        # test the shortest path of the actor
        start_point = [2, 2]
        end_point = [4, 4]
        shortest_path = a_star_search(start_point, end_point, self.initial_map, False)
        self.assertEqual(shortest_path, [[2, 2], [3, 2], [4, 2], [4, 3], [4, 4]])
