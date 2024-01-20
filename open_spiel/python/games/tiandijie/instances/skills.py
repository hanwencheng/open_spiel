from functools import partial

from open_spiel.python.games.tiandijie.calculation.effects import *
from open_spiel.python.games.tiandijie.types.Range import Range, RangeType
from open_spiel.python.games.tiandijie.types.Skill import Skill
from open_spiel.python.games.tiandijie.instances.buffs import *

normal_attack = Skill(1, True)

zhijianfongyou = Skill(0.7, False)
# 灭剑罗渊
miejianluoyuan = Skill(0.7, Range(RangeType.DIRECTIONAL, 0, 4, 3), [],
                       [
                        partial(reduce_target_benefit_buff_duration, 2),
                        partial(add_defender_buff, fengjing, 2),
                        partial(check_buff_conditional_add_target_buff(youshuang, wucui_fengmai, 2))
                        ])


