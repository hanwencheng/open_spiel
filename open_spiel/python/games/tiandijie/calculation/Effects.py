import random
from typing import List

from open_spiel.python.games.tiandijie.calculation.calculate import get_attack, get_defense, get_max_life
from open_spiel.python.games.tiandijie.calculation.calculate_damage import calculate_fix_damage, calculate_magic_damage, \
    calculate_physical_damage
from open_spiel.python.games.tiandijie.primitives import Context, Action
from open_spiel.python.games.tiandijie.primitives.buff.Buff import Buff, CasterInfo
from open_spiel.python.games.tiandijie.primitives.buff import BuffTemp
from open_spiel.python.games.tiandijie.primitives.buff.BuffTemp import BuffTypes
from open_spiel.python.games.tiandijie.primitives.hero import Hero
from open_spiel.python.games.tiandijie.calculation.Range import Range


def get_current_action(context: Context) -> Action:
    return context.actions[-1]


def _add_buffs(target: Hero, buff_temp: List[BuffTemp], duration: float):
    new_buffs = [Buff(b, duration) for b in buff_temp]
    for new_buff in new_buffs:
        existing_buff = next((buff for buff in target.buffs if buff.temp.id == new_buff.temp.id), None)
        if existing_buff is not None:
            # Replace the existing buff if the new buff has a higher level
            if new_buff.temp.level > existing_buff.temp.level:
                target.buffs.remove(existing_buff)
                target.buffs.append(new_buff)
            else:
                existing_buff.duration = duration
        else:
            target.buffs.append(new_buff)


class Effects:
    @staticmethod
    def add_buffs(target: Hero, buff_temp: List[BuffTemp], duration: float, context: Context):
        _add_buffs(target, buff_temp, duration)

    @staticmethod
    def add_fixed_damage_with_attack_and_defense(multiplier: float, is_magic: bool, context: Context):
        current_action = get_current_action(context)
        actor = current_action.actor
        damage = (get_attack(actor, is_magic, context) + get_defense(actor, is_magic, context)) * multiplier
        for target in current_action.targets:
            calculate_fix_damage(damage, target, context)

    @staticmethod
    def add_targets_buffs(buff_temp: List[BuffTemp], duration: float, context: Context):
        current_action = context.actions[-1]
        add_buffs = map(lambda b: Buff(b, duration), buff_temp)
        for target in current_action.targets:
            target.buffs.extend(add_buffs)

    @staticmethod
    def reduce_target_benefit_buff_duration(duration_reduction: int, context: Context):
        current_action = get_current_action(context)
        for target in current_action.targets:
            for buff in target.buffs:
                if buff.type == BuffTypes.Benefit:  # Assuming each buff has an 'is_advantage' attribute
                    buff.duration -= duration_reduction
                    if buff.duration < 0:
                        buff.duration = 0  # Prevent negative duration

    @staticmethod
    def check_buff_conditional_add_target_buff(check_buff: BuffTemp, add_buff: BuffTemp, duration: int,
                                               context: Context):
        current_action = get_current_action(context)
        actor = current_action.actor
        if any(buff.temp == check_buff for buff in actor.buffs):
            for target in current_action.targets:
                _add_buffs(target, [add_buff], duration)

    @staticmethod
    def add_partner_harm_buffs(buff_number: int, range_value: int, duration: int, context: Context):
        current_action = get_current_action(context)
        actor = current_action.actor
        partners = context.get_partners_in_range(actor, range_value)
        selected_harm_buff_temps = random.sample(context.harm_buffs, buff_number)
        for partner in partners:
            _add_buffs(partner, selected_harm_buff_temps, duration)

    @staticmethod
    def remove_partner_selected_buffs(buff_temp: BuffTemp, range_value: int, context: Context):
        current_action = get_current_action(context)
        actor = current_action.actor
        partners = context.get_partners_in_range(actor, range_value)
        for partner in partners:
            partner.buffs = [buff for buff in partner.buffs if buff.temp.id != buff_temp.id]

    @staticmethod
    def clear_terrain_in_range(range_class: Range, context: Context):
        terrain = context.terrain
        for i in range_class.get_area(context):
            terrain[i] = None

    @staticmethod
    def take_magic_damage(multiplier: float, context: Context, caster_info: CasterInfo):
        current_action = get_current_action(context)
        actor = current_action.actor
        calculate_magic_damage(caster_info.caster_magic_attack * multiplier, actor, context)

    @staticmethod
    def take_physical_damage(multiplier: float, context: Context, caster_info: CasterInfo):
        current_action = get_current_action(context)
        actor = current_action.actor
        calculate_physical_damage(caster_info.caster_physical_attack * multiplier, actor, context)

    @staticmethod
    def take_fixed_damage_by_percentage(percentage: float, context: Context):
        current_action = get_current_action(context)
        actor = current_action.actor
        actor_max_life = get_max_life(actor, context)
        calculate_fix_damage(actor_max_life * percentage, actor, context)

    @staticmethod
    def take_fixed_damage_by_percentage_per_each_move(percentage: float, context: Context):
        current_action: Action = get_current_action(context)
        move_count = len(current_action.moves)
        actor = current_action.actor
        actor_max_life = get_max_life(actor, context)
        calculate_fix_damage(actor_max_life * percentage * move_count, actor, context)
