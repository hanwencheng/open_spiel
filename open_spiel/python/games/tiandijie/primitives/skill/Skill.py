import enum
from typing import Callable, Any
from typing import List

from open_spiel.python.games.tiandijie.primitives import Range
from open_spiel.python.games.tiandijie.primitives.Context import Context

class SkillTargetTypes(enum.Enum):
    ENEMY_SINGLE = 0
    ENEMY_RANGE = 1
    PARTNER_SINGLE = 2
    PARTNER_RANGE = 3
    SELF = 4
    TERRAIN = 5

class Skill:
    def __init__(self, damage_multiplier: float, skill_range: Range,
                 before_buff_modifiers: List[Callable[[List[Context]], Any]],
                 after_buff_modifiers: List[Callable[[List[Context]], Any]],
                 before_fixed_damage_modifier: List[Callable[..., Any]] ,
                 after_fixed_damage_modifier: List[Callable[..., Any]],
                 ):
        self.damage_multiplier = damage_multiplier
        self.before_action_buff_modifier = before_buff_modifiers
        self.after_action_buff_modifier = after_buff_modifiers
        self.before_action_fixed_damage_modifier = before_fixed_damage_modifier
        self.after_action_fixed_damage_modifier = after_fixed_damage_modifier
        self.range = skill_range
        self.target_type = SkillTargetTypes.SELF
