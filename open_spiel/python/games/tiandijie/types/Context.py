from typing import List

from open_spiel.python.games.tiandijie.types import Action, Formation, Hero


class Context:
    def __init__(self):
        self.heroes: List[Hero] = []
        self.formation: List[Formation] = []
        self.actions: List[Action] = []

    def add_action(self, action):
        self.actions.append(action)

    def get_last_action(self) -> Action:
        if self.actions:
            return self.actions[-1]
        else:
            return None  # Return None if there are no actions



