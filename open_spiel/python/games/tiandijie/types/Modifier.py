import string
from functools import reduce
from typing import List


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
        self.passives_on: bool = True

        # Update attributes from dictionary
        for key, value in modifier_dict.items():
            if hasattr(self, key):
                setattr(self, key, value)


def accumulate_defense_modifier(collection: List[Modifier], is_magic: bool) -> float:
    attribute_name = 'magic_defense' if is_magic else 'defense'
    return accumulate_attribute(collection, attribute_name)


def accumulate_attack_modifier(collection: List[Modifier], is_magic: bool) -> float:
    attribute_name = 'magic_attack' if is_magic else 'attack'
    return accumulate_attribute(collection, attribute_name)


def accumulate_damage_modifier(collection: List[Modifier], is_magic: bool) -> float:
    attribute_name = 'magic_damage_percentage' if is_magic else 'damage_percentage'
    return accumulate_attribute(collection, attribute_name)


def accumulate_damage_reduction_modifier(collection: List[Modifier], is_magic: bool) -> float:
    attribute_name = 'magic_damage_reduction' if is_magic else 'damage_reduction'
    return accumulate_attribute(collection, attribute_name)


def accumulate_attribute(modifiers: List[Modifier], attr_name: string) -> float:
    return reduce(lambda total, buff: total + getattr(buff, attr_name, 0), modifiers, 0)
