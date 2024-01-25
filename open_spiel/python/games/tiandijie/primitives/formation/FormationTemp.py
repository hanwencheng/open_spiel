from typing import List, Any

from open_spiel.python.games.tiandijie.primitives.Modifier import Modifier
from open_spiel.python.games.tiandijie.primitives.formation import FormationEffect


class FormationTemp:
    def __init__(self, formation_id: str, formation_hero_id: str, activation_requirements: List[dict[Any]], effects: List[FormationEffect]):
        self.id = formation_id
        self.activation_requirements = activation_requirements
        self.hero_id = formation_hero_id
        self.effects = effects
        self.basic_modifier = Modifier({'attack_percentage': 15, 'magic_attack_percentage': 0, 'defense_percentage': 0, 'magic_defense_percentage': 15})

