import inspect
from open_spiel.python.games.tiandijie.primitives.buff.Buff import BuffTypes
from open_spiel.python.games.tiandijie.primitives.buff import BuffTemp, buffs
from open_spiel.python.games.tiandijie.primitives.Context import Context


def is_harm_buff(buff):
    return isinstance(buff, BuffTemp) and buff.type == BuffTypes.Harm and buff.dispellable


def is_benefit_buff(buff):
    return isinstance(buff, BuffTemp) and buff.type == BuffTypes.Benefit and buff.dispellable


# Automatically gather all instances of BuffTemp from the buff_temps module
harm_buff_temp_list = [obj for _, obj in inspect.getmembers(buffs, is_harm_buff)]
benefit_buff_temp_list = [obj for _, obj in inspect.getmembers(buffs, is_benefit_buff)]

game_context = Context()

game_context.init_buffs(harm_buff_temp_list, benefit_buff_temp_list)

game_context.init_heroes([])
