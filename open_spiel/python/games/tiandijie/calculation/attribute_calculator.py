from open_spiel.python.games.tiandijie.primitives import Context, Action
from open_spiel.python.games.tiandijie.primitives.Action import ActionTypes
from open_spiel.python.games.tiandijie.calculation.ModifierAttributes import ModifierAttributes as ma
from open_spiel.python.games.tiandijie.calculation.Range import calculate_if_targe_in_diamond_range
from open_spiel.python.games.tiandijie.primitives.hero import Hero
from open_spiel.python.games.tiandijie.calculation.Modifier import accumulate_attribute, \
    get_battle_damage_modifier, get_level1_modified_result, get_level2_modifier
from open_spiel.python.games.tiandijie.primitives.skill.SkillTemp import SkillTargetTypes, is_normal_attack, SkillTemp

LIEXING_DAMAGE_REDUCTION = 4
LIEXING_DAMAGE_INCREASE = 4


# TODO Shenbin calculation is not included

def get_element_multiplier(is_attacker: bool, context: Context) -> float:
    hero_instance = context.get_actor_by_side(is_attacker)
    attr_name = ma.element_attacker_multiplier if is_attacker else ma.element_defender_multiplier
    return get_level2_modifier(hero_instance, is_attacker, attr_name, context)


def get_penetration_multiplier(hero_instance: Hero, is_attacker: bool, is_magic: bool, context: Context):
    attr_name = ma.magic_penetration_percentage if is_magic else ma.penetration_percentage
    return get_level2_modifier(hero_instance, is_attacker, attr_name, context)


def get_defense_with_penetration(attacker_instance: Hero, defender_instance: Hero, is_magic: bool,
                                 context: Context) -> float:
    penetration = get_penetration_multiplier(attacker_instance, True, is_magic, context)
    # calculate buffs
    basic_defense = get_defense(defender_instance, False, is_magic, context)
    return basic_defense * (1 - penetration)


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


def get_max_life(hero_instance: Hero, is_attacker: bool, context: Context) -> float:
    life_attribute = hero_instance.initial_attribute.life
    basic_life = get_level1_modified_result(hero_instance, ma.life, life_attribute)
    return basic_life * (1 + get_level2_modifier(hero_instance, is_attacker, ma.life_percentage, context))


def get_defense(hero_instance: Hero, is_attacker: bool, is_magic: bool, context: Context) -> float:
    # calculate buffs
    attr_name = ma.magic_defense if is_magic else ma.defense
    defense_attribute = hero_instance.initial_attributes.defense if is_magic else hero_instance.initial_attribute.magic_defense

    basic_defense = get_level1_modified_result(hero_instance, attr_name, defense_attribute)
    return basic_defense * (1 + get_level2_modifier(hero_instance, is_attacker, attr_name, context))


def get_attack(hero_instance: Hero, is_attacker: bool, context: Context) -> float:
    action = context.get_action_by_side(is_attacker)
    is_magic = action.skill.is_magic
    # calculate buffs
    attr_name = 'magic_attack' if is_magic else 'attack'
    attack_attribute = hero_instance.initial_attribute.attack if is_magic else hero_instance.initial_attribute.magic_attack
    basic_attack = get_level1_modified_result(hero_instance, attr_name, attack_attribute)
    return basic_attack * (
            1 + get_level2_modifier(hero_instance, True, attr_name, context))

# TODO
def get_action_type_damage_modifier(is_attacker: bool, context: Context) -> float:
    current_action = context.get_last_action()
    action_type = current_action.type
    actor = context.get_actor_by_side(is_attacker)
    action_type_modifier = 0
    if action_type == ActionTypes.SKILL_ATTACK:
        action_type_modifier += get_level2_modifier(actor, is_attacker, ma.skill_damage_percentage, context)
        skill_target_type = context.get_last_action().skill.target_type
        if skill_target_type == SkillTargetTypes.ENEMY_SINGLE:
            action_type_modifier += get_level2_modifier(actor, is_attacker, ma.single_target_skill_damage_percentage, context)
        elif skill_target_type == SkillTargetTypes.ENEMY_RANGE:
            action_type_modifier += get_level2_modifier(actor, is_attacker, ma.multi_target_skill_damage_percentage, context)
    elif action_type == ActionTypes.NORMAL_ATTACK:
        action_type_modifier += get_level2_modifier(actor, is_attacker, ma.normal_attack_damage_percentage, context)

    if current_action.is_in_battle:
        action_type_modifier += get_level2_modifier(actor, is_attacker, ma.battle_damage_percentage, context)
    return action_type_modifier


def get_damage_modifier(attacker_instance: Hero, is_attacker: bool, is_magic: bool, context: Context, skill: SkillTemp) -> float:
    attr_name = ma.magic_damage_percentage if is_magic else ma.damage_percentage
    accumulated_skill_damage_modifier = skill.damage_multiplier
    accumulated_passive_damage_modifier = accumulate_attribute(attacker_instance.temp.passives, attr_name)
    accumulated_stones_percentage_damage_modifier = accumulate_attribute(attacker_instance.stones.percentage,
                                                                         attr_name)

    level2_damage_modifier = 1 + (
            get_level2_modifier(attacker_instance, is_attacker, attr_name, context)
            + accumulated_skill_damage_modifier
            + accumulated_passive_damage_modifier
            + get_action_type_damage_modifier(is_attacker, context)
            + get_battle_damage_modifier(is_attacker, context)) / 100

    # B-type damage increase (Additive)
    level1_damage_modifier = 1 + (LIEXING_DAMAGE_INCREASE + accumulated_stones_percentage_damage_modifier) / 100
    return level1_damage_modifier * level2_damage_modifier


def get_damage_reduction_modifier(defense_instance: Hero, is_attacker: bool, is_magic: bool, context: Context) -> float:
    attr_name = ma.magic_damage_reduction_percentage if is_magic else ma.damage_reduction_percentage
    accumulated_passives_damage_reduction_modifier = accumulate_attribute(defense_instance.temp.passives,
                                                                          attr_name)
    accumulated_stones_damage_reduction_percentage_modifier = accumulate_attribute(
        defense_instance.stones.percentage, attr_name)
    formation_damage_reduction_modifier = context.formation.magic_damage_reduction_percentage if is_magic else context.formation.damage_reduction_percentage

    # A-type damage increase (Additive)
    a_type_damage_reduction = 1 - (
            get_level2_modifier(defense_instance, is_attacker, attr_name, context)
            + accumulated_passives_damage_reduction_modifier
            + formation_damage_reduction_modifier) / 100

    # B-type damage increase (Additive)
    b_type_damage_reduction = 1 - (
            LIEXING_DAMAGE_REDUCTION + accumulated_stones_damage_reduction_percentage_modifier) / 100
    return a_type_damage_reduction * b_type_damage_reduction


def get_critical_hit_probability(hero_instance: Hero, is_attacker: bool, context: Context) -> float:
    critical_stones_percentage_modifier = accumulate_attribute(hero_instance.stones.percentage,
                                                               ma.critical_percentage)

    luck_attribute = hero_instance.initial_attribute.luck
    total_luck = luck_attribute * (
            1 + get_level2_modifier(hero_instance, is_attacker, ma.luck, context))
    level2_critical_modifier = get_level2_modifier(hero_instance, is_attacker, ma.critical_percentage, context)
    total_critical = total_luck / 10 + level2_critical_modifier + critical_stones_percentage_modifier
    return total_critical / 100


def get_critical_hit_resistance(hero_instance: Hero, is_attacker: bool, context: Context) -> float:
    # Calculate buffs
    level_2_hit_resistance = get_level2_modifier(hero_instance, is_attacker, ma.critical_percentage_reduction, context)
    critical_stones_percentage_modifier = accumulate_attribute(hero_instance.stones.percentage,
                                                               ma.critical_percentage_reduction)

    return 1 - (
            level_2_hit_resistance + critical_stones_percentage_modifier) / 100


def get_critical_damage_modifier(hero_instance: Hero, is_attacker: bool, context: Context) -> float:
    return 1 + get_level2_modifier(hero_instance, is_attacker, ma.critical_damage_percentage, context) / 100


def get_critical_damage_reduction_modifier(hero_instance: Hero, is_attacker: bool, context: Context) -> float:
    return 1 - get_level2_modifier(hero_instance, is_attacker, ma.critical_damage_reduction_percentage, context) / 100


def get_fixed_damage_reduction_modifier(hero_instance: Hero, is_attacker: bool, context: Context) -> float:
    accumulated_passives_damage_reduction_modifier = accumulate_attribute(hero_instance.temp.passives,
                                                                          ma.fixed_damage_reduction_percentage)
    return 1 - (get_level2_modifier(hero_instance, is_attacker, ma.fixed_damage_reduction_percentage, context)
                - accumulated_passives_damage_reduction_modifier) / 100
