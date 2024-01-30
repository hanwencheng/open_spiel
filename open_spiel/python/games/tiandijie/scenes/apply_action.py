from functools import partial
from typing import Callable

from open_spiel.python.games.tiandijie.calculation.Modifier import get_modifier
from open_spiel.python.games.tiandijie.calculation.calculate_damage import calculate_damage, apply_damage, \
    apply_counterattack_damage
from open_spiel.python.games.tiandijie.primitives.Action import Action, ActionTypes
from open_spiel.python.games.tiandijie.primitives.Context import Context
from open_spiel.python.games.tiandijie.primitives.event.Event import event_listener_calculator, EventTypes
from open_spiel.python.games.tiandijie.primitives.hero.Hero import Hero
from open_spiel.python.games.tiandijie.calculation.ModifierAttributes import ModifierAttributes as ma
from open_spiel.python.games.tiandijie.primitives.skill.Skill import SkillTargetTypes


# move actor to the desired position
def apply_move(action: Action):
    actor = action.actor
    actor.update_position(action)


action_event: dict[ActionTypes, tuple[EventTypes, EventTypes]] = {
    ActionTypes.HEAL: (EventTypes.heal_start, EventTypes.heal_end),
    ActionTypes.SKILL_ATTACK: (EventTypes.damage_start, EventTypes.damage_end),
    ActionTypes.NORMAL_ATTACK: (EventTypes.normal_attack_start, EventTypes.normal_attack_end),
    ActionTypes.SUMMON: (EventTypes.summon_start, EventTypes.summon_end),
    ActionTypes.SELF: (EventTypes.self_start, EventTypes.self_end),
    ActionTypes.PASS: (EventTypes.pass_start, EventTypes.pass_end),
    ActionTypes.COUNTERATTACK: (EventTypes.counterattack_start, EventTypes.counterattack_end),
}

skill_event: dict[SkillTargetTypes, tuple[EventTypes, EventTypes]] = {
    SkillTargetTypes.ENEMY_SINGLE: (EventTypes.single_damage_start, EventTypes.single_damage_end),
    SkillTargetTypes.ENEMY_RANGE: (EventTypes.range_damage_start, EventTypes.range_damage_end),
}


def check_if_counterattack(target: Hero, context: Context):
    is_counterattack_disabled = get_modifier(target, context, ma.is_counterattack_disabled)
    return not is_counterattack_disabled


def check_if_counterattack_first(action: Action, context: Context):
    target = action.targets[0]
    is_counterattack_first = get_modifier(target, context, ma.is_counterattack_first)
    counterattack_first_limit = get_modifier(target, context, ma.counterattack_first_limit)
    return is_counterattack_first and counterattack_first_limit > target.counterattack_count


def check_if_in_battle(action: Action, context: Context):
    if action.skill.type == SkillTargetTypes.ENEMY_SINGLE:
        if len(action.targets) == 1:
            if check_if_counterattack(action.targets[0], context):
                target = action.targets[0]
                if action.skill.range.check_if_target_in_range(target, context):
                    return True
    else:
        return False


def action_wrapper_counterattack(context: Context):
    action = context.get_last_action()
    counter_attacker = action.targets[0]
    event_listener_calculator(counter_attacker, False, EventTypes.counterattack_start, context)
    apply_counterattack_damage(action.targets[0], action.actor, action, context)
    event_listener_calculator(counter_attacker, False, EventTypes.counterattack_end, context)


def action_wrapper_battle(context: Context, action_func: Callable[[Context], None]):
    actor = context.get_last_action().actor
    event_listener_calculator(actor, True, EventTypes.battle_start, context)
    action_func(context)
    event_listener_calculator(actor, True, EventTypes.battle_end, context)


def attack_damage_events(context: Context):
    action = context.get_last_action()
    attacker = action.actor
    skill_start_event_type = skill_event[action.skill.target_type][0]
    skill_end_event_type = skill_event[action.skill.target_type][1]
    event_listener_calculator(attacker, True, EventTypes.damage_start, context)
    event_listener_calculator(attacker, True, skill_start_event_type, context)
    apply_damage(action, context)
    event_listener_calculator(attacker, True, skill_end_event_type, context)
    event_listener_calculator(attacker, True, EventTypes.damage_end, context)


def is_hero_live(hero_instance: Hero, is_attacker: bool, context: Context):
    if hero_instance.current_life <= 0:
        event_listener_calculator(hero_instance, is_attacker, EventTypes.hero_death, context)
        context.remove_hero(hero_instance)


def apply_action(context: Context, action: Action):
    if not action.actionable:
        return

    actor = context.get_last_action().actor
    context.add_action(action)
    actions_start_event_type = action_event[action.type][0]
    actions_end_event_type = action_event[action.type][1]

    event_listener_calculator(actor, True, EventTypes.move_start, context)

    if action.movable:
        apply_move(action)

    event_listener_calculator(actor, True, EventTypes.move_end, context)

    action.update_is_in_battle(check_if_in_battle(action, context))

    event_listener_calculator(actor, True, actions_start_event_type, context)

    if action.is_in_battle:
        if check_if_counterattack_first(action, context):
            action_wrapper_counterattack(context)  # take damage
            if is_hero_live(action.actor, True, context):
                action_wrapper_battle(context, attack_damage_events)  # take damage
            is_hero_live(action.targets[0], False, context)
        else:
            action_wrapper_battle(context, attack_damage_events)  # take damage
            if is_hero_live(action.targets[0], False, context):
                action_wrapper_counterattack(context)  # take damage
            is_hero_live(action.actor, True, context)
    else:
        attack_damage_events(context)
        for target in action.targets:
            is_hero_live(target, context)

    # check liveness of all the heroes
    for hero in context.heroes:
        if hero.player_id == context.get_heroes_by_player_id(actor.player_id):
            is_hero_live(hero, True, context)
        else:
            is_hero_live(hero, False, context)

    # TODO Critical
    event_listener_calculator(actor, True, actions_end_event_type, context)
