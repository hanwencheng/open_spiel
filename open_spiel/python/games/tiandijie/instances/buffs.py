from functools import partial

from open_spiel.python.games.tiandijie.calculation.effects import *
from open_spiel.python.games.tiandijie.types.Buff import BuffTemp, BuffType

# 无摧·封脉
wucui_fengmai = BuffTemp(BuffType.Harm, False, False, False, {'passives_on': False})
# 迟缓1
chihuan_1 = BuffTemp(BuffType.Harm, True, True, False, {'absolute_defense_range': 1, 'move_range': -1}, True, 1)
# 迟缓2
chihuan_2 = BuffTemp(BuffType.Harm, True, True, False, {'absolute_defense_range': 1, 'move_range': -2}, True, 2)
# 迟缓3
chihuan_3 = BuffTemp(BuffType.Harm, True, True, False, {'absolute_defense_range': 1, 'move_range': -3}, True, 3)
# 封劲
fengjing = BuffTemp(BuffType.Harm, True, True, True, {'attack_range', -1})
# 幽霜
youshuang = BuffTemp(BuffType.Others, False, False, False,
                     {'magic_damage_reduction': 20, 'damage_reduction': 20}, False, 1, None, [
                         partial(add_fixed_damage_with_attack_and_defense, 0.3, False),
                         partial(add_defender_buff, chihuan_1, 2)
                     ])

