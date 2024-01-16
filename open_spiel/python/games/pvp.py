import enum
import pyspiel


class Action(enum.IntEnum):
    MOVE = 0
    ATTACK = 1
    SKILL = 2
    WAIT = 3


_NUM_PLAYERS = 2

_DECK = []

_GAME_TYPE = pyspiel.GameType(
    short_name="tiandijie",
    long_name="tiandijie",
    dynamics=pyspiel.GameType.Dynamics.SEQUENTIAL,
    chance_mode=pyspiel.GameType.ChanceMode.EXPLICIT_STOCHASTIC,
    information=pyspiel.GameType.Information.IMPERFECT_INFORMATION,
    utility=pyspiel.GameType.Utility.ZERO_SUM,
    reward_model=pyspiel.GameType.RewardModel.TERMINAL,
    max_num_players=_NUM_PLAYERS,
    min_num_players=_NUM_PLAYERS,
    provides_information_state_string=True,
    provides_information_state_tensor=True,
    provides_observation_string=True,
    provides_observation_tensor=True,
    provides_factored_observation_string=True)
_GAME_INFO = pyspiel.GameInfo(
    num_distinct_actions=len(Action),
    max_chance_outcomes=len(_DECK),
    num_players=_NUM_PLAYERS,
    min_utility=-2.0,
    max_utility=2.0,
    utility_sum=0.0,
    max_game_length=15)


def generate_heroes_state():
    pass


class Tiandijie(pyspiel.Game):
    def __init__(self, params=None):
        super().__init__(_GAME_TYPE, _GAME_INFO, params or dict())

    def new_initial_state(self):
        return generate_heroes_state()
