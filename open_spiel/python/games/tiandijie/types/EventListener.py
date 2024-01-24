from functools import partial

from open_spiel.python.games.tiandijie.types import Context
from open_spiel.python.games.tiandijie.types.Buff import CasterInfo
from open_spiel.python.games.tiandijie.types.Event import EventTypes


class EventListener:
    def __init__(self, event_type: EventTypes, priority: int, listener: partial[[Context, CasterInfo], None]):
        self.event_type = event_type
        self.priority = priority
        self.callback = listener
