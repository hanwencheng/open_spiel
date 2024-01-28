import enum
from typing import Callable, Any
from typing import List

from open_spiel.python.games.tiandijie.calculation.Range import Range
from open_spiel.python.games.tiandijie.calculation.RangeType import RangeType
from open_spiel.python.games.tiandijie.primitives.Context import Context
from open_spiel.python.games.tiandijie.primitives.hero.HeroBasics import Professions


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
                 before_fixed_damage_modifier: List[Callable[..., Any]],
                 after_fixed_damage_modifier: List[Callable[..., Any]],
                 profession: Professions = None
                 ):
        self.damage_multiplier = damage_multiplier
        self.before_action_buff_modifier = before_buff_modifiers
        self.after_action_buff_modifier = after_buff_modifiers
        self.before_action_fixed_damage_modifier = before_fixed_damage_modifier
        self.after_action_fixed_damage_modifier = after_fixed_damage_modifier
        self.range = skill_range
        self.target_type = SkillTargetTypes.SELF


skill_range_profession_dict = {
    Professions.WARRIOR: Range(RangeType.DIAMOND, 1),
    Professions.SWORDSMAN: Range(RangeType.DIAMOND, 1),
    Professions.ARCHER: Range(RangeType.ARCHER, 2),
    Professions.SORCERER: Range(RangeType.DIAMOND, 2),
    Professions.PRIEST: Range(RangeType.DIAMOND, 2),
    Professions.GUARD: Range(RangeType.DIAMOND, 1),
}


class NormalAttack(Skill):
    def __init__(self, damage_multiplier: float, skill_range: Range,
                 before_buff_modifiers: List[Callable[[List[Context]], Any]],
                 after_buff_modifiers: List[Callable[[List[Context]], Any]],
                 before_fixed_damage_modifier: List[Callable[..., Any]],
                 after_fixed_damage_modifier: List[Callable[..., Any]],
                 profession: Professions
                 ):
        super().__init__(damage_multiplier, skill_range, before_buff_modifiers, after_buff_modifiers,
                         before_fixed_damage_modifier, after_fixed_damage_modifier)
        self.target_type = SkillTargetTypes.ENEMY_SINGLE
        self.damage_multiplier = 1.0
        self.skill_range = skill_range_profession_dict[profession]


def is_normal_attack(skill: Skill) -> bool:
    return isinstance(skill, NormalAttack)
