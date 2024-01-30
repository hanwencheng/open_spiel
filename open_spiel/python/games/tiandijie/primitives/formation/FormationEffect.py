from typing import List, Callable

from open_spiel.python.games.tiandijie.primitives.Action import Action
from open_spiel.python.games.tiandijie.primitives.Context import Context
from open_spiel.python.games.tiandijie.primitives.event import EventListener


class FormationEffect:
    def __init__(self, requirement: Callable[[bool, Context], int], modifier: dict, on_event: List[EventListener]):
        self.modifier = modifier
        self.on_event = on_event
        self.requirement = requirement
