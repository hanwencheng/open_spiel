from open_spiel.python.games.tiandijie.types import Hero


def calculate_after_damage_buff(attacker_instance: Hero, defender_instance: Hero, context: Context):
    action = context.get_last_action()
