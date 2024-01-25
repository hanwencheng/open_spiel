from open_spiel.python.games.tiandijie.primitives import Context
from open_spiel.python.games.tiandijie.primitives.hero import Hero
from open_spiel.python.games.tiandijie.primitives.skill import Skill
from open_spiel.python.games.tiandijie.primitives.Modifier import accumulate_attribute, accumulate_talents_modifier

LIEXING_DAMAGE_REDUCTION = 4
LIEXING_DAMAGE_INCREASE = 4


# TODO Shenbin calculation is not included

def get_attacker_penetration(attacker_instance, is_magic: bool):
    return 10


def get_level1_modified_result(hero_instance: Hero, value_attr_name: str, basic: float) -> float:
    accumulated_stones_value_modifier = accumulate_attribute(hero_instance.stones.value, value_attr_name)
    accumulated_stones_percentage_modifier = accumulate_attribute(hero_instance.stones.percentage, value_attr_name + '_percentage')
    return basic * (1 + accumulated_stones_percentage_modifier) + accumulated_stones_value_modifier


def get_level2_modifier(hero_instance: Hero, context: Context, attr_name: str) -> float:
    accumulated_buffs_modifier = accumulate_attribute(hero_instance.buffs, attr_name)
    accumulated_stones_effect_modifier = accumulate_attribute(hero_instance.stones.effect, attr_name)
    accumulated_talents_modifier = accumulate_talents_modifier(context, attr_name)
    accumulated_equipments_modifier = accumulate_attribute(hero_instance.equipments, attr_name)
    formation_modifier = getattr(context.formation, attr_name)

    return accumulated_talents_modifier + accumulated_buffs_modifier + accumulated_stones_effect_modifier + accumulated_equipments_modifier + formation_modifier


def get_max_life(hero_instance: Hero, context: Context) -> float:
    life_attribute = hero_instance.current_attributes.life
    basic_life = get_level1_modified_result(hero_instance, 'life', life_attribute)
    return basic_life * (1 + get_level2_modifier(hero_instance, context, 'life_percentage'))


def get_defense(defender_instance: Hero, is_magic: bool, context: Context) -> float:
    # calculate buffs
    attr_name = 'magic_defense' if is_magic else 'defense'
    defense_attribute = defender_instance.current_attributes.defense if is_magic else defender_instance.current_attributes.magic_defense

    basic_defense = get_level1_modified_result(defender_instance, attr_name, defense_attribute)
    return basic_defense * (1 + get_level2_modifier(defender_instance, context, attr_name))


def get_defense_with_penetration(attacker_instance: Hero, defender_instance: Hero, is_magic: bool,
                                 context: Context) -> float:
    penetration = get_attacker_penetration(attacker_instance, is_magic)
    # calculate buffs
    basic_defense = get_defense(defender_instance, is_magic, context)
    return basic_defense * (1 - penetration)


def get_attack(attacker_instance: Hero, is_magic: bool, context: Context) -> float:
    # calculate buffs
    attr_name = 'magic_attack' if is_magic else 'attack'
    attack_attribute = attacker_instance.current_attributes.attack if is_magic else attacker_instance.current_attributes.magic_attack
    basic_attack = get_level1_modified_result(attacker_instance, attr_name, attack_attribute)
    return basic_attack * (
            1 + get_level2_modifier(attacker_instance, context, attr_name))


def get_damage_modifier(attacker_instance: Hero, is_magic: bool, context: Context, skill: Skill) -> float:
    attr_name = 'magic_damage_percentage' if is_magic else 'damage_percentage'
    accumulated_skill_damage_modifier = skill.damage_multiplier
    accumulated_passive_damage_modifier = accumulate_attribute(attacker_instance.temp.passives, attr_name)
    accumulated_stones_percentage_damage_modifier = accumulate_attribute(attacker_instance.stones.percentage,
                                                                         attr_name)
    formation_damage_modifier = context.formation.magic_damage_percentage if is_magic else context.formation.damage_percentage

    # A-type damage increase (Additive)
    level2_damage_modifier = 1 + (
            get_level2_modifier(attacker_instance, context, attr_name)
            + accumulated_skill_damage_modifier
            + accumulated_passive_damage_modifier
            + formation_damage_modifier) / 100

    # B-type damage increase (Additive)
    level1_damage_modifier = 1 + (LIEXING_DAMAGE_INCREASE + accumulated_stones_percentage_damage_modifier) / 100
    return level1_damage_modifier * level2_damage_modifier


def get_damage_reduction_modifier(defense_instance: Hero, is_magic: bool, context: Context) -> float:
    attr_name = 'magic_damage_reduction' if is_magic else 'damage_reduction'
    accumulated_passives_damage_reduction_modifier = accumulate_attribute(defense_instance.temp.passives,
                                                                          attr_name)
    accumulated_stones_damage_reduction_percentage_modifier = accumulate_attribute(
        defense_instance.stones.percentage, attr_name)
    formation_damage_reduction_modifier = context.formation.magic_damage_reduction_percentage if is_magic else context.formation.damage_reduction_percentage

    # A-type damage increase (Additive)
    a_type_damage_reduction = 1 - (
            get_level2_modifier(defense_instance, context, attr_name)
            + accumulated_passives_damage_reduction_modifier
            + formation_damage_reduction_modifier) / 100

    # B-type damage increase (Additive)
    b_type_damage_reduction = 1 - (
            LIEXING_DAMAGE_REDUCTION + accumulated_stones_damage_reduction_percentage_modifier) / 100
    return a_type_damage_reduction * b_type_damage_reduction


def get_attacker_hit_probability1(attacker_instance: Hero, context: Context) -> float:
    critical_stones_percentage_modifier = accumulate_attribute(attacker_instance.stones.percentage, 'critical')

    luck_attribute = attacker_instance.current_attributes.luck
    total_luck = luck_attribute * (1 + get_level2_modifier(attacker_instance, context, 'luck'))
    total_critical = total_luck / 10 + get_level2_modifier(attacker_instance, context, 'critical') + critical_stones_percentage_modifier
    return total_critical / 100


def get_attacker_hit_probability(attacker_instance: Hero, context: Context) -> float:
    critical_stones_percentage_modifier = accumulate_attribute(attacker_instance.stones.percentage, 'critical')

    luck_attribute = attacker_instance.current_attributes.luck
    total_luck = luck_attribute * (
            1 + get_level2_modifier(attacker_instance, context, 'luck'))
    level2_critical_modifier = get_level2_modifier(attacker_instance, context, 'critical')
    total_critical = total_luck / 10 + level2_critical_modifier + critical_stones_percentage_modifier
    return total_critical / 100


def get_defender_hit_resistance(defender_instance: Hero, context: Context) -> float:
    # Calculate buffs
    level_2_hit_resistance = get_level2_modifier(defender_instance, context, 'critical_reduction')
    critical_stones_percentage_modifier = accumulate_attribute(defender_instance.stones.percentage,
                                                               'critical_reduction')

    return 1 - (
            level_2_hit_resistance + critical_stones_percentage_modifier) / 100


def get_critical_damage_modifier(attacker_instance: Hero, context: Context) -> float:
    return 1 + get_level2_modifier(attacker_instance, context,'critical_damage_percentage') / 100


def get_critical_damage_reduction_modifier(defender_instance: Hero, context: Context) -> float:
    return 1 - get_level2_modifier(defender_instance, context, 'critical_damage_reduction_percentage') / 100


def get_fixed_damage_reduction_modifier(defender_instance: Hero, context: Context) -> float:
    accumulated_passives_damage_reduction_modifier = accumulate_attribute(defender_instance.temp.passives,
                                                                          'fixed_damage_reduction_percentage')
    return 1 - (get_level2_modifier(defender_instance, context, 'fixed_damage_reduction_percentage')
                - accumulated_passives_damage_reduction_modifier) / 100
