from typing import List

from open_spiel.python.games.tiandijie.primitives.Context import Context
from open_spiel.python.games.tiandijie.calculation.Range import calculate_if_targe_in_diamond_range
from open_spiel.python.games.tiandijie.primitives.buff.BuffTemp import BuffTypes
from open_spiel.python.games.tiandijie.primitives.hero.Element import Elements


def check_buff_on_target(context: Context, buff_type: BuffTypes, is_self: bool) -> int:
    target = context.get_last_action().actor if is_self else context.get_last_action().targets[0]
    for buff in target.buffs:
        if buff.temp.type == buff_type:
            return 1
    return 0


def check_buff_in_range(range_value: int, context: Context, buff_type: BuffTypes, is_partner: bool) -> int:
    actor = context.get_last_action().actor
    actor_position = actor.position
    for hero in context.heroes:
        if hero.id == actor.id:
            continue
        if hero.player_id == actor.player_id if is_partner else hero.player_id != actor.player_id:
            for buff in hero.buffs:
                if buff.temp.type == buff_type:
                    if calculate_if_targe_in_diamond_range(actor_position, hero.position, range_value):
                        return 1
    return 0


class FormationRequirementsCheck:

    @staticmethod
    def in_battle_with_non_flyable(context: Context) -> int:
        action = context.get_last_action()
        if action.is_in_battle:
            target = action.targets[0]
            if target.temp.flyable:
                return 0
            else:
                return 1
        return 0

    @staticmethod
    def target_life_is_below(percentage: float, context: Context) -> int:
        target = context.get_last_action().targets[0]
        return 1 if target.current_life / target.max_life < percentage / 100 else 0

    @staticmethod
    def target_life_is_higher(percentage: float, context: Context) -> int:
        target = context.get_last_action().targets[0]
        return 1 if target.current_life / target.max_life > percentage / 100 else 0

    @staticmethod
    def self_life_is_higher(percentage: float, context: Context) -> int:
        actor = context.get_last_action().actor
        return 1 if actor.current_life / actor.max_life > percentage / 100 else 0

    @staticmethod
    def no_benefit_buff(context: Context) -> int:
        target = context.get_last_action().targets[0]
        for buff in target.buffs:
            if buff.temp.type == BuffTypes.Benefit:
                return 0
        return 1

    @staticmethod
    def element_hero_in_range(elements: List[Elements], range_value: int, context: Context) -> int:
        actor = context.get_last_action().actor
        actor_position = actor.position
        count = 0
        for element in elements:
            for hero in context.heroes:
                if hero.id == actor.id:
                    continue
                if hero.player_id == actor.player_id:
                    if hero.temp.element == element:
                        if calculate_if_targe_in_diamond_range(actor_position, hero.position, range_value):
                            count += 1
                            break

        return 1 if count == len(elements) else 0

    @staticmethod
    def always_true() -> int:
        return 1

    @staticmethod
    def life_not_full_in_range(range_value: int, context: Context) -> int:
        actor = context.get_last_action().actor
        actor_position = actor.position
        for hero in context.heroes:
            if calculate_if_targe_in_diamond_range(actor_position, hero.position, range_value):
                if hero.current_life < hero.max_life:
                    return 1
        return 0

    @staticmethod
    def has_partner_in_range(range_value, context: Context) -> int:
        actor = context.get_last_action().actor
        actor_position = actor.position
        for hero in context.heroes:
            if hero.id == actor.id:
                continue
            if hero.player_id == actor.player_id:
                if calculate_if_targe_in_diamond_range(actor_position, hero.position, range_value):
                    return 1
        return 0

    @staticmethod
    def in_range_count_with_limit(range_value, maximum_count: int, context: Context) -> int:
        actor = context.get_last_action().actor
        actor_position = actor.position
        count = 0
        for hero in context.heroes:
            if hero.id == actor.id:
                continue
            if calculate_if_targe_in_diamond_range(actor_position, hero.position, range_value):
                count += 1
        return min(count, maximum_count)

    @staticmethod
    def enemy_in_range_count_bigger_than(range_value: int, count_requirement: int, context: Context) -> int:
        actor = context.get_last_action().actor
        actor_position = actor.position
        enemy_count = 0
        for hero in context.heroes:
            if hero.id == actor.id:
                continue
            if hero.player_id != actor.player_id:
                if calculate_if_targe_in_diamond_range(actor_position, hero.position, range_value):
                    enemy_count += 1
        return 1 if enemy_count >= count_requirement else 0

    @staticmethod
    def has_harm_buff_partner_in_range(range_value: int, context: Context) -> int:
        return check_buff_in_range(range_value, context, BuffTypes.Harm, True)

    @staticmethod
    def has_harm_buff_enemy_in_range(range_value: int, context: Context) -> int:
        return check_buff_in_range(range_value, context, BuffTypes.Harm, False)

    @staticmethod
    def has_benefit_buff_partner_in_range(range_value: int, context: Context) -> int:
        return check_buff_in_range(range_value, context, BuffTypes.Benefit, True)

    @staticmethod
    def has_benefit_buff_enemy_in_range(range_value: int, context: Context) -> int:
        return check_buff_in_range(range_value, context, BuffTypes.Benefit, False)

    @staticmethod
    def self_has_benefit_buff(context: Context) -> int:
        return check_buff_on_target(context, BuffTypes.Benefit, True)

    @staticmethod
    def target_has_benefit_buff(context: Context) -> int:
        return check_buff_on_target(context, BuffTypes.Benefit, False)

    @staticmethod
    def self_has_harm_buff(context: Context) -> int:
        return check_buff_on_target(context, BuffTypes.Harm, True)

    @staticmethod
    def target_has_harm_buff(context: Context) -> int:
        return check_buff_on_target(context, BuffTypes.Harm, False)

    @staticmethod
    def life_not_full(context: Context) -> int:
        actor = context.get_last_action().actor
        return 1 if actor.current_life < actor.max_life else 0

    @staticmethod
    def life_is_full(context: Context) -> int:
        actor = context.get_last_action().actor
        return 1 if actor.current_life == actor.max_life else 0

    @staticmethod
    def target_harm_buff_count(context: Context) -> int:
        target = context.get_last_action().targets[0]
        harm_buff_count = 0
        for buff in target.buffs:
            if buff.temp.type == BuffTypes.Harm:
                harm_buff_count += 1
        return min(3, harm_buff_count)

    @staticmethod
    def self_harm_buff_count_smaller_than(count: int, context: Context) -> int:
        actor = context.get_last_action().actor
        harm_buff_count = 0
        for buff in actor.buffs:
            if buff.temp.type == BuffTypes.Harm:
                harm_buff_count += 1
        return 1 if harm_buff_count < count else 0

    @staticmethod
    def target_harm_buff_count_bigger_than(count: int, context: Context) -> int:
        target = context.get_last_action().targets[0]
        harm_buff_count = 0
        for buff in target.buffs:
            if buff.temp.type == BuffTypes.Harm:
                harm_buff_count += 1
        return 1 if harm_buff_count > count else 0

    @staticmethod
    def self_life_is_higher_and_no_harm_buff(percentage: float, context: Context) -> int:
        actor = context.get_last_action().actor
        if actor.current_life / actor.max_life > percentage / 100:
            for buff in actor.buffs:
                if buff.temp.type == BuffTypes.Harm:
                    return 0
            return 1
        return 0
