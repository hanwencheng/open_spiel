from random import random

from open_spiel.python.games.tiandijie.primitives.Action import Action
from open_spiel.python.games.tiandijie.primitives.hero.Element import get_elemental_multiplier
from open_spiel.python.games.tiandijie.calculation.attribute_calculator import *
from open_spiel.python.games.tiandijie.primitives import Context
from open_spiel.python.games.tiandijie.primitives.hero import HeroTemp, Hero

CRIT_MULTIPLIER = 1.3
LIEXING_DAMAGE_REDUCTION = 4
LIEXING_DAMAGE_INCREASE = 4


def apply_damage(context: Context):
    action = context.get_last_action()
    targets = context.get_last_action().targets
    for target in targets:
        calculate_damage(action.actor, target, action, context)


def apply_counterattack_damage(context: Context):
    pass


def calculate_damage(attacker_instance: Hero, defender_instance: Hero, action: Action, context):
    is_magic = action.is_magic
    skill = action.skill
    attacker_elemental_multiplier = get_elemental_multiplier(attacker_instance.temp.element, defender_instance.temp.element, True) + get_element_advantage_multiplier(attacker_instance.temp.element, defender_instance.temp.element)
    defender_elemental_multiplier = get_elemental_multiplier(attacker_instance.temp.element, defender_instance.temp.element,
                                                             False) + get_element_disadvantage_multiplier(defender_instance.temp.element, attacker_instance.temp.element)

    # Calculating attack-defense difference
    attack_defense_difference = (
            get_attack(attacker_instance, is_magic, context) * attacker_elemental_multiplier
            - get_defense_with_penetration(attacker_instance, defender_instance, is_magic,
                                           context) * defender_elemental_multiplier)

    # Calculating base damage
    actual_damage = (attack_defense_difference
                     * skill.damage_multiplier
                     * get_damage_modifier(attacker_instance, is_magic, context, skill)
                     * get_damage_reduction_modifier(defender_instance, is_magic, context))

    critical_probability = (get_attacker_hit_probability(attacker_instance, context)
                            - get_defender_hit_resistance(defender_instance, context))

    critical_damage_multiplier = (CRIT_MULTIPLIER
                                  * get_critical_damage_modifier(attacker_instance, context)
                                  * get_critical_damage_reduction_modifier(defender_instance, context))

    if random() < critical_probability:
        # Critical hit occurs
        defender_instance.take_harm(actual_damage * critical_damage_multiplier)
    else:
        # No critical hit
        defender_instance.take_harm(actual_damage)


def calculate_fix_damage(damage, defender_instance: Hero, context: Context):
    defender_fix_damage_reduction = get_fixed_damage_reduction_modifier(defender_instance, context)
    defender_instance.take_harm(damage * defender_fix_damage_reduction)


def calculate_magic_damage(damage: float, defender_instance: Hero, context: Context):
    actual_damage = (damage
                     * get_damage_reduction_modifier(defender_instance, True, context))
    defender_instance.take_harm(actual_damage)


def calculate_physical_damage(damage: float, defender_instance: Hero, context: Context):
    actual_damage = (damage
                     * get_damage_reduction_modifier(defender_instance, False, context))
    defender_instance.take_harm(actual_damage)
