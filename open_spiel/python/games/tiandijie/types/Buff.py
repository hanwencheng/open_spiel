import enum
from typing import Callable, List, Any

from open_spiel.python.games.tiandijie.types import Context
from open_spiel.python.games.tiandijie.types.Modifier import Modifier


class BuffType(enum.IntEnum):
    Benefit = 0
    Harm = 1
    Others = 2


class BuffTemp(Modifier):
    def __init__(self, buff_type: BuffType, dispellable, expandable, stealable, modifier_dict, upgradable: bool = False,
                 level: int = 1, before_damage=None,
                 after_damage=None, before_buff=None, after_buff=None):
        super().__init__(Modifier)
        self.type: BuffType = buff_type
        self.upgradable: bool = upgradable
        self.level: int = level or 1
        self.dispellable: bool = dispellable
        self.stealable: bool = stealable
        self.expandable: bool = expandable
        self.before_damage: [List[Callable[[Context], Any]]] = before_damage
        self.after_damage: [List[Callable[[Context], Any]]] = after_damage
        self.before_buff: [List[Callable[[Context], Any]]] = before_buff
        self.after_buff: [List[Callable[[Context], Any]]] = after_buff
        for key, value in modifier_dict.items():
            if hasattr(self, key):
                setattr(self, key, value)


class Buff:
    def __init__(self, buff_temp: BuffTemp, duration):
        # Copying attributes from BuffTemp
        self.__dict__.update(buff_temp.__dict__)
        # Setting duration
        self.duration: int = duration
        self.temp = BuffTemp
