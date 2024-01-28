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
    event_listener_calculator(EventTypes.counterattack_start, context)
    apply_counterattack_damage(context)
    event_listener_calculator(EventTypes.counterattack_end, context)


def action_wrapper_battle(context: Context, action_func: Callable[[Context], None]):
    event_listener_calculator(EventTypes.battle_start, context)
    action_func(context)
    event_listener_calculator(EventTypes.battle_end, context)


def attack_damage_events(context: Context):
    action = context.get_last_action()
    skill_start_event_type = skill_event[action.skill.target_type][0]
    skill_end_event_type = skill_event[action.skill.target_type][1]
    event_listener_calculator(EventTypes.damage_start, context)
    event_listener_calculator(skill_start_event_type, context)
    apply_damage(context)
    event_listener_calculator(skill_end_event_type, context)
    event_listener_calculator(EventTypes.damage_end, context)


def is_hero_live(hero_instance: Hero, context: Context):
    if hero_instance.current_life <= 0:
        event_listener_calculator(EventTypes.hero_death, context)
        context.remove_hero(hero_instance)


def apply_action(context: Context, action: Action):
    if not action.actionable:
        return

    context.add_action(action)
    actions_start_event_type = action_event[action.type][0]
    actions_end_event_type = action_event[action.type][1]

    event_listener_calculator(EventTypes.move_start, context)

    if action.movable:
        apply_move(action)

    event_listener_calculator(EventTypes.move_end, context)

    action.update_is_in_battle(check_if_in_battle(action, context))

    event_listener_calculator(actions_start_event_type, context)

    if action.is_in_battle:
        if check_if_counterattack_first(action, context):
            action_wrapper_counterattack(context)
            if is_hero_live(action.actor, context):
                action_wrapper_battle(context, attack_damage_events)
        else:
            action_wrapper_battle(context, attack_damage_events)
            if is_hero_live(action.targets[0], context):
                action_wrapper_counterattack(context)
            action_wrapper_counterattack(context)
    else:
        action_wrapper_battle(context, attack_damage_events)
        for target in action.targets:
            is_hero_live(target, context)

    # check liveness of all the heroes
    for hero in context.heroes:
        is_hero_live(hero, context)

    # TODO Critical
    event_listener_calculator(actions_end_event_type, context)
