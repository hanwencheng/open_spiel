from typing import List

from open_spiel.python.games.tiandijie.types import Action, Formation, Hero
from open_spiel.python.games.tiandijie.types.Buff import Buff


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

