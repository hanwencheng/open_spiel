from open_spiel.python.games.tiandijie.calculation.calculate import get_attack
from open_spiel.python.games.tiandijie.types import Hero, Context, BuffTemp


class CasterInfo:
    def __init__(self, caster: Hero, target: Hero, context: Context):
        self.caster_physical_attack = get_attack(caster, False, context)
        self.caster_magic_attack = get_attack(caster, True, context)
        self.target = target


class Buff:
    def __init__(self, buff_temp: BuffTemp, duration: int, caster_info: CasterInfo):
        # Copying attributes from BuffTemp
        self.__dict__.update(buff_temp.__dict__)
        # Setting duration
        self.duration: int = duration
        self.temp = BuffTemp
        self.caster_info = caster_info


def cast_buff(buff_temp: BuffTemp, duration: int, caster: Hero):
    return Buff(buff_temp, duration, caster)
