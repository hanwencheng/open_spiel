import enum
from typing import List
from open_spiel.python.games.tiandijie.basics import Position

from open_spiel.python.games.tiandijie.primitives.hero import Hero
from open_spiel.python.games.tiandijie.primitives.skill import Skill


class ActionTypes(enum.Enum):
    HEAL = 0
    SKILL_ATTACK = 1
    SUMMON = 2
    SELF = 3
    PASS = 4
    NORMAL_ATTACK = 5


class Action:
    def __init__(self, cast_hero: Hero, affected_heroes, is_magic: bool, skill: Skill, movable, actionable):
        self.targets: List[Hero] = affected_heroes
        self.total_damage: float = 0
        self.is_magic: bool = is_magic
        self.is_in_battle: bool = False
        self.skill: Skill = None
        self.type: ActionTypes = ActionTypes.PASS
        self.move_range: int = 0
        self.moves: List[Position] = []
        self.move_point: Position = (0, 0)
        self.action_point: Position = (0, 0)
        self.movable: bool = movable
        self.actionable: bool = actionable
        self.actor = cast_hero
        self.player_id = cast_hero.player_id

    def update_affected_heroes(self, affected_heroes: List[Hero]):
        self.targets = affected_heroes

    def update_total_damage(self, total_damage: float):
        self.total_damage = total_damage

    def update_is_in_battle(self, is_in_battle: bool):
        self.is_in_battle = is_in_battle
