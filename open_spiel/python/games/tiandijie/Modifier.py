from functools import reduce
from typing import List


class Modifier:
    def __init__(self):
        # absolute attributes
        self.attack = 0
        self.magic_attack = 0
        self.defense = 0
        self.magic_defense = 0
        self.damage = 0
        self.damage_reduction = 0
        self.magic_damage = 0
        self.magic_damage_reduction = 0
        self.heal = 0
        self.life = 0
        self.luck = 0
        self.critical = 0
        self.critical_reduction = 0
        # self.critical_damage = 0
        # self.critical_damage_reduction = 0

        # Percentage attributes
        self.attack_percentage = 1
        self.magic_attack_percentage = 1
        self.defense_percentage = 1
        self.magic_defense_percentage = 1
        self.damage_percentage = 1
        self.damage_reduction_percentage = 1
        self.magic_damage_percentage = 1
        self.magic_damage_reduction_percentage = 1
        self.heal_percentage = 1
        self.life_percentage = 1

        self.luck_percentage = 1
        self.critical_damage_percentage = 1
        self.critical_damage_reduction_percentage = 1

        # Other
        self.move_range = 0
        self.attack_range = 0


def accumulate_defense_modifier(collection: List[Modifier], is_magic):
    attribute_name = 'magic_defense' if is_magic else 'defense'
    return accumulate_attribute(collection, attribute_name)


def accumulate_attack_modifier(collection: List[Modifier], is_magic):
    attribute_name = 'magic_attack' if is_magic else 'attack'
    return accumulate_attribute(collection, attribute_name)


def accumulate_damage_modifier(collection: List[Modifier], is_magic):
    attribute_name = 'magic_damage_percentage' if is_magic else 'damage_percentage'
    return accumulate_attribute(collection, attribute_name)


def accumulate_damage_reduction_modifier(collection: List[Modifier], is_magic):
    attribute_name = 'magic_damage_reduction' if is_magic else 'damage_reduction'
    return accumulate_attribute(collection, attribute_name)


def accumulate_attribute(modifier, attr_name):
    return reduce(lambda total, buff: total + getattr(buff, attr_name, 0), modifier, 0)
