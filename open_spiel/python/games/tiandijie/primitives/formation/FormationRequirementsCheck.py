from typing import List

from open_spiel.python.games.tiandijie.primitives.Context import Context
from open_spiel.python.games.tiandijie.primitives.Range import calculate_if_targe_in_diamond_range
from open_spiel.python.games.tiandijie.primitives.buff.BuffTemp import BuffTypes
from open_spiel.python.games.tiandijie.primitives.hero.Element import Elements


class FormationRequirementsCheck:

    @staticmethod
    def targe_life_is_higher(percentage: float, context: Context) -> int:
        target = context.get_last_action().targets[0]
        return 1 if target.current_life / target.max_life > percentage/100 else 0

    @staticmethod
    def self_life_is_higher(percentage: float, context: Context) -> int:
        actor = context.get_last_action().actor
        return 1 if actor.current_life / actor.max_life > percentage/100 else 0

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
        for hero in context.heroes:
            if hero.element in elements:
                if calculate_if_targe_in_diamond_range(actor_position, hero.position, range_value):
                    return 1
        return 0

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
    def in_range(range_value, context: Context) -> int:
        actor = context.get_last_action().actor
        actor_position = actor.position
        for hero in context.heroes:
            if calculate_if_targe_in_diamond_range(actor_position, hero.position, range_value):
                return 1
        return 0

    @staticmethod
    def has_benefit_buff(context: Context) -> int:
        target = context.get_last_action().targets[0]
        for buff in target.buffs:
            if buff.temp.type == BuffTypes.Benefit:
                return 1
        return 0

    @staticmethod
    def life_not_full(context: Context) -> int:
        actor = context.get_last_action().actor
        return 1 if actor.current_life < actor.max_life else 0

    @staticmethod
    def target_harm_buff_count(context: Context) -> int:
        target = context.get_last_action().targets[0]
        harm_buff_count = 0
        for buff in target.buffs:
            if buff.temp.type == BuffTypes.Harm:
                harm_buff_count += 1
        return min(3, harm_buff_count)
