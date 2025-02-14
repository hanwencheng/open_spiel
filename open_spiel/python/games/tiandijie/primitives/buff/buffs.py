from enum import Enum
from functools import partial

from open_spiel.python.games.tiandijie.calculation.Effects import Effects
from open_spiel.python.games.tiandijie.primitives.buff.BuffTemp import BuffTemp, BuffTypes
from open_spiel.python.games.tiandijie.primitives.event.Event import EventTypes
from open_spiel.python.games.tiandijie.primitives.event.EventListener import EventListener
from open_spiel.python.games.tiandijie.calculation.ModifierAttributes import ModifierAttributes as ma


class BuffTemps(Enum):
    # 无摧·封脉	有害	不可驱散	不可扩散	不可偷取	所有被动「绝学」失效（不可驱散）
    wucui_fengmai = BuffTemp('wucui_fengmai', BuffTypes.Harm, False, False, False, {ma.passives_disabled: True})

    # 迟缓I	有害	可驱散	可扩散	不可偷取	移动力-1，无法护卫
    chihuan_1 = BuffTemp('chihuan', BuffTypes.Harm, True, True, False, {ma.absolute_defense_range: 1, ma.move_range: -1}, True, 1)

    # 迟缓II	有害	可驱散	可扩散	不可偷取	移动力-2，无法护卫
    chihuan_2 = BuffTemp('chihuan', BuffTypes.Harm, True, True, False, {ma.absolute_defense_range: 1, ma.move_range: -2}, True, 2)

    # 迟缓III	有害	可驱散	可扩散	不可偷取	移动力-3，无法护卫
    chihuan_3 = BuffTemp('chihuan', BuffTypes.Harm, True, True, False, {ma.absolute_defense_range: 1, ma.move_range: -3}, True, 3)

    # 封劲	有害	可驱散	可扩散	可偷取	主动绝学射程-1
    fengjing = BuffTemp('fengjing', BuffTypes.Harm, True, True, True, {ma.attack_range, -1})

    # 幽霜	其他	不可驱散	不可扩散	不可偷取	免伤+20%，主动造成伤害后，对目标造成1次「固定伤害」（（物攻+物防）的30%），并施加「迟缓I」状态，持续2回合
    youshuang = BuffTemp('youshuang', BuffTypes.Others, False, False, False, {ma.magic_damage_reduction_percentage: 20, ma.damage_reduction_percentage: 20}, False, 1, [
        EventListener(EventTypes.damage_end, 1, partial(Effects.add_fixed_damage_with_attack_and_defense, multiplier=0.3, is_magic=False)),
        EventListener(EventTypes.damage_end, 2, partial(Effects.add_targets_buffs, buff_temp=[chihuan_1], duration=2))])

    # 禁闭
    jinbi = BuffTemp('jinbi', BuffTypes.Harm, False, False, False, {ma.is_action_disabled: True, ma.is_counterattack_disabled: True}, False, 1, [EventListener(EventTypes.damage_end, 1, partial(Effects.add_partner_harm_buffs, buff_number=2, range=2, duration=2))])

    # 三昧真火	有害	可驱散	不可扩散	不可偷取	法防-15%，行动结束时，遭受1次法术伤害（施加者法攻的50%）
    sanmei_zhenhuo = BuffTemp('sanmei_zhenhuo', BuffTypes.Harm, True, False, False, {ma.magic_defense_percentage: -15}, False, 1, [EventListener(EventTypes.action_end, 1, partial(Effects.take_magic_damage, multiplier=0.5))])

    # 中毒	有害	可驱散	可扩散	可偷取	行动结束时，损失10%气血，若每多移动1格，则额外损失5%气血（最多15%）
    zhongdu = BuffTemp('zhongdu', BuffTypes.Harm, True, True, True, {}, False, 1, [
        EventListener(EventTypes.action_end, 1, partial(Effects.take_fixed_damage_by_percentage, percentage=0.1)),
        EventListener(EventTypes.action_end, 1, partial(Effects.take_fixed_damage_by_percentage_per_each_move, percentage=0.05))
        ])
