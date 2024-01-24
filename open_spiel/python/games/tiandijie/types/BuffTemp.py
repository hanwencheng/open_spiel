import enum
import string
from typing import Callable, List, Any

from open_spiel.python.games.tiandijie.types import Context, EventListener
from open_spiel.python.games.tiandijie.types.Modifier import Modifier


class BuffType(enum.IntEnum):
    Benefit = 0
    Harm = 1
    Others = 2


class BuffTemp():
    def __init__(self, buff_id: string, buff_type: BuffType, dispellable, expandable, stealable, modifier_dict,
                 upgradable: bool = False,
                 level: int = 1, on_event=None):
        if on_event is None:
            on_event = []
        self.id = buff_id
        self.type: BuffType = buff_type
        self.upgradable: bool = upgradable
        self.level: int = level or 1
        self.dispellable: bool = dispellable
        self.stealable: bool = stealable
        self.expandable: bool = expandable
        self.on_event: List[EventListener]
        self.modifier = Modifier(modifier_dict)
