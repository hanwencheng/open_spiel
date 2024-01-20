from typing import Callable, Any
from typing import List

from open_spiel.python.games.tiandijie.types import Buff, Range
from open_spiel.python.games.tiandijie.types.Context import Context


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
