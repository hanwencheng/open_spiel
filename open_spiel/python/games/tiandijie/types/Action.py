from typing import List

from open_spiel.python.games.tiandijie.types import Hero


class Action:
    def __init__(self, cast_hero: Hero, affected_heroes: List[Hero]):
        self.target = affected_heroes
        self.total_damage = 0

    def update_affected_heroes(self, affected_heroes: List[Hero]):
        self.target = affected_heroes

    def update_total_damage(self, total_damage: float):
        self.total_damage = total_damage



