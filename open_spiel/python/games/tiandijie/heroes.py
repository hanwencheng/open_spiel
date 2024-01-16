import enum
from typing import Tuple

from open_spiel.python.games.tiandijie import wunei, basicAttributes
from open_spiel.python.games.tiandijie.types import Attributes


class Elements(enum.IntEnum):
    FIRE = 1  # 火
    WATER = 2  # 冰
    THUNDER = 3  # 雷
    LIGHT = 4  # 光
    DARK = 5  # 暗
    ETHEREAL = 6  # 幽


class Gender(enum.IntEnum):
    MALE = 1
    FEMALE = 2


class Professions(enum.Enum):
    # ID，RANGE, MOVE
    GUARD = (1, 1, 3)
    SWORDSMAN = (2, 1, 3)
    SORCERER = (3, 2, 3)
    PRIEST = (4, 2, 3)
    ARCHER = (5, 2, 3)
    RIDER = (6, 1, 5)
    WARRIOR = (7, 1, 4)

class Hero:
    def __init__(self, basicInfo, initial_attributes, growth_coefficients, skills):
        self.name = "玄羽"
        self.pinyin = "XUANYU"
        self.rarity = "绝"
        self.gender = Gender.FEMALE
        if self.gender not in Gender:
            raise ValueError("性别必须是‘男’或‘女’")
        self.element = Elements.DARK
        self.profession = Professions.ARCHER
        self.wunei_profession = wunei.WuneiProfessions.ARCHER
        self.jishen_profession = basicAttributes.JishenProfessions.ARCHER
        self.shenbin_profession = basicAttributes.ShenbinProfessions.ARCHER
        self.huazhen_profession = basicAttributes.HuazhenProfessions.ARCHER
        self.range = 2
        self.movement = 3
        self.initial_attributes = Attributes(172, 89, 31, 22, 23, 60)
        self.growth_coefficients = Attributes(25.77, 13.42, 4.7, 3.36, 3.49, 0.6)
        self.talent = "玄翎鸩影"
        self.initial_skill = "逐风破"
        self.skills = {
            "初级": ["魔", "幽镝戒杀"],
            "中级": ["飞羽憾魄"],
            "高级": ["迅", "奋力", "漫天箭雨", "摧心闇矢"],
            "特级": ["晦弓在弦"],
            "极级": ["魂", "贯甲咒"]
        }
        self.weapons = ["柳木弓", "缠银弓", "暮云弓", "幽蚕弓"]
        self.weapon_features = ["鹤唳", "翎牙", "锁心"]
        # Attributes initialization
        self.current_attributes = None
        self.initialize_attributes()

    def initialize_attributes(self):
        self.current_attributes.generate_max_level_attributes(
            self.growth_coefficients,
            self.wunei_profession,
            self.jishen_profession,
            self.shenbin_profession,
            self.huazhen_profession
        )
