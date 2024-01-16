import enum
from open_spiel.python.games.tiandijie.types import Attributes


class JishenProfessions(enum.Enum):
    SWORDSMAN_WITH_MAGIC = (867, 0, 335, 268, 202, 0)  # LIFE, ATTACK, DEFENSE, MAGIC_ATTACK, MAGIC_DEFENSE, LUCK
    SWORDSMAN = (867, 268, 335, 0, 202, 0)
    PRIEST = (991, 0, 310, 0, 366, 0)
    ARCHER = (643, 251, 299, 0, 224, 155)
    RIDER_HIGH_DAMAGE = (659, 244, 288, 0, 275, 200)
    RIDER_BALANCE = (683, 259, 266, 0, 297, 133)
    GUARD_STRIKE = (1219, 155, 377, 0, 193, 0)
    GUARD_DEFENSE = (1370, 0, 397, 0, 211, 0)
    SORCERER_DAMAGE = (732, 0, 262, 259, 350, 0)
    SORCERER_ASSIST = (770, 0, 280, 244, 375, 0)
    WARRIOR = (810, 0, 288, 259, 308, 0)


class ShenbinProfessions(enum.Enum):
    SWORDSMAN_WITH_MAGIC = (85, 0, 0, 79, 0, 0)
    SWORDSMAN = (85, 79, 0, 0, 0, 0)
    PRIEST = (77, 0, 0, 63, 0, 0)
    ARCHER = (76, 74, 0, 0, 0, 0)
    RIDER_HIGH_DAMAGE = (78, 73, 0, 0, 0, 0)
    RIDER_BALANCE = (81, 77, 0, 0, 0, 0)
    GUARD_STRIKE = (90, 75, 0, 0, 0, 0)
    GUARD_DEFENSE = (98, 73, 0, 0, 0, 0)  # include wuxiang.mifu
    SORCERER_DAMAGE = (71, 0, 0, 77, 0, 0)
    SORCERER_ASSIST = (76, 0, 0, 73, 0, 0)
    WARRIOR = (76, 0, 0, 73, 0, 0)


class HuazhenProfessions(enum.Enum):
    SWORDSMAN = (96, 45, 34, 0, 21, 35)
    SWORDSMAN_WITH_MAGIC = (96, 0, 34, 45, 21, 35)
    PRIEST = (84, 0, 29, 36, 38, 30)
    ARCHER = (86, 42, 30, 0, 23, 40)
    RIDER_HIGH_DAMAGE = (88, 41, 29, 0, 28, 46)
    RIDER_BALANCE = (88, 41, 29, 0, 28, 45)
    GUARD_STRIKE = (114, 39, 41, 0, 21, 30)
    GUARD_DEFENSE = (114, 39, 41, 0, 21, 30)
    SORCERER_DAMAGE = (80, 0, 27, 43, 36, 35)
    SORCERER_ASSIST = (80, 0, 27, 43, 36, 35)
    WARRIOR = (84, 0, 30, 43, 33, 30)


class XingpanProfessions(enum.Enum):
    SWORDSMAN = (120, 45, 20, 0, 15, 0)
    SWORDSMAN_WITH_MAGIC = (100, 0, 15, 42, 22, 0)
    PRIEST = (105, 0, 18, 36, 24, 0)
    ARCHER = (110, 42, 18, 0, 15, 0)
    RIDER_HIGH_DAMAGE = (115, 42, 17, 0, 17, 0)
    RIDER_BALANCE = (115, 42, 17, 0, 17, 0)
    GUARD_STRIKE = (145, 36, 25, 0, 15, 0)
    GUARD_DEFENSE = (145, 36, 25, 0, 15, 0)
    SORCERER_DAMAGE = (100, 0, 15, 42, 22, 0)
    SORCERER_ASSIST = (100, 0, 15, 42, 22, 0)
    WARRIOR = (105, 0, 18, 40, 18, 0)


class HuazhenAmplifier(enum.Enum):
    SWORDSMAN = (4, 2, 2, 0, 2, 2)
    SWORDSMAN_WITH_MAGIC = (4, 0, 2, 2, 2, 2)
    PRIEST = (4, 0, 2, 2, 2, 2)
    ARCHER = (4, 2, 2, 0, 2, 2)
    RIDER_HIGH_DAMAGE = (4, 2, 2, 0, 2, 2)
    RIDER_BALANCE = (4, 2, 2, 0, 2, 2)
    GUARD_STRIKE = (4, 2, 2, 0, 2, 2)
    GUARD_DEFENSE = (4, 2, 2, 0, 2, 2)
    SORCERER_DAMAGE = (4, 0, 2, 2, 2, 2)
    SORCERER_ASSIST = (4, 0, 2, 2, 2, 2)
    WARRIOR = (4, 0, 2, 2, 2, 2)


def calculateMaxAddedValue(wuneiProfession, jishenProfession, shenbinProfession,
                           huazhenProfession, xingpan_profession):
    # Ensure each profession is a tuple of 6 numbers
    print('profession is', [jishenProfession, shenbinProfession, huazhenProfession, wuneiProfession])
    # if not all(len(profession) == 6 for profession in
    #            [jishenProfession, shenbinProfession, huazhenProfession, wuneiProfession]):
    #     raise ValueError("Each profession must be a tuple of 6 numbers")

    # Applying the formula to each corresponding element
    calculated_values = tuple(
        jishenProfession.value[i] +
        shenbinProfession.value[i] * (69 / 10 + 1) +
        huazhenProfession.value[i] +
        sum(wuneiProfession.value[i]) +
        xingpan_profession.value[i]
        for i in range(6)
    )

    return Attributes(*calculated_values)
