import string
from enum import Enum
from functools import partial
from typing import List

from open_spiel.python.games.tiandijie.calculation.Effects import Effects
from open_spiel.python.games.tiandijie.primitives.event.Event import EventTypes
from open_spiel.python.games.tiandijie.primitives.event.EventListener import EventListener
from open_spiel.python.games.tiandijie.primitives.Modifier import Modifier


class TerrainBuffTemp:
    def __init__(self, buff_id: string, dispellable: bool, modifier_dict, on_event=None):
        if on_event is None:
            on_event = []
        self.modifier = Modifier(modifier_dict)
        self.id = buff_id
        self.dispellable = dispellable
        self.on_event: List[EventListener] = on_event


class TerrainBuff:
    def __init__(self, temp: TerrainBuffTemp, duration: int, side: int):
        self.temp = temp
        self.duration = duration
        self.side = side


class TerrainBuffTemps(Enum):
    fire = TerrainBuffTemp('fire', True, {}, [
        EventListener(EventTypes.action_end, 1, partial(Effects.take_fixed_damage_by_percentage, percentange=0.1))])
    ice = TerrainBuffTemp('ice', True, {'move_range': -1})
