import enum

from open_spiel.python.games.tiandijie.Modifier import Modifier


class BuffType(enum.Enum):
    Benefit: 0
    Harm: 1


class Buff(Modifier):
    def __int__(self, duration, dispellable, level):
        super().__init__(Modifier)
        self.type = BuffType.Benefit
        self.dispellable = dispellable
        self.duration = duration
        self.level = level or 1
        self.healing = 0
        self.damage = 0
