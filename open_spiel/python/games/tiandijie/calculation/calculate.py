from open_spiel.python.games.tiandijie.primitives import Context
from open_spiel.python.games.tiandijie.primitives.Action import ActionTypes
from open_spiel.python.games.tiandijie.primitives.ModifierAttributes import ModifierAttributes as ma
from open_spiel.python.games.tiandijie.primitives.Range import calculate_if_targe_in_diamond_range
from open_spiel.python.games.tiandijie.primitives.hero import Hero
from open_spiel.python.games.tiandijie.primitives.skill import Skill
from open_spiel.python.games.tiandijie.primitives.Modifier import accumulate_attribute, accumulate_talents_modifier, \
    get_battle_damage_modifier
from open_spiel.python.games.tiandijie.primitives.skill.Skill import SkillTargetTypes

LIEXING_DAMAGE_REDUCTION = 4
LIEXING_DAMAGE_INCREASE = 4


# TODO Shenbin calculation is not included

def get_attacker_penetration(attacker_instance, is_magic: bool):
    return 10

# TODO, calculate 先攻和反击上限，范围加成
def get_counter_attack_range(hero_instance: Hero, context: Context):
    counter_attack_range = hero_instance.temp.range
    return counter_attack_range


def check_in_battle(context: Context) -> bool:
    current_action = context.get_last_action()
    target = current_action.targets[0]
    if len(target) != 1:
        return False
    actor = current_action.actor
    if calculate_if_targe_in_diamond_range(actor, target, get_counter_attack_range(target, context)):
        return True
    else:
        return False

def get_level1_modified_result(hero_instance: Hero, value_attr_name: str, basic: float) -> float:
    accumulated_stones_value_modifier = accumulate_attribute(hero_instance.stones.value, value_attr_name)
    accumulated_stones_percentage_modifier = accumulate_attribute(hero_instance.stones.percentage,
                                                                  value_attr_name + '_percentage')
    return basic * (1 + accumulated_stones_percentage_modifier) + accumulated_stones_value_modifier


def get_level2_modifier(hero_instance: Hero, context: Context, attr_name: str) -> float:
    accumulated_buffs_modifier = accumulate_attribute(hero_instance.buffs, attr_name)
    accumulated_stones_effect_modifier = accumulate_attribute(hero_instance.stones.effect, attr_name)
    accumulated_talents_modifier = accumulate_talents_modifier(context, attr_name)
    accumulated_equipments_modifier = accumulate_attribute(hero_instance.equipments, attr_name)
    formation_modifier = getattr(context.formation, attr_name)

    return accumulated_talents_modifier + accumulated_buffs_modifier + accumulated_stones_effect_modifier + accumulated_equipments_modifier + formation_modifier


def get_max_life(hero_instance: Hero, context: Context) -> float:
    life_attribute = hero_instance.initial_attribute.life
    basic_life = get_level1_modified_result(hero_instance, ma.life, life_attribute)
    return basic_life * (1 + get_level2_modifier(hero_instance, context, ma.life_percentage))


def get_defense(defender_instance: Hero, is_magic: bool, context: Context) -> float:
    # calculate buffs
    attr_name = ma.magic_defense if is_magic else ma.defense
    defense_attribute = defender_instance.initial_attributes.defense if is_magic else defender_instance.initial_attribute.magic_defense

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
    attack_attribute = attacker_instance.initial_attribute.attack if is_magic else attacker_instance.initial_attribute.magic_attack
    basic_attack = get_level1_modified_result(attacker_instance, attr_name, attack_attribute)
    return basic_attack * (
            1 + get_level2_modifier(attacker_instance, context, attr_name))

def get_action_type_damage_modifier(context: Context) -> float:
    action_type = context.get_last_action().type
    actor = context.get_last_action().actor
    action_type_modifier = 0
    if action_type == ActionTypes.SKILL:
        action_type_modifier += get_level2_modifier(actor, context, ma.skill_damage_percentage)
        skill_target_type = context.get_last_action().skill.target_type
        if skill_target_type == SkillTargetTypes.ENEMY_SINGLE:
            action_type_modifier += get_level2_modifier(actor, context, ma.single_target_skill_damage_percentage)
        elif skill_target_type == SkillTargetTypes.ENEMY_RANGE:
            action_type_modifier += get_level2_modifier(actor, context, ma.multi_target_skill_damage_percentage)
    elif action_type == ActionTypes.ATTACK:
        action_type_modifier += get_level2_modifier(actor, context, ma.normal_attack_damage_percentage)

    if context.get_last_action().is_in_battle:
        action_type_modifier += get_level2_modifier(actor, context, ma.battle_damage_percentage)
    return action_type_modifier


def get_damage_modifier(attacker_instance: Hero, is_magic: bool, context: Context, skill: Skill) -> float:

    attr_name = ma.magic_damage_percentage if is_magic else ma.damage_percentage
    accumulated_skill_damage_modifier = skill.damage_multiplier
    accumulated_passive_damage_modifier = accumulate_attribute(attacker_instance.temp.passives, attr_name)
    accumulated_stones_percentage_damage_modifier = accumulate_attribute(attacker_instance.stones.percentage,
                                                                         attr_name)


    action_type_damage_modifier = get_action_type_damage_modifier(context)

    level2_damage_modifier = 1 + (
            get_level2_modifier(attacker_instance, context, attr_name)
            + accumulated_skill_damage_modifier
            + accumulated_passive_damage_modifier
            + get_action_type_damage_modifier(context)
            + get_battle_damage_modifier(context)) / 100

    # B-type damage increase (Additive)
    level1_damage_modifier = 1 + (LIEXING_DAMAGE_INCREASE + accumulated_stones_percentage_damage_modifier) / 100
    return level1_damage_modifier * level2_damage_modifier


def get_damage_reduction_modifier(defense_instance: Hero, is_magic: bool, context: Context) -> float:
    attr_name = ma.magic_damage_reduction_percentage if is_magic else ma.damage_reduction_percentage
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
    critical_stones_percentage_modifier = accumulate_attribute(attacker_instance.stones.percentage, ma.critical)

    luck_attribute = attacker_instance.initial_attribute.luck
    total_luck = luck_attribute * (1 + get_level2_modifier(attacker_instance, context, ma.luck))
    total_critical = total_luck / 10 + get_level2_modifier(attacker_instance, context,
                                                           ma.critical) + critical_stones_percentage_modifier
    return total_critical / 100


def get_attacker_hit_probability(attacker_instance: Hero, context: Context) -> float:
    critical_stones_percentage_modifier = accumulate_attribute(attacker_instance.stones.percentage, ma.critical)

    luck_attribute = attacker_instance.initial_attribute.luck
    total_luck = luck_attribute * (
            1 + get_level2_modifier(attacker_instance, context, ma.luck))
    level2_critical_modifier = get_level2_modifier(attacker_instance, context, ma.critical)
    total_critical = total_luck / 10 + level2_critical_modifier + critical_stones_percentage_modifier
    return total_critical / 100


def get_defender_hit_resistance(defender_instance: Hero, context: Context) -> float:
    # Calculate buffs
    level_2_hit_resistance = get_level2_modifier(defender_instance, context, ma.critical_reduction)
    critical_stones_percentage_modifier = accumulate_attribute(defender_instance.stones.percentage,
                                                               ma.critical_reduction)

    return 1 - (
            level_2_hit_resistance + critical_stones_percentage_modifier) / 100


def get_critical_damage_modifier(attacker_instance: Hero, context: Context) -> float:
    return 1 + get_level2_modifier(attacker_instance, context, ma.critical_damage_percentage) / 100


def get_critical_damage_reduction_modifier(defender_instance: Hero, context: Context) -> float:
    return 1 - get_level2_modifier(defender_instance, context, ma.critical_damage_reduction_percentage) / 100


def get_fixed_damage_reduction_modifier(defender_instance: Hero, context: Context) -> float:
    accumulated_passives_damage_reduction_modifier = accumulate_attribute(defender_instance.temp.passives,
                                                                          ma.fixed_damage_reduction_percentage)
    return 1 - (get_level2_modifier(defender_instance, context, ma.fixed_damage_reduction_percentage)
                - accumulated_passives_damage_reduction_modifier) / 100
