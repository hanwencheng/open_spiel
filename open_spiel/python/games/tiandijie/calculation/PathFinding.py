import heapq
from collections import deque
from typing import List

from open_spiel.python.games.tiandijie.types.map.Terrain import Terrain
from open_spiel.python.games.tiandijie.types.map.TerrainType import TerrainType

type TerrainMap = List[List[Terrain]]


def is_accessible(x, y, terrain_map: TerrainMap, can_fly):
    if can_fly:
        return terrain_map[y][x].terrain_type in [TerrainType.NORMAL, TerrainType.FLYABLE_OBSTACLE,
                                                  TerrainType.EFFECT_SPAWN, TerrainType.HERO_SPAWN]
    else:
        return terrain_map[y][x].terrain_type in [TerrainType.NORMAL, TerrainType.EFFECT_SPAWN, TerrainType.HERO_SPAWN]


def bfs_move_range(start, move_limit, terrain_map: TerrainMap, can_fly):
    width, height = len(terrain_map[0]), len(terrain_map)
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Four directions
    visited = set()  # Record visited positions
    queue = deque([(start, 0)])  # Position and steps from the start
    reachable = []

    while queue:
        (x, y), steps = queue.popleft()
        if steps <= move_limit and is_accessible(x, y, terrain_map, can_fly):
            reachable.append((x, y))
            for dx, dy in directions:
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < width and 0 <= new_y < height and (new_x, new_y) not in visited:
                    visited.add((new_x, new_y))
                    queue.append(((new_x, new_y), steps + 1))

    return reachable


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return not self.elements

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


def heuristic(a, b):
    (x1, y1), (x2, y2) = a, b
    return abs(x1 - x2) + abs(y1 - y2)


def a_star_search(start, goal, battle_map, can_fly):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {start: None}
    cost_so_far = {start: 0}

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        for next in get_neighbors(current, battle_map, can_fly):
            new_cost = cost_so_far[current] + 1  # Assumes equal cost for each step
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                frontier.put(next, priority)
                came_from[next] = current

    return reconstruct_path(came_from, start, goal)


def get_neighbors(position, battle_map, can_fly):
    (x, y) = position
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    neighbors = []
    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < len(battle_map[0]) and 0 <= new_y < len(battle_map):
            if is_accessible(new_x, new_y, battle_map, can_fly):
                neighbors.append((new_x, new_y))
    return neighbors


def reconstruct_path(came_from, start, goal):
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path


def get_path_terrain_types(path, battle_map):
    return [battle_map[y][x].terrain_type for x, y in path]
