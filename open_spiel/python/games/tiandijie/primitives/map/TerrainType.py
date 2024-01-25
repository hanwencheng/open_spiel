from enum import Enum


class TerrainType(Enum):
    NORMAL = (0, True, True, "Normal")
    FLYABLE_OBSTACLE = (1, False, True, "Flyable Obstacle")
    IMPASSABLE_OBSTACLE = (2, False, False, "Impassable Obstacle")
    HERO_SPAWN = (3, False, False, "Hero Spawn")
    EFFECT_SPAWN = (4, True, True, "Effect Spawn")
