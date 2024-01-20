from typing import List

from open_spiel.python.games.tiandijie.types import Hero, Skill


class Action:
    def __init__(self, cast_hero: Hero, affected_heroes, is_magic: bool, skill: Skill, movable, actionable):
        self.targets: List[Hero] = affected_heroes
        self.total_damage: float = 0
        self.is_magic: bool = is_magic
        self.skill: Skill = None
        self.move_range: int = 0
        self.move_point: List[int, int] = [0, 0]
        self.action_point: List[int, int] = [0, 0]
        self.movable: bool = movable
        self.actionable: bool = actionable

    def update_affected_heroes(self, affected_heroes: List[Hero]):
        self.targets = affected_heroes

    def update_total_damage(self, total_damage: float):
        self.total_damage = total_damage



