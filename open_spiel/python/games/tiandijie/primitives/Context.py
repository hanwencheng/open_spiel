from typing import List

from open_spiel.python.games.tiandijie.primitives import Action
from open_spiel.python.games.tiandijie.primitives.formation import Formation
from open_spiel.python.games.tiandijie.primitives.buff.Buff import Buff
from open_spiel.python.games.tiandijie.primitives.hero import Hero


class Context:
    def __init__(self):
        self.heroes: List[Hero] = []
        self.formation: List[Formation] = []
        self.actions: List[Action] = []
        self.harm_buffs: List[Buff] = []
        self.benefit_buffs: List[Buff] = []

    def add_action(self, action):
        self.actions.append(action)

    def get_last_action(self) -> Action:
        if self.actions:
            return self.actions[-1]
        else:
            return None  # Return None if there are no actions

    def get_partners_in_range(self, hero: Hero, range_value: int) -> List[Hero]:
        return []

    def init_buffs(self, harm_buffs, benefit_buffs):
        self.harm_buffs = harm_buffs
        self.benefit_buffs = benefit_buffs

    def init_heroes(self, heroes: List[Hero]):
        self.heroes = heroes

    def get_current_player_id(self) -> int:
        return self.get_last_action().player_id

    def get_formation_by_player_id(self, player_id: int) -> Formation:
        return [formation for formation in self.formation if formation.player_id == player_id][0]

    def get_heroes_by_player_id(self, player_id: int) -> List[Hero]:
        return [hero for hero in self.heroes if hero.player_id == player_id]

    def get_heroes_by_counter_player_id(self, player_id: int) -> List[Hero]:
        return [hero for hero in self.heroes if hero.player_id != player_id]
