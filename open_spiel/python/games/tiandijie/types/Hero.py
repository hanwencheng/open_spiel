from typing import List
from basics import Position

from open_spiel.python.games.Element import Elements
from open_spiel.python.games.tiandijie import wunei
from open_spiel.python.games.tiandijie.HeroBasics import Gender, Professions
from open_spiel.python.games.tiandijie.types import BasicAttributes, Passive, Buff, Equipment
from open_spiel.python.games.tiandijie.types.Stone import Stone
from open_spiel.python.games.tiandijie.types.Attributes import Attributes


class Hero:
    def __init__(self, basicInfo, initial_attributes, growth_coefficients, skills, playerId):
        self.current_life: float = 1
        self.name = "玄羽"
        self.pinyin = "XUANYU"
        self.rarity = "绝"
        self.playerId = 0
        self.buffs: List[Buff] = []
        self.passives: List[Passive] = []
        self.stones = Stone()
        self.equipments: List[Equipment] = []
        self.gender = Gender.FEMALE
        if self.gender not in Gender:
            raise ValueError("性别必须是‘男’或‘女’")
        self.element: Elements = Elements.DARK
        self.profession: Professions = Professions.ARCHER
        self.wunei_profession = wunei.WuneiProfessions.ARCHER
        self.jishen_profession = BasicAttributes.JishenProfessions.ARCHER
        self.shenbin_profession = BasicAttributes.ShenbinProfessions.ARCHER
        self.huazhen_profession = BasicAttributes.HuazhenProfessions.ARCHER
        self.position: Position = (0, 0)
        self.range: int = 2
        self.movement: int = 3
        self.initial_attributes: Attributes = Attributes(172, 89, 31, 22, 23, 60)
        self.growth_coefficients: Attributes = Attributes(25.77, 13.42, 4.7, 3.36, 3.49, 0.6)
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
        self.current_attributes: Attributes = None
        self.initialize_attributes()

    def initialize_attributes(self):
        self.current_attributes.generate_max_level_attributes(
            self.growth_coefficients,
            self.wunei_profession,
            self.jishen_profession,
            self.shenbin_profession,
            self.huazhen_profession
        )
        self.current_life = self.current_attributes.life

    def take_harm(self, harm_value: float):
        if harm_value > 0:
            self.current_life -= harm_value

    def take_healing(self, healing_value: float):
        if healing_value > 0:
            self.current_life += healing_value
