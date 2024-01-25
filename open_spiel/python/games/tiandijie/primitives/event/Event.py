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
    move_end = 'move_end'

    action_start = 'action_start'
    # damage
    damage_start = 'damage_start'
    damage_end = 'damage_end'
    # battle
    battle_start = 'battle_start'
    battle_end = 'battle_end'
    # range_damage
    range_damage_start = 'range_damage_start'
    range_damage_end = 'range_damage_end'
    # critical_damage
    critical_damage_start = 'critical_damage_start'
    critical_damage_end = 'critical_damage_end'
    # heal
    heal_start = 'heal_start'
    heal_end = 'heal_end'
    # 反击
    counterattack_start = 'counterattack_start'
    counterattack_end = 'counterattack_end'

    action_end = 'action_end'

    partner_action_start = 'partner_action_start'
    partner_action_end = 'partner_action_end'

    partner_battle_start = 'partner_battle_start'
    partner_battle_end = 'partner_battle_end'

    enemy_action_start = 'enemy_action_start'
    enemy_action_end = 'enemy_action_end'

    enemy_battle_start = 'enemy_battle_start'
    enemy_battle_end = 'enemy_battle_end'

    hero_death = 'hero_death'

    # actions
    damage = 'damage'
    summon = 'summon'
    battle = 'battle'
    heal = 'heal'


class EventListenerContainer:
    def __init__(self, listener: EventListener, caster_info: CasterInfo):
        self.listener = listener
        self.casterInfo = caster_info


def event_listener_calculator(event_type: string, context: Context):
    event_listener_containers: List[EventListenerContainer] = []
    current_action: Action = context.get_last_action()
    if current_action is None:
        return
    actor: Hero = current_action.actor
    # Calculated Buffs
    for buff in actor.buffs:
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
