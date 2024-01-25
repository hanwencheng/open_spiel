import string
from functools import reduce
from typing import List

from open_spiel.python.games.tiandijie.calculation.Effects import get_current_action
from open_spiel.python.games.tiandijie.primitives.Context import Context
from open_spiel.python.games.tiandijie.primitives.hero import Hero


class Modifier:
    def __init__(self, modifier_dict):
        # absolute attributes
        self.attack: float = 0
        self.magic_attack: float = 0
        self.defense: float = 0
        self.magic_defense: float = 0
        self.damage: float = 0
        self.damage_reduction: float = 0
        self.magic_damage: float = 0
        self.magic_damage_reduction: float = 0
        self.heal: float = 0
        self.life: float = 0
        self.luck: float = 0
        self.critical: float = 0
        self.critical_reduction: float = 0
        # self.critical_damage = 0
        # self.critical_damage_reduction = 0

        # Percentage attributes
        self.attack_percentage: float = 1
        self.magic_attack_percentage: float = 1
        self.defense_percentage: float = 1
        self.magic_defense_percentage: float = 1
        self.damage_percentage: float = 1
        self.damage_reduction_percentage: float = 1
        self.magic_damage_percentage: float = 1
        self.magic_damage_reduction_percentage: float = 1
        self.heal_percentage: float = 1
        self.life_percentage: float = 1

        self.luck_percentage: float = 1
        self.critical_damage_percentage: float = 1
        self.critical_damage_reduction_percentage: float = 1
        self.fixed_damage_reduction_percentage: float = 1

        # Other
        self.move_range: int = 0
        self.attack_range: int = 0

        self.absolute_defense_range: int = 1
        self.passives_disabled: bool = False
        self.action_disabled: bool = False
        self.no_counterattack: bool = False
        self.counterattack_first: bool = False
        self.counterattack_first_limit: int = 0

        # Update attributes from dictionary
        for key, value in modifier_dict.items():
            if hasattr(self, key):
                setattr(self, key, value)


def accumulate_attribute(modifiers: List[Modifier], attr_name: string) -> float:
    return reduce(lambda total, buff: total + getattr(buff, attr_name, 0), modifiers, 0)


def merge_modifier(total: Modifier, hero: Hero, attr_name: string) -> Modifier:
    setattr(total, attr_name, getattr(total, attr_name, 0) + getattr(hero.talents, attr_name, 0))
    return total


def accumulate_talents_modifier(context: Context, attr_name: string) -> float:
    current_player_id = context.get_current_player_id()
    partner_heroes = context.get_heroes_by_player_id(current_player_id)
    counter_heroes = context.get_heroes_by_counter_player_id(current_player_id)

    partner_talents = reduce(lambda total, hero: total + getattr(hero.talents, attr_name), partner_heroes, float(0))
    counter_talents = reduce(lambda total, hero: total + getattr(total, hero.talents, attr_name), counter_heroes, float(0))
    return partner_talents + counter_talents

