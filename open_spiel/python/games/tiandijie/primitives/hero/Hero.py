from typing import List

from open_spiel.python.games.tiandijie.primitives import Equipment
from open_spiel.python.games.tiandijie.primitives.Stone import Stone
from open_spiel.python.games.tiandijie.primitives.hero.Attributes import Attributes, generate_max_level_attributes
from open_spiel.python.games.tiandijie.primitives.hero import HeroTemp
from open_spiel.python.games.tiandijie.primitives.buff import Buff


class Hero:
    def __init__(self, player_id: int, hero_temp: HeroTemp):
        self.player_id = player_id
        self.temp: HeroTemp = hero_temp
        self.equipments: List[Equipment] = []
        self.stones = Stone()
        self.buffs: List[Buff] = []
        self.initial_attributes = None
        self.current_life: float = 1.0
        self.initialize_attributes()

    def initialize_attributes(self):
        initial_attributes = generate_max_level_attributes(
            self.temp.level0_attributes,
            self.temp.growth_coefficients,
            self.temp.profession
        )
        self.initial_attributes = initial_attributes
        self.current_life = self.initial_attributes.life

    def take_harm(self, harm_value: float):
        if harm_value > 0:
            self.current_life -= harm_value

    def take_healing(self, healing_value: float):
        if healing_value > 0:
            self.current_life += healing_value
