import string
from functools import reduce
from typing import List

from open_spiel.python.games.tiandijie.calculation.Effects import get_current_action
from open_spiel.python.games.tiandijie.primitives.Action import Action
from open_spiel.python.games.tiandijie.primitives.Context import Context
from open_spiel.python.games.tiandijie.calculation.ModifierAttributes import ModifierAttributes
from open_spiel.python.games.tiandijie.primitives.formation.Formation import Formation
from open_spiel.python.games.tiandijie.primitives.formation.FormationEffect import FormationEffect
from open_spiel.python.games.tiandijie.primitives.hero import Hero


class Modifier:
    def __init__(self, modifier_dict):
        # self.attack: float = 0
        # self.magic_attack: float = 0
        # self.defense: float = 0
        # self.magic_defense: float = 0
        # self.magic_damage: float = 0
        # self.magic_damage_reduction: float = 0
        # self.heal: float = 0
        # self.life: float = 0
        # self.luck: float = 0
        # self.critical: float = 0
        # self.critical_reduction: float = 0
        #
        # self.attack_percentage: float = 0
        # self.skill_damage_percentage: float = 0
        # self.single_target_skill_damage_percentage: float = 0
        # self.multi_target_skill_damage_percentage: float = 0
        # self.normal_attack_damage_percentage: float = 0
        # self.battle_damage_percentage: float = 0
        #
        # self.magic_attack_percentage: float = 0
        # self.defense_percentage: float = 0
        # self.magic_defense_percentage: float = 0
        # self.damage_percentage: float = 0
        # self.damage_reduction_percentage: float = 0
        # self.magic_damage_percentage: float = 0
        # self.magic_damage_reduction_percentage: float = 0
        # self.heal_percentage: float = 0
        # self.life_percentage: float = 0
        #
        # self.luck_percentage: float = 0
        # self.critical_damage_percentage: float = 0
        # self.critical_damage_reduction_percentage: float = 0
        # self.fixed_damage_reduction_percentage: float = 0
        #
        # self.move_range: int = 0
        # self.attack_range: int = 0
        #
        # self.absolute_defense_range: int = 0
        # self.counterattack_first_limit: int = 0

        # self.is_passives_disabled: bool = False
        # self.is_action_disabled: bool = False
        # self.counterattack_disabled: bool = False
        # self.is_counterattack_first: bool = False

        for attribute_name in dir(ModifierAttributes):
            if attribute_name.startswith("is_"):
                attribute_name = getattr(ModifierAttributes, attribute_name)
                setattr(self, attribute_name, False)
            elif not attribute_name.startswith("__"):
                attribute_key = getattr(ModifierAttributes, attribute_name)
                setattr(self, attribute_key, 0)

        # Update attributes from dictionary
        for key, value in modifier_dict.items():
            if hasattr(self, key):
                setattr(self, key, value)


def accumulate_attribute(modifiers: List[Modifier], attr_name: string) -> float:
    return reduce(lambda total, buff: total + getattr(buff, attr_name, 0), modifiers, 0)


def merge_modifier(total: Modifier, hero: Hero, attr_name: string) -> Modifier:
    setattr(total, attr_name, getattr(total, attr_name, 0) + getattr(hero.talents, attr_name, 0))
    return total


def accumulate_talents_modifier(attr_name: string, is_attacker: bool, context: Context) -> float:
    player_id = context.get_actor_by_side(is_attacker).player_id
    partner_heroes = context.get_heroes_by_player_id(player_id)
    counter_heroes = context.get_heroes_by_counter_player_id(player_id)

    partner_talents = reduce(lambda total, hero: total + getattr(hero.talents, attr_name), partner_heroes, float(0))
    counter_talents = reduce(lambda total, hero: total + getattr(total, hero.talents, attr_name), counter_heroes,
                             float(0))
    return partner_talents + counter_talents


def get_formation_modifier(attr_name: string, is_attacker: bool, context: Context) -> float:
    hero_instance = context.get_actor_by_side(is_attacker)
    player_id = hero_instance.player_id
    current_formation: Formation = context.get_formation_by_player_id(player_id)
    basic_modifier_value = 0
    if current_formation.is_active:
        basic_modifier_value = getattr(current_formation.temp.basic_modifier, attr_name)
        formation_effects: List[FormationEffect] = current_formation.temp.effects
        for effect in formation_effects:
            multiplier = effect.requirement(is_attacker, context)
            if multiplier > 0:
                basic_modifier_value += getattr(effect.modifier, attr_name) * multiplier
    return basic_modifier_value


def get_battle_damage_modifier(is_attacker: bool, context: Context) -> float:
    action = context.get_action_by_side(is_attacker)
    is_in_battle = action.is_in_battle
    if is_in_battle:
        return get_formation_modifier(ModifierAttributes.battle_damage_percentage, is_attacker, context)
    else:
        return 0


def get_level1_modified_result(hero_instance: Hero, value_attr_name: str, basic: float) -> float:
    accumulated_stones_value_modifier = accumulate_attribute(hero_instance.stones.value, value_attr_name)
    accumulated_stones_percentage_modifier = accumulate_attribute(hero_instance.stones.percentage,
                                                                  value_attr_name + '_percentage')
    return basic * (1 + accumulated_stones_percentage_modifier) + accumulated_stones_value_modifier


def get_level2_modifier(hero_instance: Hero, is_attacker: bool, attr_name: str, context: Context) -> float:
    accumulated_buffs_modifier = accumulate_attribute(hero_instance.buffs, attr_name)
    accumulated_stones_effect_modifier = accumulate_attribute(hero_instance.stones.effect, attr_name)
    accumulated_talents_modifier = accumulate_talents_modifier(attr_name, is_attacker, context)
    accumulated_equipments_modifier = accumulate_attribute(hero_instance.equipments, attr_name)
    formation_modifier = get_formation_modifier(attr_name, is_attacker, context)
    accumulated_passives_modifier = accumulate_attribute(hero_instance.enabled_passives, attr_name)

    return accumulated_talents_modifier + accumulated_buffs_modifier + accumulated_stones_effect_modifier + accumulated_equipments_modifier + formation_modifier + accumulated_passives_modifier


def get_modifier(hero_instance: Hero, is_attacker: bool, context: Context, attr_name: str) -> float:
    accumulated_buffs_modifier = accumulate_attribute(hero_instance.buffs, attr_name)
    accumulated_talents_modifier = accumulate_talents_modifier(attr_name, is_attacker, context)
    accumulated_equipments_modifier = accumulate_attribute(hero_instance.equipments, attr_name)
    accumulated_passives_modifier = accumulate_attribute(hero_instance.enabled_passives, attr_name)

    return accumulated_talents_modifier + accumulated_buffs_modifier + accumulated_equipments_modifier + accumulated_passives_modifier
