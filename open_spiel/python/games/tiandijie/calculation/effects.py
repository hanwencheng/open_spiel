from open_spiel.python.games.tiandijie.calculation.calculate import get_attack, get_defense
from open_spiel.python.games.tiandijie.calculation.calculate_damage import calculate_fix_damage
from open_spiel.python.games.tiandijie.types import Context, Action
from open_spiel.python.games.tiandijie.types.Buff import BuffTemp, Buff, BuffType


def get_current_action(context: Context) -> Action:
    return context.actions[-1]


def add_fixed_damage_with_attack_and_defense(multiplier: float, is_magic: bool, context: Context):
    current_action = get_current_action(context)
    actor = current_action.actor
    damage = (get_attack(actor, is_magic, context) + get_defense(actor, is_magic, context)) * multiplier
    for target in current_action.targets:
        calculate_fix_damage(damage, target, context)


def add_defender_buff(buff_temp: BuffTemp, duration: float, context: Context):
    current_action = context.actions[-1]
    actor = current_action.actor
    for target in current_action.targets:
        target.buffs.push(Buff(buff_temp, duration))


def reduce_target_benefit_buff_duration(duration_reduction: int, context: Context):
    current_action = get_current_action(context)
    for target in current_action.targets:
        for buff in target.buffs:
            if buff.type == BuffType.Benefit:  # Assuming each buff has an 'is_advantage' attribute
                buff.duration -= duration_reduction
                if buff.duration < 0:
                    buff.duration = 0  # Prevent negative duration


def check_buff_conditional_add_target_buff(check_buff: BuffTemp, add_buff: BuffTemp, duration: int, context: Context):
    current_action = get_current_action(context)
    actor = current_action.actor
    if any(buff.temp == check_buff for buff in actor.buffs):
        for target in current_action.targets:
            target.buffs.push(Buff(add_buff, duration))
