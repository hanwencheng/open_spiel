from random import random

from open_spiel.python.games.Element import get_elemental_multiplier
from open_spiel.python.games.tiandijie.types.Context import Context
from open_spiel.python.games.tiandijie.types.Hero import Hero
from open_spiel.python.games.tiandijie.types.Modifier import accumulate_defense_modifier, accumulate_attack_modifier, \
    accumulate_damage_modifier, accumulate_damage_reduction_modifier, accumulate_attribute
from open_spiel.python.games.tiandijie.types.Skill import Skill

CRIT_MULTIPLIER = 1.3
LIEXING_DAMAGE_REDUCTION = 4
LIEXING_DAMAGE_INCREASE = 4


def get_attacker_penetration(attacker_instance, is_magic: bool):
    return 10


def get_defender_defense(attacker_instance, defender_instance, is_magic, context):
    penetration = get_attacker_penetration(attacker_instance, is_magic)
    # calculate buffs
    accumulated_buffs_modifier = accumulate_defense_modifier(defender_instance.buffs, is_magic)
    accumulated_stones_value_modifier = accumulate_defense_modifier(defender_instance.stones.value, is_magic)
    accumulated_stones_effect_modifier = accumulate_defense_modifier(defender_instance.stones.effect, is_magic)
    accumulated_stones_percentage_modifier = accumulate_defense_modifier(defender_instance.stones.percentage, is_magic)
    accumulated_talents_modifier = accumulate_defense_modifier(context.heroes.talents, is_magic)
    accumulated_equipments_modifier = accumulate_defense_modifier(defender_instance.equipments, is_magic)

    defense_attribute = defender_instance.current_attributes.defense if is_magic else defender_instance.current_attributes.magic_defense
    basic_defense = defense_attribute * (1 + accumulated_stones_percentage_modifier) + accumulated_stones_value_modifier
    return basic_defense * ((
                                    1 + accumulated_talents_modifier + accumulated_buffs_modifier + accumulated_stones_effect_modifier + accumulated_equipments_modifier) - penetration)


def get_attacker_attack_value(attacker_instance, is_magic, context):
    # calculate buffs
    accumulated_buffs_modifier = accumulate_attack_modifier(attacker_instance.buffs, is_magic)
    accumulated_stones_value_modifier = accumulate_attack_modifier(attacker_instance.stones.value, is_magic)
    accumulated_stones_effect_modifier = accumulate_attack_modifier(attacker_instance.stones.effect, is_magic)
    accumulated_stones_percentage_modifier = accumulate_attack_modifier(attacker_instance.stones.percentage, is_magic)
    accumulated_talents_modifier = accumulate_attack_modifier(context.heroes.talents, is_magic)
    accumulated_equipments_modifier = accumulate_attack_modifier(attacker_instance.equipments, is_magic)

    attack_attribute = attacker_instance.current_attributes.attack if is_magic else attacker_instance.current_attributes.magic_attack
    basic_attack = attack_attribute * (1 + accumulated_stones_percentage_modifier) + accumulated_stones_value_modifier
    return basic_attack * (
            1 + accumulated_talents_modifier + accumulated_buffs_modifier + accumulated_stones_effect_modifier + accumulated_equipments_modifier)


def get_damage_modifier(attacker_instance: Hero, is_magic: bool, context: Context, skill: Skill):
    accumulated_talents_damage_modifier = accumulate_damage_modifier(context.heroes.talents, is_magic)
    accumulated_skill_damage_modifier = skill.damage_multiplier
    accumulated_passive_damage_modifier = accumulate_damage_modifier(attacker_instance.passives, is_magic)
    accumulated_buffs_damage_modifier = accumulate_damage_modifier(attacker_instance.buffs, is_magic)
    accumulated_equipment_damage_modifier = accumulate_damage_modifier(attacker_instance.equipments, is_magic)
    accumulated_stones_percentage_damage_modifier = accumulate_damage_modifier(attacker_instance.stones.percentage,
                                                                               is_magic)
    formation_damage_modifier = context.formation.magic_damage_percentage if is_magic else context.formation.damage_percentage
    accumulated_stones_effect_damage_modifier = accumulate_damage_modifier(attacker_instance.stones.effect, is_magic)

    # A-type damage increase (Additive)
    a_type_damage_increase = 1 + (
            accumulated_talents_damage_modifier
            + accumulated_skill_damage_modifier
            + accumulated_buffs_damage_modifier
            + accumulated_equipment_damage_modifier
            + accumulated_stones_effect_damage_modifier
            + accumulated_passive_damage_modifier
            + formation_damage_modifier) / 100

    # B-type damage increase (Additive)
    b_type_damage_increase = 1 + (LIEXING_DAMAGE_INCREASE + accumulated_stones_percentage_damage_modifier) / 100
    return a_type_damage_increase * b_type_damage_increase


def get_damage_reduction_modifier(defense_instance: Hero, is_magic: bool, context: Context):
    accumulated_talents_damage_reduction_modifier = accumulate_damage_reduction_modifier(context.heroes.talents,
                                                                                         is_magic)
    accumulated_passives_damage_reduction_modifier = accumulate_damage_reduction_modifier(defense_instance.passives, is_magic)
    accumulated_buffs_damage_reduction_modifier = accumulate_damage_reduction_modifier(defense_instance.buffs, is_magic)
    accumulated_equipment_damage_reduction_modifier = accumulate_damage_reduction_modifier(defense_instance.equipments,
                                                                                           is_magic)
    accumulated_stones_damage_reduction_percentage_modifier = accumulate_damage_reduction_modifier(
        defense_instance.stones.percentage, is_magic)
    formation_damage_reduction_modifier = context.formation.magic_damage_reduction_percentage if is_magic else context.formation.damage_reduction_percentage
    accumulated_stones_effect_damage_reduction_modifier = accumulate_damage_reduction_modifier(
        defense_instance.stones.effect, is_magic)

    # A-type damage increase (Additive)
    a_type_damage_reduction = 1 - (
            accumulated_talents_damage_reduction_modifier
            + accumulated_passives_damage_reduction_modifier
            + accumulated_buffs_damage_reduction_modifier
            + accumulated_equipment_damage_reduction_modifier
            + accumulated_stones_effect_damage_reduction_modifier
            + formation_damage_reduction_modifier) / 100

    # B-type damage increase (Additive)
    b_type_damage_reduction = 1 - (
                LIEXING_DAMAGE_REDUCTION + accumulated_stones_damage_reduction_percentage_modifier) / 100
    return a_type_damage_reduction * b_type_damage_reduction


def get_attacker_hit_probability(attacker_instance, context):
    # calculate buffs
    luck_accumulated_buffs_modifier = accumulate_attribute(attacker_instance.buffs, 'luck')
    luck_stones_effect_modifier = accumulate_attribute(attacker_instance.stones.effect, 'luck')
    luck_talents_modifier = accumulate_attribute(context.talents, 'luck')

    critical_equipments_modifier = accumulate_attribute(attacker_instance.equipments, 'critical')
    critical_buffs_modifier = accumulate_attribute(attacker_instance.buffs, 'critical')
    critical_stones_effect_modifier = accumulate_attribute(attacker_instance.stones.effect, 'critical')
    critical_stones_percentage_modifier = accumulate_attribute(attacker_instance.stones.percentage, 'critical')
    critical_talents_modifier = accumulate_attribute(context.talents, 'critical')
    critical_formation_modifier = context.formation.critical

    luck_attribute = attacker_instance.current_attributes.luck
    total_luck = luck_attribute * (
                1 + luck_accumulated_buffs_modifier + luck_stones_effect_modifier + luck_talents_modifier)
    total_critical = total_luck / 10 + critical_equipments_modifier + critical_buffs_modifier + critical_stones_effect_modifier + critical_talents_modifier + critical_formation_modifier + critical_stones_percentage_modifier
    return total_critical / 100


def get_defender_hit_resistance(defender_instance, context):
    # Calculate buffs
    accumulated_buffs_modifier = accumulate_attribute(defender_instance.buffs, 'critical_reduction')
    accumulated_stones_effect_modifier = accumulate_attribute(defender_instance.stones.effect, 'critical_reduction')
    accumulated_talents_modifier = accumulate_attribute(context.talents, 'critical_reduction')
    accumulated_equipments_modifier = accumulate_attribute(defender_instance.equipments, 'critical_reduction')
    critical_stones_percentage_modifier = accumulate_attribute(defender_instance.stones.percentage,
                                                               'critical_reduction')
    formation_modifier = context.formation.critical_reduction

    return 1 - (
                accumulated_buffs_modifier - accumulated_stones_effect_modifier - accumulated_talents_modifier - accumulated_equipments_modifier - formation_modifier - critical_stones_percentage_modifier) / 100


def get_critical_damage_modifier(attacker_instance, context):
    accumulated_equipments_modifier = accumulate_attribute(attacker_instance.equipments, 'critical_damage_percentage')
    accumulated_buffs_modifier = accumulate_attribute(attacker_instance.buffs, 'critical_damage_percentage')
    accumulated_stones_effect_modifier = accumulate_attribute(attacker_instance.stones.effect,
                                                              'critical_damage_percentage')
    accumulated_talents_modifier = accumulate_attribute(context.talents, 'critical_damage_percentage')
    formation_modifier = context.formation.critical

    return 1 + (
                accumulated_equipments_modifier + accumulated_buffs_modifier + accumulated_stones_effect_modifier + accumulated_talents_modifier + formation_modifier) / 100


def get_critical_damage_reduction_modifier(defender_instance, context):
    accumulated_equipments_modifier = accumulate_attribute(defender_instance.equipments,
                                                           'critical_damage_reduction_percentage')
    accumulated_buffs_modifier = accumulate_attribute(defender_instance.buffs, 'critical_damage_reduction_percentage')
    accumulated_stones_effect_modifier = accumulate_attribute(defender_instance.stones.effect,
                                                              'critical_damage_reduction_percentage')
    accumulated_talents_modifier = accumulate_attribute(context.talents, 'critical_damage_reduction_percentage')
    formation_modifier = context.formation.critical
    return 1 - (
                accumulated_equipments_modifier - accumulated_buffs_modifier - accumulated_stones_effect_modifier
                - accumulated_talents_modifier - formation_modifier) / 100


def calculate_damage(attacker_instance: Hero, defender_instance: Hero, is_magic: bool, context, skill: Skill):
    attacker_elemental_multiplier = get_elemental_multiplier(attacker_instance.element, defender_instance.element, True)
    defender_elemental_multiplier = get_elemental_multiplier(attacker_instance.element, defender_instance.element,
                                                             False)

    # Calculating attack-defense difference
    attack_defense_difference = (
            get_attacker_attack_value(attacker_instance, is_magic, context) * attacker_elemental_multiplier
            - get_defender_defense(attacker_instance, defender_instance, is_magic, context) * defender_elemental_multiplier)

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
        return actual_damage * critical_damage_multiplier
    else:
        # No critical hit
        return actual_damage
