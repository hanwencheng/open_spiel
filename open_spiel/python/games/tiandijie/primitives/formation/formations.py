from functools import partial

from open_spiel.python.games.tiandijie.primitives.event.Event import EventTypes
from open_spiel.python.games.tiandijie.primitives.event.EventListener import EventListener
from open_spiel.python.games.tiandijie.primitives.formation.FormationEffect import FormationEffect
from open_spiel.python.games.tiandijie.primitives.formation.FormationTemp import FormationTemp
from open_spiel.python.games.tiandijie.primitives.hero.Element import Elements
from open_spiel.python.games.tiandijie.primitives.hero.HeroBasics import Professions, Gender
from open_spiel.python.games.tiandijie.calculation.Effects import Effects
from open_spiel.python.games.tiandijie.primitives.formation.FormationRequirementsCheck import \
    FormationRequirementsCheck as Check


class Formations:
    # 上阵韩千秀和「侠客」，「铁卫」英灵至少各一名时，激活战阵。所有我方上阵角色物攻，物防，法攻，法防提升15%，主动造成伤害后，额外附加1次「固定伤害」（目标当前气血*15%）。
    feiyanjinghong = FormationTemp('feiyanjinghong', 'hanqianxiu',
                                   [{'[profession': Professions.GUARD}, {'profession': Professions.SWORDSMAN}], [
                                       FormationEffect(Check.always_true, {}, [EventListener(EventTypes.damage_end, 1,
                                                                                             partial(
                                                                                                 Effects.take_fixed_damage_by_percentage,
                                                                                                 0.15))])])

    # 万念轮回阵: 上阵铁手夏侯仪和「雷」，「冰」属性英灵至少各一位时，激活战阵。所有我方上阵角色物攻，物防，法攻，法防提高15%，3格范围内存在气血未满的角色，伤害提高10%。
    wannianlunhui = FormationTemp('wannianlunhui', 'tieshouxiahouyi',
                                  [{'element': Elements.THUNDER}, {'element': Elements.WATER}], [
                                      FormationEffect(partial(Check.life_not_full_in_range, 3),
                                                      {'damage_percentage': 10, 'magic_damage_percentage': 10}, [])])

    # 三身通智阵: 上阵真胤和至少2位「阵眼」英灵时，激活战阵。所有我方上阵角色物攻，物防，法攻，法防提高15%，2格内有其他友方角色时，绝学伤害提升10%。
    sanshentongzhi = FormationTemp('sanshentongzhi', 'zhenyin', [{'has_formation': True}, {'has_formation': True}],
                                   [FormationEffect(partial(Check.in_range, 2), {'skill_damage_percentage': 10}, [])])

    # 义鼠夺风阵: 上阵白玉堂和「暗」，「炎」属相英灵至少各一位时，激活战阵。所有我方上阵角色物攻，物防，法攻，法防提高15%，自身携带「有益状态」时，伤害提高10%。
    yishuduofeng = FormationTemp('yishuduofeng', 'baiyutang', [{'element': Elements.DARK}, {'element': Elements.FIRE}],
                                 [FormationEffect(Check.has_benefit_buff,
                                                  {'damage_percentage': 10, 'magic_damage_percentage': 10}, [])])

    # 乾坤流烨阵: 上阵武英仲和至少2位「光」属性英灵时，激活战阵。所有我方上阵角色物攻，物防，法攻，法防提高15%，若目标未携带「有益状态」，「对战中」伤害提高15%。
    qiankunliuye = FormationTemp('qiankunliuye', 'wuyingzhong',
                                 [{'element': Elements.LIGHT}, {'element': Elements.LIGHT}],
                                 [FormationEffect(Check.has_benefit_buff,
                                                  {'battle_damage_modifier': 15}, [])])

    # 伦巴第协阵： 上阵古伦德和至少2位「男性」英灵时，激活战阵。所有我方上阵角色物攻，物防，法攻，法防提升15%，自身气血未满时，伤害提高10%。
    lunbadixie = FormationTemp('lunbadixie', 'gulunde', [{'gender': Gender.MALE}, {'gender': Gender.MALE}], [
        FormationEffect(Check.life_not_full, {'damage_percentage': 10, 'magic_damage_percentage': 10}, [])])

    # 佛口蛇心阵: 上阵青和「雷」，「光」属相英灵至少各一位时，激活战阵。所有我方上阵角色物攻，物防，法攻，法防提高15%。目标每有1个「有害状态」，「对战中」伤害提高5%（最多提高15%）。
    fokoushexin = FormationTemp('fokoushexin', 'qing', [{'element': Elements.THUNDER}, {'element': Elements.LIGHT}],
                                [FormationEffect(Check.target_harm_buff_count, {'battle_damage_modifier': 5}, [])])

    # 侠风洗刃阵: 上阵奚歌和「炎」，「雷」英灵至少各一位时，激活战阵。所有我方上阵角色物攻，物防，法攻，法防提高15%，单体绝学伤害提高10%。
    xiafengxiren = FormationTemp('xiafengxiren', 'xige', [{'element': Elements.FIRE}, {'element': Elements.THUNDER}], [FormationEffect(Check.always_true, {'single_target_skill_damage_percentage': 10}, [])])
