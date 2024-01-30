import enum
import string
from typing import List

from open_spiel.python.games.tiandijie.primitives import Action
from open_spiel.python.games.tiandijie.primitives.buff.Buff import CasterInfo
from open_spiel.python.games.tiandijie.primitives.Context import Context
from open_spiel.python.games.tiandijie.primitives.event.EventListener import EventListener
from open_spiel.python.games.tiandijie.primitives.hero import Hero


class EventTypes(enum.Enum):
    move_start = 'move_start'
    move = 'move'
    move_end = 'move_end'

    action_start = 'action_start'
    # damage
    damage_start = 'damage_start'
    damage = 'damage'
    damage_end = 'damage_end'
    # battle
    battle_start = 'battle_start'
    battle = 'battle'
    battle_end = 'battle_end'
    # range_damage
    range_damage_start = 'range_damage_start'
    range_damage = 'range_damage'
    range_damage_end = 'range_damage_end'
    # single_damage
    single_damage_start = 'single_damage_start'
    single_damage = 'single_damage'
    single_damage_end = 'single_damage_end'
    # normal_attack
    normal_attack_start = 'normal_attack_start'
    normal_attack = 'normal_attack'
    normal_attack_end = 'normal_attack_end'
    # critical_damage
    critical_damage_start = 'critical_damage_start'
    critical_damage = 'critical_damage'
    critical_damage_end = 'critical_damage_end'
    # heal
    heal_start = 'heal_start'
    heal = 'heal'
    heal_end = 'heal_end'
    # summon
    summon_start = 'summon_start'
    summon = 'summon'
    summon_end = 'summon_end'
    # self
    self_start = 'self_start'
    self = 'self'
    self_end = 'self_end'
    # pass
    pass_start = 'pass_start'
    pass_end = 'pass_end'
    # counterattack
    counterattack_start = 'counterattack_start'
    counterattack = 'counterattack'
    counterattack_end = 'counterattack_end'

    action_end = 'action_end'

    partner_action_start = 'partner_action_start'
    partner_action = 'partner_action'
    partner_action_end = 'partner_action_end'

    partner_battle_start = 'partner_battle_start'
    partner_battle = 'partner_battle'
    partner_battle_end = 'partner_battle_end'

    enemy_action_start = 'enemy_action_start'
    enemy_action = 'enemy_action'
    enemy_action_end = 'enemy_action_end'

    enemy_battle_start = 'enemy_battle_start'
    enemy_battle = 'enemy_battle'
    enemy_battle_end = 'enemy_battle_end'

    hero_death = 'hero_death'


class EventListenerContainer:
    def __init__(self, listener: EventListener, caster_info: CasterInfo):
        self.listener = listener
        self.casterInfo = caster_info


def event_listener_calculator(hero_instance: Hero, is_attacker: bool, event_type: string, context: Context):
    event_listener_containers: List[EventListenerContainer] = []
    current_action: Action = context.get_last_action()
    if current_action is None:
        return
    # Calculated Buffs
    for buff in hero_instance.buffs:
        buff_event_listeners: List[EventListener] = buff.temp.on_event
        for event_listener in buff_event_listeners:
            if event_listener.event_type == event_type:
                event_listener_containers.append(EventListenerContainer(event_listener, buff.caster_info))

    # Calculate Talents

    # Calculate Passives

    # re-order the event listeners by priority in accumulated_event_listeners
    event_listener_containers.sort(key=lambda x: x.listener.priority)

    for event_listener_container in event_listener_containers:
        event_listener_container.listener.callback(context, event_listener_container.casterInfo)
